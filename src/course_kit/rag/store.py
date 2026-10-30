"""In-memory dense vector index. Java analog: Lucene / Elasticsearch kNN.

This is a numpy matrix plus ids — brute-force cosine. A hosted vector DB
starts to pay off when the corpus no longer fits in RAM or you need filters
pushed down to the index (exactly like choosing Elasticsearch over a HashMap).
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .chunking import Chunk
from .embeddings import DEFAULT_DIM, FakeEmbedder
from .vectors import as_vector, top_k

FloatVec = NDArray[np.float64]


class VectorIndex:
    """Add (id, vector, payload) rows and search by cosine similarity."""

    def __init__(self, *, dim: int = DEFAULT_DIM) -> None:
        self.dim = dim
        self._ids: list[str] = []
        self._payloads: list[dict[str, Any]] = []
        self._matrix = np.zeros((0, dim), dtype=np.float64)

    def __len__(self) -> int:
        return len(self._ids)

    def add(
        self,
        chunk_id: str,
        vector: ArrayLike,
        *,
        payload: dict[str, Any] | None = None,
    ) -> None:
        vec = as_vector(vector)
        if vec.shape[0] != self.dim:
            raise ValueError(f"expected dim {self.dim}, got {vec.shape[0]}")
        self._ids.append(chunk_id)
        self._payloads.append(dict(payload or {}))
        self._matrix = np.vstack([self._matrix, vec.reshape(1, -1)])

    def add_chunk(self, chunk: Chunk, vector: ArrayLike) -> None:
        self.add(
            chunk.chunk_id,
            vector,
            payload={
                "text": chunk.text,
                "path": chunk.path,
                "heading": chunk.heading,
                "is_code": chunk.is_code,
                "stem": chunk.stem,
            },
        )

    def search(self, query: ArrayLike, *, k: int = 5) -> list[dict[str, Any]]:
        ranked = top_k(query, self._matrix, k=k)
        hits: list[dict[str, Any]] = []
        for index, score in ranked:
            payload = dict(self._payloads[index])
            payload["chunk_id"] = self._ids[index]
            payload["score"] = score
            hits.append(payload)
        return hits

    def dump(self) -> dict[str, Any]:
        return {
            "model": "fake-hash-v1",
            "dim": self.dim,
            "chunks": [
                {
                    "id": chunk_id,
                    "vector": self._matrix[index].tolist(),
                    **self._payloads[index],
                }
                for index, chunk_id in enumerate(self._ids)
            ],
        }

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.dump(), indent=2) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> VectorIndex:
        payload = json.loads(path.read_text(encoding="utf-8"))
        dim = int(payload["dim"])
        index = cls(dim=dim)
        for row in payload["chunks"]:
            vector = row["vector"]
            chunk_id = str(row["id"])
            extra = {key: value for key, value in row.items() if key not in {"id", "vector"}}
            index.add(chunk_id, vector, payload=extra)
        return index

    @classmethod
    def from_chunks(
        cls,
        chunks: Sequence[Chunk],
        *,
        embedder: FakeEmbedder | None = None,
        dim: int = DEFAULT_DIM,
    ) -> VectorIndex:
        hasher = embedder if embedder is not None else FakeEmbedder(dim=dim)
        index = cls(dim=hasher.dim)
        for chunk in chunks:
            index.add_chunk(chunk, hasher.embed(chunk.text))
        return index
