"""Compose the v1.0 layers in order, like a Spring Boot stack."""

from __future__ import annotations

_LAYERS = (
    "http",
    "security",
    "budget",
    "rag",
    "agent",
    "observe",
    "evals",
)


def architecture_layers() -> list[str]:
    """Return http, security, budget, rag, agent, observe, evals — in that order."""
    return list(_LAYERS)


def layer_index(name: str) -> int:
    """0-based index of a layer. Raise KeyError if unknown."""
    try:
        return architecture_layers().index(name)
    except ValueError as exc:
        raise KeyError(name) from exc
