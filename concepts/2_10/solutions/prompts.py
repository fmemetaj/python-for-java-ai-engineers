"""Load a versioned prompt file (solution)."""

from __future__ import annotations

from pathlib import Path


def load_prompt(path: Path) -> str:
    """Return file text stripped of surrounding whitespace."""
    return path.read_text(encoding="utf-8").strip()


def prompt_version(path: Path) -> str:
    """Return the filename stem (e.g. answer_from_doc.v1)."""
    return path.stem
