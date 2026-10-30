"""Offline RAG helpers: fake embeddings, cosine search, chunking, hybrid fusion.

Generation still uses the Responses API (`client.responses.create`), never the
sunset Assistants API. Embeddings, when live, use `client.embeddings.create`.
Graded work uses FakeEmbedder and precomputed fixture vectors.
"""

from .chunking import Chunk, chunk_by_size, chunk_preserving_fences, chunk_structured
from .embeddings import (
    DEFAULT_DIM,
    Embedder,
    FakeEmbedder,
    get_embedder,
    token_hash_embed,
)
from .hybrid import bm25_scores, fuse_scores, hybrid_search, min_max, rerank_by_cosine
from .store import VectorIndex
from .vectors import cosine_similarity, l2_normalize, top_k

__all__ = [
    "DEFAULT_DIM",
    "Chunk",
    "Embedder",
    "FakeEmbedder",
    "VectorIndex",
    "bm25_scores",
    "chunk_by_size",
    "chunk_preserving_fences",
    "chunk_structured",
    "cosine_similarity",
    "fuse_scores",
    "get_embedder",
    "hybrid_search",
    "l2_normalize",
    "min_max",
    "rerank_by_cosine",
    "token_hash_embed",
    "top_k",
]
