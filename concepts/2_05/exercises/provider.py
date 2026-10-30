"""Resolve LLM_PROVIDER the way get_client does."""

from __future__ import annotations

VALID = ("fake", "ollama", "openai")


def resolve_provider(name: str | None) -> str:
    """Lowercase, default fake. Raise ValueError on unknown names."""
    raise NotImplementedError


def is_live(name: str) -> bool:
    """True for ollama and openai (opt-in). False for fake."""
    raise NotImplementedError
