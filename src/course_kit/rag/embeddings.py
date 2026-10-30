"""Deterministic fake embeddings (hashing trick) and an optional live factory.

This is **not** a neural embedding model. Same text → same vector. Shared
tokens push vectors closer together than unrelated text. Live OpenAI uses
`client.embeddings.create` (Embeddings API), never Assistants, and is not
required for graded work.

Official docs: https://platform.openai.com/docs/guides/embeddings
"""

from __future__ import annotations

import hashlib
import os
import re
from typing import Protocol

import numpy as np
from numpy.typing import NDArray

DEFAULT_DIM = 64
FloatVec = NDArray[np.float64]
_TOKEN = re.compile(r"[a-z0-9]+", re.IGNORECASE)


class Embedder(Protocol):
    """Java analogy: a hashing / feature function, not Lucene's inverted index."""

    dim: int

    def embed(self, text: str) -> FloatVec: ...

    def embed_many(self, texts: list[str]) -> FloatVec: ...


def tokenize(text: str) -> list[str]:
    """Lowercased alphanumeric tokens. Introduces numpy-adjacent text features."""
    return _TOKEN.findall(text.lower())


def _features(text: str) -> list[str]:
    tokens = tokenize(text)
    feats = list(tokens)
    feats.extend(f"{left}_{right}" for left, right in zip(tokens, tokens[1:]))
    return feats


def token_hash_embed(text: str, *, dim: int = DEFAULT_DIM) -> FloatVec:
    """Feature-hashing embedder. Deterministic, offline, no native model weights.

    Each token and adjacent bigram hashes into a bucket with a ±1 sign
    (the hashing trick). The vector is L2-normalized so cosine equals a dot
    product. Empty text becomes the first standard-basis vector.
    """
    if dim < 2:
        raise ValueError("dim must be >= 2")
    vec = np.zeros(dim, dtype=np.float64)
    for feature in _features(text):
        digest = hashlib.sha256(feature.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "little") % dim
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vec[index] += sign
    norm = float(np.linalg.norm(vec))
    if norm == 0.0:
        vec[0] = 1.0
        return vec
    return vec / norm


class FakeEmbedder:
    """Offline embedder for tests, CI, and graded exercises."""

    def __init__(self, *, dim: int = DEFAULT_DIM) -> None:
        self.dim = dim

    def embed(self, text: str) -> FloatVec:
        return token_hash_embed(text, dim=self.dim)

    def embed_many(self, texts: list[str]) -> FloatVec:
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float64)
        return np.stack([self.embed(text) for text in texts])


def get_embedder(provider: str | None = None, *, dim: int = DEFAULT_DIM) -> FakeEmbedder:
    """Return an embedder. Live OpenAI is optional and never used in CI.

    Graded work: `LLM_PROVIDER=fake` (default) → FakeEmbedder.
    Optional live path: `client.embeddings.create`, not Responses, not Assistants.
    """
    name = (provider or os.environ.get("LLM_PROVIDER") or "fake").strip().lower() or "fake"
    if name == "fake":
        return FakeEmbedder(dim=dim)
    if name == "openai":
        raise RuntimeError(
            "Live embeddings are optional. Keep LLM_PROVIDER=fake for graded work. "
            "If you opt in, call client.embeddings.create "
            "(https://platform.openai.com/docs/guides/embeddings) — "
            "never the sunset Assistants API, and not client.responses.create "
            "(Responses is for generation in the RAG answer step)."
        )
    if name == "ollama":
        raise RuntimeError(
            "Ollama embeddings are an optional local path (loopback only). "
            "Keep LLM_PROVIDER=fake in CI. The FakeEmbedder is deterministic."
        )
    raise ValueError(f"Unknown LLM_PROVIDER={name!r}. Use fake, ollama, or openai.")
