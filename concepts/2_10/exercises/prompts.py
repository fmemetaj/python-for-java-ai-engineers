"""Load a versioned prompt file."""

from __future__ import annotations

from pathlib import Path


def load_prompt(path: Path) -> str:
    """Return file text stripped of surrounding whitespace."""
    raise NotImplementedError


def prompt_version(path: Path) -> str:
    """Return the filename stem (e.g. answer_from_doc.v1)."""
    raise NotImplementedError
