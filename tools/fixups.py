"""Deterministic post-translation fixups: terminology normalization + targeted
corrections for known model slips. Reproducible and version-controlled so the
recurring pipeline self-heals these issues on every run.

Applied to the assembled translated document BEFORE anchor rewrite, so that any
normalization which changes a heading is reflected in both the heading and the
links that target it (the anchor rewrite recomputes slugs afterwards).
"""
from __future__ import annotations

import json

from . import config

_FIXUPS_FILE = config.ROOT / "fixups.json"


def load_fixups() -> dict:
    if _FIXUPS_FILE.exists():
        return json.loads(_FIXUPS_FILE.read_text(encoding="utf-8"))
    return {"normalize": {}, "literal": []}


def apply_fixups(text: str, fixups: dict | None = None) -> tuple[str, int]:
    """Return (fixed_text, n_changes)."""
    fx = fixups if fixups is not None else load_fixups()
    n = 0
    for src, dst in (fx.get("normalize") or {}).items():
        if src and src != dst and src in text:
            n += text.count(src)
            text = text.replace(src, dst)
    for rule in fx.get("literal") or []:
        find, replace = rule.get("find"), rule.get("replace", "")
        if find and find in text:
            n += text.count(find)
            text = text.replace(find, replace)
    return text, n
