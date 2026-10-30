"""Guided: injection markers and secret redaction."""

from __future__ import annotations

from collections.abc import Sequence

# Keep this list in the starter so the exercise is about using it, not inventing it.
MARKERS = (
    "ignore previous instructions",
    "dump the system prompt",
    "print the api key",
    "call delete_page",
)


def looks_like_injection(text: str) -> bool:
    """True when any MARKER appears in text (case-insensitive)."""
    raise NotImplementedError


def redact_secrets(text: str, secrets: Sequence[str]) -> str:
    """Replace each non-empty secret with ***."""
    raise NotImplementedError
