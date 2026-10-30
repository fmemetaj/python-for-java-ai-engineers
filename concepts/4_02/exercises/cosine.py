"""Cosine similarity."""

from __future__ import annotations

from collections.abc import Sequence


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    """dot / (|a||b|). Return 0.0 if either vector has norm 0. Raise on shape mismatch."""
    raise NotImplementedError
