"""Batch embeddings as a matrix (solution)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from course_kit.rag.embeddings import token_hash_embed


def embed_many(texts: list[str], *, dim: int = 8) -> NDArray[np.float64]:
    """Stack token_hash_embed rows. Empty list → shape (0, dim)."""
    if not texts:
        return np.zeros((0, dim), dtype=np.float64)
    return np.stack([token_hash_embed(text, dim=dim) for text in texts])
