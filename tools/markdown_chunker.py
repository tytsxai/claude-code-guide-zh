"""Split markdown into translation chunks.

Rules:
- Never split inside a fenced code block (``` or ~~~).
- Prefer to break at heading boundaries (#..######) or horizontal rules (---).
- Greedily pack content up to ``max_chars`` per chunk.
- The concatenation of all returned chunks reproduces the input byte-for-byte,
  so reassembling translated chunks needs no separator bookkeeping.
"""
from __future__ import annotations

import re

_HEADING = re.compile(r"^#{1,6}\s")
_FENCE = re.compile(r"^\s*(```+|~~~+)")
_HR = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")


def _is_break_point(line: str) -> bool:
    return bool(_HEADING.match(line) or _HR.match(line))


def split_markdown(text: str, max_chars: int) -> list[str]:
    lines = text.splitlines(keepends=True)
    chunks: list[str] = []
    buf: list[str] = []
    buf_len = 0
    in_fence = False
    fence_marker = ""

    for line in lines:
        stripped = line.lstrip()
        fence_match = _FENCE.match(line)
        if fence_match:
            marker = fence_match.group(1)[0] * 3  # normalise ``` / ~~~
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif stripped.startswith(fence_marker):
                in_fence = False

        # Decide whether to flush *before* appending this line.
        if (
            not in_fence
            and buf_len >= max_chars
            and _is_break_point(line)
            and buf
        ):
            chunks.append("".join(buf))
            buf, buf_len = [], 0

        buf.append(line)
        buf_len += len(line)

    if buf:
        chunks.append("".join(buf))

    # Safety net: if a single chunk is still way over budget (e.g. a giant code
    # block with no break points), hard-split it so the API call doesn't fail.
    hard_limit = max_chars * 3
    out: list[str] = []
    for c in chunks:
        if len(c) <= hard_limit:
            out.append(c)
            continue
        for i in range(0, len(c), max_chars):
            out.append(c[i : i + max_chars])
    return out or [""]
