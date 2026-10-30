"""BM25, min-max fusion, cosine rerank."""

from __future__ import annotations

from collections.abc import Sequence


def bm25_scores(query: str, docs: Sequence[str]) -> list[float]:
    """Okapi BM25 scores, one per doc. Empty corpus → []."""
    raise NotImplementedError


def fuse_scores(
    vector_scores: Sequence[float],
    lexical_scores: Sequence[float],
    *,
    alpha: float,
) -> list[float]:
    """min-max each list, then alpha * vector + (1-alpha) * lexical."""
    raise NotImplementedError


def rerank_ids(
    query_vector: Sequence[float],
    ids: Sequence[str],
    vectors: Sequence[Sequence[float]],
    *,
    k: int,
) -> list[str]:
    """Return k ids with the highest cosine to query_vector."""
    raise NotImplementedError
