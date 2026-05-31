"""DeepSeek-backed Markdown translator with multi-key rotation + failover."""
from __future__ import annotations

import hashlib
import json
import threading
import time

import requests

from . import config


class KeyPool:
    """Round-robin key pool that quarantines keys hitting rate/auth errors."""

    def __init__(self, keys: list[str]):
        if not keys:
            raise SystemExit(
                "No DeepSeek API keys found. Set DEEPSEEK_API_KEYS or DEEPSEEK_API_KEY."
            )
        self._keys = keys
        self._idx = 0
        self._cooldown: dict[int, float] = {}
        self._lock = threading.Lock()

    def acquire(self) -> tuple[int, str]:
        with self._lock:
            n = len(self._keys)
            for _ in range(n):
                i = self._idx
                self._idx = (self._idx + 1) % n
                until = self._cooldown.get(i, 0.0)
                if until <= time.monotonic():
                    return i, self._keys[i]
            # All keys cooling down: pick the soonest-free one.
            i = min(self._cooldown, key=self._cooldown.get)
            wait = max(0.0, self._cooldown[i] - time.monotonic())
            if wait:
                time.sleep(min(wait, 30))
            return i, self._keys[i]

    def penalize(self, idx: int, seconds: float) -> None:
        with self._lock:
            self._cooldown[idx] = time.monotonic() + seconds


SYSTEM_PROMPT = """你是一名资深技术文档翻译专家,负责把 Claude Code 的英文技术文档翻译成简体中文。

严格遵守以下规则:
1. 只翻译正文与说明性文字。保持 Markdown 结构完全不变:标题层级、列表、表格、引用块、加粗/斜体标记。
2. 绝不翻译或改动:代码块(``` 或 ~~~ 之间的内容)、行内代码(反引号包裹)、命令、文件路径、URL、HTML/徽章、YAML/JSON 键名、环境变量名。
3. 标题里的锚点链接(如 [文字](#anchor))中的 #anchor 锚点保持英文原样,只翻译方括号内的显示文字。
4. 专有名词与产品名保持英文:Claude Code、MCP、CLI、API、Hooks、Skills、Plugins、Anthropic、SDK 等。
5. 译文要自然、专业、符合中文技术读者习惯,不要逐字硬译。
6. 直接输出翻译后的 Markdown,不要添加任何解释、前后缀或代码围栏包裹整体内容。
7. 输入可能是文档的一个片段,可能从句子中间开始或结束 —— 按原样翻译,不要补全或删减。"""


def _glossary_hint(glossary: dict) -> str:
    keep = glossary.get("keep") or []
    mapping = glossary.get("map") or {}
    parts = []
    if keep:
        parts.append("以下术语保持英文不译:" + "、".join(keep) + "。")
    if mapping:
        pairs = "; ".join(f"{en} → {zh}" for en, zh in mapping.items())
        parts.append("以下术语按固定译法翻译:" + pairs + "。")
    return "\n".join(parts)


class Translator:
    def __init__(self, glossary: dict | None = None):
        self.pool = KeyPool(config.load_api_keys())
        self.glossary = glossary or config.load_glossary()
        self._glossary_hint = _glossary_hint(self.glossary)
        self.cache = self._load_cache()
        self._cache_dirty = False
        self.stats = {"hits": 0, "misses": 0, "api_calls": 0}

    # ---- chunk cache -------------------------------------------------------
    def _load_cache(self) -> dict:
        if config.TRANSLATION_CACHE.exists():
            try:
                return json.loads(config.TRANSLATION_CACHE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return {}
        return {}

    def save_cache(self) -> None:
        if not self._cache_dirty:
            return
        config.TRANSLATION_CACHE.parent.mkdir(parents=True, exist_ok=True)
        config.TRANSLATION_CACHE.write_text(
            json.dumps(self.cache, ensure_ascii=False, indent=0), encoding="utf-8"
        )

    def _cache_key(self, chunk: str) -> str:
        h = hashlib.sha256()
        h.update(config.DEEPSEEK_MODEL.encode())
        h.update(b"\x00")
        h.update(self._glossary_hint.encode())
        h.update(b"\x00")
        h.update(chunk.encode("utf-8"))
        return h.hexdigest()

    # ---- API call ----------------------------------------------------------
    def _call_api(self, chunk: str) -> str:
        user_content = chunk
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT + (
                "\n\n术语表:\n" + self._glossary_hint if self._glossary_hint else "")},
            {"role": "user", "content": user_content},
        ]
        payload = {
            "model": config.DEEPSEEK_MODEL,
            "messages": messages,
            "temperature": config.TEMPERATURE,
            "stream": False,
        }
        url = config.DEEPSEEK_BASE_URL.rstrip("/") + "/chat/completions"

        last_err = None
        attempts = max(len(self.pool._keys) * config.MAX_RETRIES_PER_KEY, 3)
        for attempt in range(attempts):
            idx, key = self.pool.acquire()
            try:
                self.stats["api_calls"] += 1
                resp = requests.post(
                    url,
                    headers={"Authorization": f"Bearer {key}",
                             "Content-Type": "application/json"},
                    json=payload,
                    timeout=config.REQUEST_TIMEOUT,
                )
            except requests.RequestException as e:
                last_err = e
                time.sleep(min(2 ** attempt, 20))
                continue

            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]

            # Rate limited or quota -> quarantine this key, try the next.
            if resp.status_code in (429, 402):
                self.pool.penalize(idx, 60)
                last_err = RuntimeError(f"{resp.status_code}: {resp.text[:200]}")
                time.sleep(min(2 ** attempt, 20))
                continue
            # Auth problems -> long quarantine.
            if resp.status_code in (401, 403):
                self.pool.penalize(idx, 600)
                last_err = RuntimeError(f"{resp.status_code}: {resp.text[:200]}")
                continue
            # Server errors -> backoff and retry.
            if resp.status_code >= 500:
                last_err = RuntimeError(f"{resp.status_code}: {resp.text[:200]}")
                time.sleep(min(2 ** attempt, 20))
                continue
            # Other 4xx -> not retryable.
            raise RuntimeError(f"DeepSeek API error {resp.status_code}: {resp.text[:300]}")

        raise RuntimeError(f"Translation failed after {attempts} attempts: {last_err}")

    def translate_chunk(self, chunk: str) -> str:
        if not chunk.strip():
            return chunk
        ck = self._cache_key(chunk)
        if ck in self.cache:
            self.stats["hits"] += 1
            return self.cache[ck]
        self.stats["misses"] += 1
        translated = self._call_api(chunk)
        self.cache[ck] = translated
        self._cache_dirty = True
        return translated

    def translate_document(self, text: str) -> str:
        from .markdown_chunker import split_markdown

        chunks = split_markdown(text, config.MAX_CHUNK_CHARS)
        return "".join(self.translate_chunk(c) for c in chunks)
