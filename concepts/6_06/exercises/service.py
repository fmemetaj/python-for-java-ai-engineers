"""Health payload and question validation. No HTTP server."""

from __future__ import annotations


def health() -> dict[str, str]:
    """Return status=ok and provider=fake. Must not call an LLM."""
    raise NotImplementedError


def validate_question(question: str) -> str:
    """Return the stripped question. Raise ValueError when it is empty."""
    raise NotImplementedError
