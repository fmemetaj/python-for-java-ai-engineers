"""L2-normalize and cosine top-k indices (solution)."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from course_kit.rag.vectors import l2_normalize as _norm, top_k


def l2_normalize(values: Sequence[float]) -> NDArray[np.float64]:
    """Divide by Euclidean norm. Zero vector stays zero."""
    return _norm(values)


def topk_indices(query: Sequence[float], matrix: Sequence[Sequence[float]], k: int) -> list[int]:
    """Indices of the k highest cosine rows, highest first."""
    return [index for index, _score in top_k(query, matrix, k=k)]
