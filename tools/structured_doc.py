"""Structure-preserving Markdown helpers.

The translation pipeline must NEVER drop, merge, or demote a heading, and every
in-page anchor link must keep resolving. To guarantee that, we parse the English
doc into an ordered list of heading / body nodes, translate them separately, and
reassemble with heading levels copied verbatim from the source. Anchors are then
rewritten from the English GitHub slug to the new Chinese slug.
"""
from __future__ import annotations

import re

_FENCE = re.compile(r"^\s*(```+|~~~+)")
_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*$")
_LINK_ANCHOR = re.compile(r"\]\(#([^)]+)\)")


def parse_nodes(text: str) -> list[dict]:
    """Split into ordered nodes: {'type':'heading',level,text,nl} | {'type':'body',text}."""
    lines = text.splitlines(keepends=True)
    nodes: list[dict] = []
    body: list[str] = []
    in_fence = False
    marker = ""

    def flush_body():
        if body:
            nodes.append({"type": "body", "text": "".join(body)})
            body.clear()

    for line in lines:
        fm = _FENCE.match(line)
        is_heading = False
        if fm:
            mk = fm.group(1)[0] * 3
            if not in_fence:
                in_fence, marker = True, mk
            elif line.lstrip().startswith(marker):
                in_fence = False
        elif not in_fence:
            stripped = line.rstrip("\n")
            hm = _HEADING.match(stripped)
            if hm:
                is_heading = True
                flush_body()
                nl = line[len(stripped):]  # preserve original line ending
                nodes.append({
                    "type": "heading",
                    "level": len(hm.group(1)),
                    "text": hm.group(2).strip(),
                    "nl": nl or "\n",
                })
        if not is_heading:
            body.append(line)
    flush_body()
    return nodes


def split_code_segments(text: str) -> list[tuple[str, str]]:
    """Split body text into ordered ('prose'|'code', text) segments, fence-aware.

    Code segments (whole fenced blocks, fences included) are kept verbatim and
    never sent to the translator, guaranteeing byte-identical code and fences.
    Concatenating all segment texts reproduces the input exactly.
    """
    lines = text.splitlines(keepends=True)
    segments: list[tuple[str, str]] = []
    prose: list[str] = []
    code: list[str] = []
    in_fence = False
    marker = ""

    def flush_prose():
        if prose:
            segments.append(("prose", "".join(prose)))
            prose.clear()

    for line in lines:
        fm = _FENCE.match(line)
        if fm:
            mk = fm.group(1)[0] * 3
            if not in_fence:
                flush_prose()
                in_fence, marker = True, mk
                code.append(line)
                continue
            if line.lstrip().startswith(marker):
                code.append(line)
                segments.append(("code", "".join(code)))
                code.clear()
                in_fence = False
                continue
            code.append(line)
            continue
        if in_fence:
            code.append(line)
        else:
            prose.append(line)
    # Unterminated fence (malformed source): treat accumulated code as prose-safe verbatim.
    if code:
        segments.append(("code", "".join(code)))
    flush_prose()
    return segments


def github_slug(text: str, seen: dict[str, int]) -> str:
    """Reproduce GitHub's heading-anchor slug algorithm (incl. duplicate counter)."""
    s = text
    s = re.sub(r"`([^`]*)`", r"\1", s)              # inline code -> contents
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)  # links -> visible text
    s = re.sub(r"<[^>]+>", "", s)                   # strip HTML tags
    s = s.strip().lower()
    out = []
    for ch in s:
        if ch.isalnum() or ch in (" ", "-", "_"):   # isalnum keeps CJK/Unicode letters
            out.append(ch)
    base = "".join(out).replace(" ", "-")
    if base in seen:
        seen[base] += 1
        return f"{base}-{seen[base]}"
    seen[base] = 0
    return base


def build_slug_map(en_headings: list[str], zh_headings: list[str]) -> dict[str, str]:
    """Map English slug -> Chinese slug, position by position (1:1 by construction)."""
    assert len(en_headings) == len(zh_headings), "heading counts must match"
    en_seen: dict[str, int] = {}
    zh_seen: dict[str, int] = {}
    mapping: dict[str, str] = {}
    for en, zh in zip(en_headings, zh_headings):
        en_slug = github_slug(en, en_seen)
        zh_slug = github_slug(zh, zh_seen)
        if en_slug and en_slug != zh_slug:
            mapping[en_slug] = zh_slug
    return mapping


def rewrite_anchors(text: str, slug_map: dict[str, str]) -> tuple[str, int]:
    """Rewrite `](#en-slug)` link targets to the Chinese slug. Returns (text, n_rewritten)."""
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        slug = m.group(1)
        if slug in slug_map:
            n += 1
            return f"](#{slug_map[slug]})"
        return m.group(0)

    return _LINK_ANCHOR.sub(repl, text), n
