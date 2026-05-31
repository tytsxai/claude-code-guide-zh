"""Central configuration. All secrets come from environment variables only."""
from __future__ import annotations

import json
import os
from pathlib import Path

# ---- Paths -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache"
UPSTREAM_DIR = CACHE_DIR / "upstream"
TRANSLATION_CACHE = CACHE_DIR / "translations.json"
CONTENT_DIR = ROOT / "content"
STATE_FILE = ROOT / ".sync-state.json"
GLOSSARY_FILE = ROOT / "glossary.json"
UPDATE_LOG = ROOT / "content" / "update-log-zh.md"

# ---- Upstream --------------------------------------------------------------
UPSTREAM_REPO = os.environ.get(
    "UPSTREAM_REPO", "https://github.com/Cranot/claude-code-guide.git"
)
UPSTREAM_BRANCH = os.environ.get("UPSTREAM_BRANCH", "main")

# Files matching these suffixes get translated. Everything else is ignored.
TRANSLATE_SUFFIXES = {".md", ".markdown"}
# Files we never touch even if they match the suffix (upstream's own backups).
SKIP_NAMES = {"README_OLD_BACKUP.md"}

# ---- DeepSeek API ----------------------------------------------------------
# `deepseek-v4-flash` is a real, light-reasoning model (verified live against the
# API). It returns `reasoning_content` separately and spends a small reasoning
# budget, so we set an explicit MAX_OUTPUT_TOKENS below to avoid truncation.
# Alternatives: `deepseek-chat` (V3.x), `deepseek-reasoner` (R1).
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")

# Multi-key load balancing / failover. Provide keys via either:
#   DEEPSEEK_API_KEYS="key1,key2,key3"   (comma or whitespace separated)
# or a single DEEPSEEK_API_KEY.
def load_api_keys() -> list[str]:
    raw = os.environ.get("DEEPSEEK_API_KEYS") or os.environ.get("DEEPSEEK_API_KEY", "")
    for sep in (";", "\n", "\t", " "):
        raw = raw.replace(sep, ",")
    seen, keys = set(), []
    for k in (k.strip() for k in raw.split(",")):
        if k and k not in seen:
            seen.add(k)
            keys.append(k)
    return keys


# ---- Chunking / translation tuning ----------------------------------------
MAX_CHUNK_CHARS = int(os.environ.get("MAX_CHUNK_CHARS", "6000"))
REQUEST_TIMEOUT = int(os.environ.get("DEEPSEEK_TIMEOUT", "300"))
MAX_RETRIES_PER_KEY = int(os.environ.get("MAX_RETRIES_PER_KEY", "3"))
# Explicit output cap. DeepSeek's *default* is only 4096 tokens, which truncates
# large chunks (measured: a 12k-char section needs ~4200 output tokens). v4-flash
# also spends some budget on reasoning, so leave generous headroom.
MAX_OUTPUT_TOKENS = int(os.environ.get("DEEPSEEK_MAX_TOKENS", "8192"))
# Concurrent chunk translations. With multiple keys we fan out across them.
CONCURRENCY = int(os.environ.get("TRANSLATE_CONCURRENCY", "6"))
# Reasoning models (v4-flash, reasoner) can reject `temperature`; omit unless set.
_temp = os.environ.get("DEEPSEEK_TEMPERATURE")
TEMPERATURE = float(_temp) if _temp not in (None, "") else None

# This project's own repo (for the attribution banner's project link / Issue link).
PROJECT_REPO_URL = os.environ.get(
    "PROJECT_REPO_URL", "https://github.com/tytsxai/claude-code-guide-zh"
)

# Attribution banner prepended to the translated front-page guide (content/README.md).
# {repo_name}/{repo_url}/{author} = upstream source; {project_url} = THIS project.
ATTRIBUTION_BANNER = """> **🌏 非官方中文翻译版（机器翻译）** · 本文档由 [`claude-code-guide-zh`]({project_url}) 流水线**每小时**自动翻译并持续同步自上游英文仓库
> [{repo_name}]({repo_url})（原作者 [@{author}](https://github.com/{author})）。
> 译文仅供学习参考，**以[官方英文文档](https://code.claude.com/docs/en/overview)为准**；翻译问题欢迎到[本仓库]({project_url}/issues) 提 Issue。
> 翻译引擎：DeepSeek。

---

"""


def load_glossary() -> dict:
    if GLOSSARY_FILE.exists():
        return json.loads(GLOSSARY_FILE.read_text(encoding="utf-8"))
    return {"keep": [], "map": {}}
