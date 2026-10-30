"""Naive size-based chunker (solution)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    start: int


def chunk_by_size(text: str, *, max_chars: int, overlap: int, path: str = "doc.md") -> list[Chunk]:
    """Windows of max_chars with overlap. Ids are '{stem}:{index}'."""
    if max_chars < 1:
        raise ValueError("max_chars")
    if overlap < 0 or overlap >= max_chars:
        raise ValueError("overlap")
    stem = path.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0] or "doc"
    if not text:
        return []
    out: list[Chunk] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        out.append(Chunk(chunk_id=f"{stem}:{len(out)}", text=text[start:end], start=start))
        if end >= len(text):
            break
        start = end - overlap
    return out
