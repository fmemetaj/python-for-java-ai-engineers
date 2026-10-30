"""Cosine similarity (solution)."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    """dot / (|a||b|). Return 0.0 if either vector has norm 0. Raise on shape mismatch."""
    a = np.asarray(left, dtype=np.float64)
    b = np.asarray(right, dtype=np.float64)
    if a.shape != b.shape:
        raise ValueError("shape mismatch")
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))
