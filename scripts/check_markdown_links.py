"""Fail if a repo-relative Markdown link does not resolve to a file.

Skips http(s), mailto, and bare same-file anchors. Used by tests and
`uv run python scripts/check_markdown_links.py`.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from course_kit.loader import repo_root

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "irc:")
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"}


def markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def targets(markdown: str) -> list[str]:
    found: list[str] = []
    for match in LINK_RE.finditer(markdown):
        raw = match.group(1).strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1].strip()
        href = raw.split()[0] if raw else ""
        href = href.strip("\"'")
        if not href or href.startswith("#"):
            continue
        if any(href.lower().startswith(prefix) for prefix in SKIP_PREFIXES):
            continue
        found.append(href)
    return found


def resolve(source: Path, href: str) -> Path:
    path_part = href.split("#", 1)[0].split("?", 1)[0]
    if not path_part:
        return source
    return (source.parent / path_part).resolve()


def broken_links(root: Path) -> list[tuple[Path, str, Path]]:
    root = root.resolve()
    broken: list[tuple[Path, str, Path]] = []
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for href in targets(text):
            dest = resolve(path, href)
            try:
                dest.relative_to(root)
            except ValueError:
                broken.append((path, href, dest))
                continue
            if not dest.exists():
                broken.append((path, href, dest))
    return broken


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check repo-relative Markdown links")
    parser.parse_args(argv)
    root = repo_root()
    issues = broken_links(root)
    if not issues:
        print("All relative Markdown links resolve")
        return 0
    for source, href, dest in issues:
        print(f"BROKEN {source.relative_to(root)} -> {href} (resolved {dest})")
    print(f"{len(issues)} broken Markdown link(s)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
