"""L2-normalize and cosine top-k indices."""

from __future__ import annotations

from collections.abc import Sequence

from numpy.typing import NDArray
import numpy as np


def l2_normalize(values: Sequence[float]) -> NDArray[np.float64]:
    """Divide by Euclidean norm. Zero vector stays zero."""
    raise NotImplementedError


def topk_indices(query: Sequence[float], matrix: Sequence[Sequence[float]], k: int) -> list[int]:
    """Indices of the k highest cosine rows, highest first."""
    raise NotImplementedError
