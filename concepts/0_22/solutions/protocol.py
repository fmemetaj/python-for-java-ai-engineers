"""Structural Protocol for a DocsDesk retriever (solution)."""

from __future__ import annotations

from typing import Protocol


class Retriever(Protocol):
    def search(self, query: str) -> list[str]: ...


class MemoryRetriever:
    def __init__(self, docs: list[str]) -> None:
        self.docs = docs

    def search(self, query: str) -> list[str]:
        """Return docs that contain query as a substring, in order."""
        return [doc for doc in self.docs if query in doc]


def top_hit(retriever: Retriever, query: str) -> str | None:
    """First search result, or None if there are none."""
    hits = retriever.search(query)
    return hits[0] if hits else None
