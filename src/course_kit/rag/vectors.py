"""Small numpy linear algebra for embeddings: cosine, L2-norm, top-k.

Java developers: this is `double[]` math, not a Stream pipeline. numpy arrays
are homogeneous and contiguous; a Python `list[float]` is a list of objects.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatVec = NDArray[np.float64]


def as_vector(values: ArrayLike) -> FloatVec:
    vec = np.asarray(values, dtype=np.float64)
    if vec.ndim != 1:
        raise ValueError(f"expected a 1-D vector, got shape {vec.shape}")
    return vec


def as_matrix(values: ArrayLike) -> FloatVec:
    mat = np.asarray(values, dtype=np.float64)
    if mat.ndim == 1:
        mat = mat.reshape(1, -1)
    if mat.ndim != 2:
        raise ValueError(f"expected a 2-D matrix, got shape {mat.shape}")
    return mat


def l2_normalize(values: ArrayLike) -> FloatVec:
    """Divide by the Euclidean norm. Zero vectors stay zero (cosine will be 0)."""
    vec = np.asarray(values, dtype=np.float64)
    if vec.ndim == 1:
        norm = float(np.linalg.norm(vec))
        if norm == 0.0:
            return vec.copy()
        return vec / norm
    if vec.ndim == 2:
        norms = np.linalg.norm(vec, axis=1, keepdims=True)
        safe = np.where(norms == 0.0, 1.0, norms)
        out = vec / safe
        out[norms.squeeze(1) == 0.0] = 0.0
        return out
    raise ValueError(f"expected 1-D or 2-D, got shape {vec.shape}")


def cosine_similarity(left: ArrayLike, right: ArrayLike) -> float:
    """Cosine similarity in [-1, 1]. Orthogonal → 0; parallel → 1; opposite → -1.

    cosine(a, b) = dot(a, b) / (|a| |b|). Zero-length vectors return 0.0 so a
    missing embedding never looks like a perfect match.
    """
    a = as_vector(left)
    b = as_vector(right)
    if a.shape != b.shape:
        raise ValueError(f"shape mismatch {a.shape} vs {b.shape}")
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def top_k(
    query: ArrayLike,
    matrix: ArrayLike,
    *,
    k: int = 5,
) -> list[tuple[int, float]]:
    """Return up to k (row_index, cosine) pairs, highest cosine first."""
    if k < 1:
        raise ValueError("k must be >= 1")
    q = l2_normalize(as_vector(query))
    mat = as_matrix(matrix)
    if mat.shape[0] == 0:
        return []
    if mat.shape[1] != q.shape[0]:
        raise ValueError(f"dim mismatch query {q.shape[0]} vs matrix {mat.shape[1]}")
    docs = l2_normalize(mat)
    scores = docs @ q
    take = min(k, scores.shape[0])
    # argpartition then sort the shortlist — fine for the course corpus size.
    order = np.argsort(-scores, kind="stable")[:take]
    return [(int(index), float(scores[index])) for index in order]
