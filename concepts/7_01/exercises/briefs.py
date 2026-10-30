"""Guided: the three original capstone briefs."""

from __future__ import annotations

from typing import Any


def list_briefs() -> list[str]:
    """Return the three brief ids in a stable order."""
    raise NotImplementedError


def choose_brief(name: str) -> dict[str, Any]:
    """Return a brief dict with id, title, corpus, write_tools. Raise KeyError if unknown."""
    raise NotImplementedError
