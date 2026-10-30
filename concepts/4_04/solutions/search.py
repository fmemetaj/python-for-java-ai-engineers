"""In-memory cosine index (solution)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from course_kit.rag.store import VectorIndex


class InMemoryIndex:
    def __init__(self, *, dim: int) -> None:
        self._inner = VectorIndex(dim=dim)

    def add(
        self, chunk_id: str, vector: Sequence[float], *, payload: dict[str, Any] | None = None
    ) -> None:
        self._inner.add(chunk_id, vector, payload=payload)

    def search(self, query: Sequence[float], *, k: int) -> list[dict[str, Any]]:
        """Return up to k hits with keys id (or chunk_id) and score, highest cosine first."""
        hits = self._inner.search(query, k=k)
        out: list[dict[str, Any]] = []
        for hit in hits:
            row = dict(hit)
            row["id"] = hit["chunk_id"]
            out.append(row)
        return out
