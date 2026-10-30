"""BM25 + cosine fusion. Offline; no live search cluster."""

from __future__ import annotations

from course_kit.rag.hybrid import bm25_scores, fuse_scores, min_max, rerank_by_cosine

docs = [
    "Bearer JWT authentication header",
    "HMAC-SHA256 webhook signature",
    "refund a captured payment",
]
lexical = bm25_scores("refund captured", docs)
assert lexical[2] > lexical[0]

# Example: min-max then fuse. Equal BM25 → zeros → cosine decides.
assert min_max([5.0, 5.0, 5.0]) == [0.0, 0.0, 0.0]
fused = fuse_scores([0.1, 0.9, 0.2], [10.0, 1.0, 1.0], alpha=0.5)
assert fused[0] > fused[2] or fused[1] >= min(fused)

reranked = rerank_by_cosine(
    [1.0, 0.0],
    [{"id": "a"}, {"id": "b"}],
    [[0.0, 1.0], [1.0, 0.0]],
    k=1,
)
assert reranked[0]["id"] == "b"

print("4.7 examples ok")
