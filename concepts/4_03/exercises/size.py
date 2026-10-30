"""Naive size-based chunker."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    start: int


def chunk_by_size(text: str, *, max_chars: int, overlap: int, path: str = "doc.md") -> list[Chunk]:
    """Windows of max_chars with overlap. Ids are '{stem}:{index}'."""
    raise NotImplementedError
