"""Compose the v1.0 layers in order, like a Spring Boot stack."""

from __future__ import annotations


def architecture_layers() -> list[str]:
    """Return http, security, budget, rag, agent, observe, evals — in that order."""
    raise NotImplementedError


def layer_index(name: str) -> int:
    """0-based index of a layer. Raise KeyError if unknown."""
    raise NotImplementedError
