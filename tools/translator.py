"""DeepSeek-backed Markdown translator with multi-key rotation + failover."""
from __future__ import annotations

import hashlib
import json
import re
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


# Only 0-3 leading spaces count as an ATX heading; 4+ spaces is an indented code
# block (e.g. an example CLAUDE.md), whose `#` lines must NOT be touched.
_STRAY_HEADING = re.compile(r"(?m)^( {0,3})#{1,6}[ \t]+(.*)$")


def _strip_stray_headings(text: str) -> str:
    """Prose segments contain no headings by construction; the model occasionally
    hallucinates one (prepends `#`). Demote any such line back to plain prose."""
    return _STRAY_HEADING.sub(r"\1\2", text)


HEADING_SYS = """你是技术文档翻译专家。下面每一行是一个 Markdown 标题文本,格式为 `<<<编号>>> 英文标题`。
把每个标题翻译成简体中文,严格遵守:
1. 逐条翻译,输出必须保持完全相同的 `<<<编号>>> 译文` 格式,编号和行数与输入一一对应,不增不减不合并。
2. 不要输出 Markdown 的 # 号(只翻译标题文字本身)。
3. 保留产品名与技术术语英文:Claude Code、MCP、CLI、API、SDK、Hooks、Skills、Plugins、CLAUDE.md 等。
4. 保留形如 [OFFICIAL]、[COMMUNITY]、[EXPERIMENTAL]、[NEW] 的标记原样不译。
5. 保留标题中的行内代码(反引号)、命令名、版本号原样。
6. 只输出带编号的译文,不要任何解释或额外文字。"""


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
        self._sys_translate = SYSTEM_PROMPT + (
            "\n\n术语表:\n" + self._glossary_hint if self._glossary_hint else "")
        self.cache = self._load_cache()
        self._cache_dirty = False
        self.stats = {"hits": 0, "misses": 0, "api_calls": 0}
        self._lock = threading.Lock()

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
    def _call_api(self, content: str, system_prompt: str | None = None) -> str:
        messages = [
            {"role": "system", "content": system_prompt or self._sys_translate},
            {"role": "user", "content": content},
        ]
        payload = {
            "model": config.DEEPSEEK_MODEL,
            "messages": messages,
            "stream": False,
            "max_tokens": config.MAX_OUTPUT_TOKENS,
        }
        if config.TEMPERATURE is not None:
            payload["temperature"] = config.TEMPERATURE
        url = config.DEEPSEEK_BASE_URL.rstrip("/") + "/chat/completions"

        last_err = None
        attempts = max(len(self.pool._keys) * config.MAX_RETRIES_PER_KEY, 3)
        for attempt in range(attempts):
            idx, key = self.pool.acquire()
            try:
                with self._lock:
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
                choice = data["choices"][0]
                content = choice["message"].get("content") or ""
                finish = choice.get("finish_reason")
                # Truncated output would silently corrupt the doc — surface it.
                if finish == "length":
                    last_err = RuntimeError(
                        "output truncated (finish_reason=length); raise DEEPSEEK_MAX_TOKENS "
                        "or lower MAX_CHUNK_CHARS"
                    )
                    raise last_err
                if not content.strip():
                    last_err = RuntimeError("empty content from API")
                    time.sleep(min(2 ** attempt, 20))
                    continue
                return content

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

    def translate_chunk(self, chunk: str, cache_tag: str = "") -> str:
        if not chunk.strip():
            return chunk
        # Preserve the EXACT leading/trailing whitespace around the segment.
        # The model strips boundary newlines, which would glue segments together
        # (e.g. prose onto the next code fence, breaking Markdown structure).
        core = chunk.strip()
        i = chunk.find(core)
        lead, trail = chunk[:i], chunk[i + len(core):]
        ck = self._cache_key(cache_tag + core)
        with self._lock:
            if ck in self.cache:
                self.stats["hits"] += 1
                return lead + self.cache[ck] + trail
            self.stats["misses"] += 1
        translated = self._call_api(core).strip()
        with self._lock:
            self.cache[ck] = translated
            self._cache_dirty = True
        return lead + translated + trail

    def _translate_body(self, text: str) -> str:
        """Translate a non-heading block.

        Fenced code blocks are kept byte-for-byte verbatim (never sent to the
        model), guaranteeing exact fence/code preservation. Only prose between
        code blocks is translated, sub-split if it exceeds the chunk size.
        """
        from . import structured_doc as sd
        from .markdown_chunker import split_markdown

        out: list[str] = []
        for kind, seg in sd.split_code_segments(text):
            if kind == "code" or not seg.strip():
                out.append(seg)
            elif len(seg) <= config.MAX_CHUNK_CHARS:
                out.append(_strip_stray_headings(self.translate_chunk(seg)))
            else:
                out.append(_strip_stray_headings("".join(
                    self.translate_chunk(c) for c in split_markdown(seg, config.MAX_CHUNK_CHARS))))
        return "".join(out)

    # ---- heading batch translation (structure-critical) --------------------
    def _translate_headings(self, headings: list[str]) -> list[str]:
        """Translate heading texts 1:1, count guaranteed (cache + batch + fallback)."""
        results: dict[str, str] = {}
        todo: list[str] = []
        for h in headings:
            ck = self._cache_key("HEADING::" + h)
            with self._lock:
                hit = self.cache.get(ck)
            if hit is not None:
                results[h] = hit
                with self._lock:
                    self.stats["hits"] += 1
            elif h not in results and h not in todo:
                todo.append(h)

        groups = [todo[i : i + 50] for i in range(0, len(todo), 50)]
        if groups:
            from concurrent.futures import ThreadPoolExecutor

            workers = max(1, min(config.CONCURRENCY, len(groups)))
            with ThreadPoolExecutor(max_workers=workers) as ex:
                batch_results = list(ex.map(self._heading_batch, groups))
            for group, translated in zip(groups, batch_results):
                for src, tr in zip(group, translated):
                    results[src] = tr
                    with self._lock:
                        self.cache[self._cache_key("HEADING::" + src)] = tr
                        self._cache_dirty = True
                        self.stats["misses"] += 1
        return [results[h] for h in headings]

    def _heading_batch(self, group: list[str]) -> list[str]:
        numbered = "\n".join(f"<<<{i}>>> {h}" for i, h in enumerate(group))
        out = self._call_api(numbered, HEADING_SYS)
        parsed: dict[int, str] = {}
        for m in re.finditer(r"<<<(\d+)>>>[ \t]*(.*)", out):
            parsed[int(m.group(1))] = m.group(2).strip()
        # Fallback: any index the batch failed to return gets translated alone.
        result = []
        for i, h in enumerate(group):
            if i in parsed and parsed[i]:
                result.append(parsed[i])
            else:
                single = self._call_api(f"<<<0>>> {h}", HEADING_SYS)
                ms = re.search(r"<<<0>>>[ \t]*(.*)", single)
                result.append(ms.group(1).strip() if ms and ms.group(1).strip() else h)
        return result

    # ---- top-level: structure-preserving document translation --------------
    def translate_markdown(self, text: str) -> str:
        from concurrent.futures import ThreadPoolExecutor

        from . import structured_doc as sd

        nodes = sd.parse_nodes(text)
        heading_nodes = [n for n in nodes if n["type"] == "heading"]
        body_nodes = [n for n in nodes if n["type"] == "body"]

        # 1. Headings: count- and level-preserving.
        en_headings = [n["text"] for n in heading_nodes]
        zh_headings = self._translate_headings(en_headings) if en_headings else []

        # 2. Bodies: translate in parallel across the key pool.
        workers = max(1, min(config.CONCURRENCY, max(1, len(body_nodes))))
        with ThreadPoolExecutor(max_workers=workers) as ex:
            zh_bodies = list(ex.map(lambda n: self._translate_body(n["text"]), body_nodes))

        # 3. Reassemble in original order, copying heading levels verbatim.
        out: list[str] = []
        hi = bi = 0
        for n in nodes:
            if n["type"] == "heading":
                out.append("#" * n["level"] + " " + zh_headings[hi] + n["nl"])
                hi += 1
            else:
                out.append(zh_bodies[bi])
                bi += 1
        assembled = "".join(out)

        # 4. Deterministic fixups (terminology normalization + known corrections).
        #    May alter heading text, so apply BEFORE recomputing anchor slugs.
        from . import fixups as fx

        assembled, n_fix = fx.apply_fixups(assembled)
        self.stats["fixups"] = self.stats.get("fixups", 0) + n_fix

        # 5. Rewrite anchors: English slug -> Chinese slug, using the POST-fixup
        #    heading text so links stay consistent with any normalized headings.
        fixed_nodes = sd.parse_nodes(assembled)
        fixed_zh = [n["text"] for n in fixed_nodes if n["type"] == "heading"]
        target_headings = fixed_zh if len(fixed_zh) == len(en_headings) else zh_headings
        slug_map = sd.build_slug_map(en_headings, target_headings)
        assembled, n_rewritten = sd.rewrite_anchors(assembled, slug_map)
        self.stats["anchors_rewritten"] = self.stats.get("anchors_rewritten", 0) + n_rewritten
        return assembled

    # Backwards-compatible alias.
    def translate_document(self, text: str) -> str:
        return self.translate_markdown(text)
