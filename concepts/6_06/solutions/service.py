"""Health payload and question validation. No HTTP server."""

from __future__ import annotations


def health() -> dict[str, str]:
    """Return status=ok and provider=fake. Must not call an LLM."""
    return {"status": "ok", "provider": "fake"}


def validate_question(question: str) -> str:
    """Return the stripped question. Raise ValueError when it is empty."""
    text = question.strip()
    if not text:
        raise ValueError("question must be non-empty")
    return text
