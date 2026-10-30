"""Hashing-trick embedder (not a neural model)."""

from __future__ import annotations

from numpy.typing import NDArray
import numpy as np


def token_hash_embed(text: str, *, dim: int = 8) -> NDArray[np.float64]:
    """Return a L2-normalized dim-vector. Empty text → e0. dim must be >= 2."""
    raise NotImplementedError
