"""Resolve LLM_PROVIDER the way get_client does (solution)."""

from __future__ import annotations

VALID = ("fake", "ollama", "openai")


def resolve_provider(name: str | None) -> str:
    """Lowercase, default fake. Raise ValueError on unknown names."""
    resolved = (name or "fake").strip().lower() or "fake"
    if resolved not in VALID:
        raise ValueError(f"Unknown LLM_PROVIDER={resolved!r}. Use one of: {', '.join(VALID)}.")
    return resolved


def is_live(name: str) -> bool:
    """True for ollama and openai (opt-in). False for fake."""
    return resolve_provider(name) != "fake"
