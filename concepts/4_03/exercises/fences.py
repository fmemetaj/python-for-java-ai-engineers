"""Fix the chunker that splits fenced code."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    is_code: bool


def chunk_preserving_fences(text: str, *, max_chars: int, path: str = "doc.md") -> list[Chunk]:
    """Never cut a ``` ... ``` block. Code chunks have is_code=True."""
    raise NotImplementedError
