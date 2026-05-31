"""Tracks the last upstream commit we successfully translated."""
from __future__ import annotations

import json

from . import config


def load_state() -> dict:
    if config.STATE_FILE.exists():
        try:
            return json.loads(config.STATE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"last_commit": None, "last_sync": None, "translated_files": []}


def save_state(state: dict) -> None:
    config.STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
