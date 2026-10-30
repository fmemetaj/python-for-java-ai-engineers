"""Batch embeddings as a matrix."""

from __future__ import annotations

from numpy.typing import NDArray
import numpy as np


def embed_many(texts: list[str], *, dim: int = 8) -> NDArray[np.float64]:
    """Stack token_hash_embed rows. Empty list → shape (0, dim)."""
    raise NotImplementedError
