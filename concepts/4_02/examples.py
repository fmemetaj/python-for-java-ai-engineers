"""Cosine, L2-norm, top-k. Offline numpy only."""

from __future__ import annotations

import numpy as np

from course_kit.rag.vectors import cosine_similarity, l2_normalize, top_k

# Example 1 — parallel.
assert cosine_similarity([1.0, 0.0], [2.0, 0.0]) == 1.0

# Example 2 — orthogonal.
assert abs(cosine_similarity([1.0, 0.0], [0.0, 1.0])) < 1e-12

# Example 3 — opposite.
assert cosine_similarity([1.0, 0.0], [-1.0, 0.0]) == -1.0

# Example 4 — 3-4-5 triangle.
unit = l2_normalize([3.0, 4.0])
assert np.allclose(unit, [0.6, 0.8])
assert cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0

# Example 5 — top-k order.
matrix = np.array([[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]], dtype=np.float64)
ranked = top_k([1.0, 0.0], matrix, k=2)
assert ranked[0][0] == 0
assert ranked[1][0] == 2

print("4.2 examples ok")
