"""Hashing-trick embedder (not a neural model) (solution)."""

from __future__ import annotations

import hashlib
import re

import numpy as np
from numpy.typing import NDArray

_TOKEN = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def token_hash_embed(text: str, *, dim: int = 8) -> NDArray[np.float64]:
    """Return a L2-normalized dim-vector. Empty text → e0. dim must be >= 2."""
    if dim < 2:
        raise ValueError("dim must be >= 2")
    vec = np.zeros(dim, dtype=np.float64)
    for token in _TOKEN.findall(text.lower()):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "little") % dim
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vec[index] += sign
    norm = float(np.linalg.norm(vec))
    if norm == 0.0:
        vec[0] = 1.0
        return vec
    return vec / norm
