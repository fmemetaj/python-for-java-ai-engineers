"""Lexical BM25 + dense cosine fusion, then optional cosine rerank.

Java analog: Elasticsearch BM25 scoring combined with a kNN clause, or a
`rescore` phase. Optional in Module 4 (concept 4.7).
Official BM25: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/relevance/bm25
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Sequence
from typing import Any

from numpy.typing import ArrayLike

from .embeddings import tokenize
from .store import VectorIndex
from .vectors import cosine_similarity


def bm25_scores(
    query: str,
    docs: Sequence[str],
    *,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[float]:
    """Okapi BM25 over an in-memory list of strings (no Lucene dependency)."""
    tokenized = [tokenize(doc) for doc in docs]
    q_tokens = tokenize(query)
    n_docs = len(docs)
    if n_docs == 0:
        return []
    avgdl = sum(len(tokens) for tokens in tokenized) / n_docs
    df: dict[str, int] = {}
    for tokens in tokenized:
        for term in set(tokens):
            df[term] = df.get(term, 0) + 1
    scores: list[float] = []
    for tokens in tokenized:
        tf_map = Counter(tokens)
        dl = len(tokens) or 1
        score = 0.0
        for term in q_tokens:
            tf = tf_map.get(term, 0)
            n_q = df.get(term, 0)
            idf = math.log(1.0 + (n_docs - n_q + 0.5) / (n_q + 0.5))
            denom = tf + k1 * (1.0 - b + b * dl / avgdl)
            if denom:
                score += idf * (tf * (k1 + 1.0)) / denom
        scores.append(score)
    return scores


def min_max(values: Sequence[float]) -> list[float]:
    if not values:
        return []
    lo = min(values)
    hi = max(values)
    if hi == lo:
        return [0.0] * len(values)
    return [(value - lo) / (hi - lo) for value in values]


def fuse_scores(
    vector_scores: Sequence[float],
    lexical_scores: Sequence[float],
    *,
    alpha: float = 0.6,
) -> list[float]:
    """alpha * cosine + (1 - alpha) * BM25 after independent min-max scaling."""
    if len(vector_scores) != len(lexical_scores):
        raise ValueError("score lists must be the same length")
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must be in [0, 1]")
    vec = min_max(vector_scores)
    lex = min_max(lexical_scores)
    return [alpha * left + (1.0 - alpha) * right for left, right in zip(vec, lex)]


def hybrid_search(
    query: str,
    index: VectorIndex,
    query_vector: ArrayLike,
    *,
    k: int = 5,
    alpha: float = 0.6,
    pool: int = 20,
) -> list[dict[str, Any]]:
    """Retrieve a pool by cosine, rescore with fused BM25 + cosine, return top-k."""
    hits = index.search(query_vector, k=max(pool, k))
    docs = [str(hit.get("text", "")) for hit in hits]
    lexical = bm25_scores(query, docs)
    vector = [float(hit["score"]) for hit in hits]
    fused = fuse_scores(vector, lexical, alpha=alpha)
    ranked = sorted(zip(fused, hits), key=lambda item: item[0], reverse=True)
    out: list[dict[str, Any]] = []
    for score, hit in ranked[:k]:
        row = dict(hit)
        row["hybrid_score"] = score
        out.append(row)
    return out


def rerank_by_cosine(
    query_vector: ArrayLike,
    hits: Sequence[dict[str, Any]],
    vectors: Sequence[Sequence[float]],
    *,
    k: int = 5,
) -> list[dict[str, Any]]:
    """Second-stage rerank: keep the candidate list, sort by cosine, take k."""
    scored: list[tuple[float, dict[str, Any]]] = []
    for hit, vector in zip(hits, vectors):
        scored.append((cosine_similarity(query_vector, vector), dict(hit)))
    scored.sort(key=lambda item: item[0], reverse=True)
    out: list[dict[str, Any]] = []
    for score, hit in scored[:k]:
        hit["rerank_score"] = score
        out.append(hit)
    return out
