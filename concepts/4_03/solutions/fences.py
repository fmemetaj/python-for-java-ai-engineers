"""Fix the chunker that splits fenced code (solution)."""

from __future__ import annotations

import re
from dataclasses import dataclass

FENCE = re.compile(r"```[\w+-]*\n.*?```", re.DOTALL)


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    is_code: bool


def chunk_preserving_fences(text: str, *, max_chars: int, path: str = "doc.md") -> list[Chunk]:
    """Never cut a ``` ... ``` block. Code chunks have is_code=True."""
    stem = path.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0] or "doc"
    chunks: list[Chunk] = []
    cursor = 0
    for match in FENCE.finditer(text):
        prose = text[cursor : match.start()]
        for start in range(0, len(prose), max_chars):
            piece = prose[start : start + max_chars].strip()
            if piece:
                chunks.append(Chunk(f"{stem}:{len(chunks)}", piece, False))
        chunks.append(Chunk(f"{stem}:{len(chunks)}", match.group(0).strip("\n"), True))
        cursor = match.end()
    tail = text[cursor:].strip()
    for start in range(0, len(tail), max_chars):
        piece = tail[start : start + max_chars].strip()
        if piece:
            chunks.append(Chunk(f"{stem}:{len(chunks)}", piece, False))
    return chunks
