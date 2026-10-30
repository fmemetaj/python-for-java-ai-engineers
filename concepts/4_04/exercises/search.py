"""In-memory cosine index."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


class InMemoryIndex:
    def __init__(self, *, dim: int) -> None:
        raise NotImplementedError

    def add(
        self, chunk_id: str, vector: Sequence[float], *, payload: dict[str, Any] | None = None
    ) -> None:
        raise NotImplementedError

    def search(self, query: Sequence[float], *, k: int) -> list[dict[str, Any]]:
        """Return up to k hits with keys id (or chunk_id) and score, highest cosine first."""
        raise NotImplementedError
