"""BM25, min-max fusion, cosine rerank (solution)."""

from __future__ import annotations

from collections.abc import Sequence

from course_kit.rag.hybrid import bm25_scores as _bm25, fuse_scores as _fuse, rerank_by_cosine


def bm25_scores(query: str, docs: Sequence[str]) -> list[float]:
    """Okapi BM25 scores, one per doc. Empty corpus → []."""
    return _bm25(query, docs)


def fuse_scores(
    vector_scores: Sequence[float],
    lexical_scores: Sequence[float],
    *,
    alpha: float,
) -> list[float]:
    """min-max each list, then alpha * vector + (1-alpha) * lexical."""
    return _fuse(vector_scores, lexical_scores, alpha=alpha)


def rerank_ids(
    query_vector: Sequence[float],
    ids: Sequence[str],
    vectors: Sequence[Sequence[float]],
    *,
    k: int,
) -> list[str]:
    """Return k ids with the highest cosine to query_vector."""
    hits = [{"id": ident} for ident in ids]
    ranked = rerank_by_cosine(query_vector, hits, vectors, k=k)
    return [str(hit["id"]) for hit in ranked]
