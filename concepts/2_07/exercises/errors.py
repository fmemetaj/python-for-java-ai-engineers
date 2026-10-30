"""Spot official migration errors and read either output shape."""

from __future__ import annotations

from typing import Any


def is_migration_error(snippet: str) -> bool:
    """True if the snippet matches a common Chat Completions → Responses mistake."""
    raise NotImplementedError


def extract_text(payload: dict[str, Any]) -> str:
    """Read assistant text from a Responses object or a Chat Completions object."""
    raise NotImplementedError
