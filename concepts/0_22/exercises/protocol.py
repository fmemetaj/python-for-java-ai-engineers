"""Structural Protocol for a DocsDesk retriever."""

from __future__ import annotations

from typing import Protocol


class Retriever(Protocol):
    def search(self, query: str) -> list[str]: ...


class MemoryRetriever:
    def __init__(self, docs: list[str]) -> None:
        self.docs = docs

    def search(self, query: str) -> list[str]:
        """Return docs that contain query as a substring, in order."""
        raise NotImplementedError


def top_hit(retriever: Retriever, query: str) -> str | None:
    """First search result, or None if there are none."""
    raise NotImplementedError
