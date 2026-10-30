"""Embeddings as numpy vectors. Offline FakeEmbedder; not tiktoken, not Assistants."""

from __future__ import annotations

import numpy as np

from course_kit.rag import FakeEmbedder, get_embedder, token_hash_embed
from course_kit.rag.vectors import cosine_similarity

# Example 1 — a numpy vector is a homogeneous array, not ArrayList<Double>.
vec = np.array([1.0, 0.0, 0.0], dtype=np.float64)
assert vec.shape == (3,)
assert vec.ndim == 1

# Example 2 — dimension is part of the space.
eight = FakeEmbedder(dim=8).embed("hello")
assert eight.shape == (8,)

# Example 3 — deterministic.
left = token_hash_embed("Bearer JWT", dim=16)
right = token_hash_embed("Bearer JWT", dim=16)
assert np.allclose(left, right)
assert abs(float(np.linalg.norm(left)) - 1.0) < 1e-9

# Example 4 — shared tokens sit closer than unrelated jargon.
refund = token_hash_embed("refund captured payment", dim=32)
near = token_hash_embed("refund a captured payment", dim=32)
far = token_hash_embed("HMAC-SHA256 webhook signature", dim=32)
assert cosine_similarity(refund, near) > cosine_similarity(refund, far)

# Example 5 — empty text is a unit vector, not a silent zero.
empty = token_hash_embed("", dim=8)
assert empty[0] == 1.0
assert abs(float(np.linalg.norm(empty)) - 1.0) < 1e-9

# Example 6 — factory stays fake unless you opt in.
assert isinstance(get_embedder("fake"), FakeEmbedder)

print("4.1 examples ok")
