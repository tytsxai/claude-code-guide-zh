"""Sync + translate pipeline entry point.

Steps:
  1. Clone/update the upstream repo into a local cache.
  2. Diff the new commit against the last synced commit (full set on first run).
  3. Translate added/modified Markdown files into ``content/`` (mirroring paths).
  4. Remove translations for deleted files.
  5. Update sync state + write a Chinese update log.

Usage:
  python -m tools.sync                 # incremental sync
  python -m tools.sync --full          # re-translate everything
  python -m tools.sync --dry-run       # show what would change, no API calls
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import config, state


def run_git(args: list[str], cwd: Path) -> str:
    res = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    )
    return res.stdout.strip()


def ensure_upstream() -> Path:
    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    repo = config.UPSTREAM_DIR
    if (repo / ".git").exists():
        run_git(["fetch", "--depth", "50", "origin", config.UPSTREAM_BRANCH], repo)
        run_git(["checkout", config.UPSTREAM_BRANCH], repo)
        run_git(["reset", "--hard", f"origin/{config.UPSTREAM_BRANCH}"], repo)
    else:
        subprocess.run(
            ["git", "clone", "--depth", "50", "--branch", config.UPSTREAM_BRANCH,
             config.UPSTREAM_REPO, str(repo)],
            check=True,
        )
    return repo


def head_commit(repo: Path) -> str:
    return run_git(["rev-parse", "HEAD"], repo)


def changed_files(repo: Path, old: str | None) -> tuple[list[str], list[str]]:
    """Return (changed_or_added, deleted) relative paths."""
    if old is None:
        files = run_git(["ls-files"], repo).splitlines()
        return _filter(files), []
    try:
        diff = run_git(["diff", "--name-status", f"{old}..HEAD"], repo)
    except subprocess.CalledProcessError:
        # old commit not in shallow history -> treat as full sync
        files = run_git(["ls-files"], repo).splitlines()
        return _filter(files), []
    changed, deleted = [], []
    for line in diff.splitlines():
        parts = line.split("\t")
        status = parts[0]
        path = parts[-1]
        if status.startswith("D"):
            deleted.append(path)
        else:
            changed.append(path)
    return _filter(changed), _filter(deleted)


def _filter(paths: list[str]) -> list[str]:
    out = []
    for p in paths:
        name = Path(p).name
        if name in config.SKIP_NAMES:
            continue
        if Path(p).suffix.lower() in config.TRANSLATE_SUFFIXES:
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="re-translate everything")
    ap.add_argument("--dry-run", action="store_true", help="no API calls, just report")
    args = ap.parse_args()

    repo = ensure_upstream()
    new_commit = head_commit(repo)
    st = state.load_state()
    old_commit = None if args.full else st.get("last_commit")

    changed, deleted = changed_files(repo, old_commit)
    print(f"Upstream HEAD: {new_commit[:10]}  (was {str(old_commit)[:10]})")
    print(f"Markdown files to translate: {len(changed)}  | deleted: {len(deleted)}")
    for p in changed:
        print(f"  ~ {p}")
    for p in deleted:
        print(f"  - {p}")

    if args.dry_run:
        print("\n[dry-run] no API calls made.")
        return 0

    if not changed and not deleted:
        print("Nothing to do — already up to date.")
        return 0

    from .translator import Translator

    translator = Translator()
    config.CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    done = []
    try:
        for rel in changed:
            src = repo / rel
            if not src.exists():
                continue
            text = src.read_text(encoding="utf-8", errors="replace")
            print(f"Translating {rel} ({len(text)} chars)...", flush=True)
            translated = translator.translate_document(text)
            if rel == "README.md":
                banner = config.ATTRIBUTION_BANNER.format(
                    repo_name="Cranot/claude-code-guide",
                    repo_url="https://github.com/Cranot/claude-code-guide",
                    author="Cranot",
                )
                translated = banner + translated
            dest = config.CONTENT_DIR / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(translated, encoding="utf-8")
            done.append(rel)
    finally:
        translator.save_cache()

    for rel in deleted:
        dest = config.CONTENT_DIR / rel
        if dest.exists():
            dest.unlink()

    # Update state.
    now = datetime.now(timezone.utc).isoformat()
    tracked = set(st.get("translated_files", [])) | set(done)
    tracked -= set(deleted)
    st.update({
        "last_commit": new_commit,
        "last_sync": now,
        "translated_files": sorted(tracked),
    })
    state.save_state(st)

    _append_log(new_commit, done, deleted, translator.stats)

    print("\n--- summary ---")
    print(f"translated: {len(done)} | deleted: {len(deleted)}")
    print(f"cache hits: {translator.stats['hits']} | misses: {translator.stats['misses']}"
          f" | api calls: {translator.stats['api_calls']}")
    return 0


def _append_log(commit: str, done: list[str], deleted: list[str], stats: dict) -> None:
    config.UPDATE_LOG.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"## {now} · 上游 `{commit[:10]}`", ""]
    for p in done:
        lines.append(f"- 翻译更新：`{p}`")
    for p in deleted:
        lines.append(f"- 删除：`{p}`")
    lines.append(
        f"- 统计：缓存命中 {stats['hits']} / 新译 {stats['misses']} / API 调用 {stats['api_calls']}"
    )
    lines.append("")
    header = "# 同步更新日志\n\n本文件由自动化流水线生成，记录每次从上游同步与翻译的变更。\n\n"
    prev = ""
    if config.UPDATE_LOG.exists():
        existing = config.UPDATE_LOG.read_text(encoding="utf-8")
        prev = existing.split("\n\n", 2)[-1] if existing.startswith("# 同步更新日志") else existing
    config.UPDATE_LOG.write_text(header + "\n".join(lines) + "\n" + prev, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
