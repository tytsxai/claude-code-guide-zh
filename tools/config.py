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
# NOTE: `deepseek-v4-flash` was requested but is not (yet) a real DeepSeek model.
# Real models today: `deepseek-chat` (V3.x) and `deepseek-reasoner` (R1).
# Override with the DEEPSEEK_MODEL env var the moment a new model ships.
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

# Multi-key load balancing / failover. Provide keys via either:
#   DEEPSEEK_API_KEYS="key1,key2,key3"   (comma or whitespace separated)
# or a single DEEPSEEK_API_KEY.
def load_api_keys() -> list[str]:
    raw = os.environ.get("DEEPSEEK_API_KEYS") or os.environ.get("DEEPSEEK_API_KEY", "")
    keys = [k.strip() for k in raw.replace("\n", ",").replace(" ", ",").split(",")]
    return [k for k in keys if k]


# ---- Chunking / translation tuning ----------------------------------------
MAX_CHUNK_CHARS = int(os.environ.get("MAX_CHUNK_CHARS", "6000"))
REQUEST_TIMEOUT = int(os.environ.get("DEEPSEEK_TIMEOUT", "180"))
MAX_RETRIES_PER_KEY = int(os.environ.get("MAX_RETRIES_PER_KEY", "3"))
TEMPERATURE = float(os.environ.get("DEEPSEEK_TEMPERATURE", "0.2"))

# Attribution banner prepended to the translated front-page guide (content/README.md).
ATTRIBUTION_BANNER = """> **🌏 中文翻译版** · 本文档由机器自动翻译并持续同步自上游英文仓库
> [{repo_name}]({repo_url})（作者 [@{author}](https://github.com/{author})）。
> 译文仅供学习参考，**以官方英文原文为准**；如有翻译问题欢迎提 Issue。
> 由 [`claude-code-guide-zh`](https://github.com/{author}) 自动化流水线生成 · 翻译引擎：DeepSeek。

---

"""


def load_glossary() -> dict:
    if GLOSSARY_FILE.exists():
        return json.loads(GLOSSARY_FILE.read_text(encoding="utf-8"))
    return {"keep": [], "map": {}}
