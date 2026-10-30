"""Split docs into retrieval units. Size-based vs structure-aware (Markdown/Javadoc).

A chunker that cuts every N characters will bisect fenced code and headings.
Structure-aware chunking keeps fences atomic and splits on Markdown headings.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
FENCE = re.compile(r"```[\w+-]*\n.*?```", re.DOTALL)


@dataclass(frozen=True)
class Chunk:
    """One retrieval unit plus metadata (path, heading, whether it is code)."""

    chunk_id: str
    text: str
    path: str = ""
    heading: str = ""
    start: int = 0
    is_code: bool = False
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def stem(self) -> str:
        name = self.path.replace("\\", "/").rsplit("/", 1)[-1]
        return name.rsplit(".", 1)[0] if name else self.chunk_id.split(":", 1)[0]


def _pack_windows(text: str, max_chars: int, overlap: int) -> list[tuple[int, str]]:
    if max_chars < 1:
        raise ValueError("max_chars must be >= 1")
    if overlap < 0 or overlap >= max_chars:
        raise ValueError("overlap must be >= 0 and < max_chars")
    if not text:
        return []
    out: list[tuple[int, str]] = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + max_chars, length)
        out.append((start, text[start:end]))
        if end >= length:
            break
        start = end - overlap
    return out


def chunk_by_size(
    text: str,
    *,
    max_chars: int = 240,
    overlap: int = 40,
    path: str = "",
) -> list[Chunk]:
    """Naive character windows. Splits code fences — that is the bug 4.3 fixes."""
    stem = path.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0] or "doc"
    chunks: list[Chunk] = []
    for index, (start, piece) in enumerate(_pack_windows(text, max_chars, overlap)):
        chunks.append(
            Chunk(
                chunk_id=f"{stem}:{index}",
                text=piece,
                path=path,
                start=start,
            )
        )
    return chunks


def _fence_spans(text: str) -> list[tuple[int, int]]:
    return [(match.start(), match.end()) for match in FENCE.finditer(text)]


def _inside_fence(index: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= index < end for start, end in spans)


def chunk_preserving_fences(
    text: str,
    *,
    max_chars: int = 240,
    overlap: int = 40,
    path: str = "",
) -> list[Chunk]:
    """Size windows that never cut a fenced code block in half."""
    stem = path.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0] or "doc"
    spans = _fence_spans(text)
    pieces: list[tuple[int, str, bool]] = []
    cursor = 0
    for start, end in spans:
        if cursor < start:
            pieces.append((cursor, text[cursor:start], False))
        pieces.append((start, text[start:end], True))
        cursor = end
    if cursor < len(text):
        pieces.append((cursor, text[cursor:], False))

    chunks: list[Chunk] = []
    for offset, piece, is_code in pieces:
        if is_code:
            chunks.append(
                Chunk(
                    chunk_id=f"{stem}:{len(chunks)}",
                    text=piece.strip("\n"),
                    path=path,
                    start=offset,
                    is_code=True,
                )
            )
            continue
        for rel_start, window in _pack_windows(piece, max_chars, overlap):
            stripped = window.strip()
            if not stripped:
                continue
            chunks.append(
                Chunk(
                    chunk_id=f"{stem}:{len(chunks)}",
                    text=stripped,
                    path=path,
                    start=offset + rel_start,
                    is_code=False,
                )
            )
    return chunks


def chunk_structured(
    text: str,
    *,
    max_chars: int = 400,
    overlap: int = 40,
    path: str = "",
) -> list[Chunk]:
    """Split on Markdown headings, keep fences atomic, pack remaining prose."""
    stem = path.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0] or "doc"
    spans = _fence_spans(text)
    headings = [
        match for match in HEADING.finditer(text) if not _inside_fence(match.start(), spans)
    ]
    bounds: list[tuple[int, str]] = [(0, "")]
    for match in headings:
        bounds.append((match.start(), match.group(2).strip()))
    bounds.append((len(text), ""))

    chunks: list[Chunk] = []
    for index, (start, heading) in enumerate(bounds[:-1]):
        end = bounds[index + 1][0]
        section = text[start:end]
        if not section.strip():
            continue
        for piece in chunk_preserving_fences(
            section, max_chars=max_chars, overlap=overlap, path=path
        ):
            chunks.append(
                Chunk(
                    chunk_id=f"{stem}:{len(chunks)}",
                    text=piece.text,
                    path=path,
                    heading=heading or piece.heading,
                    start=start + piece.start,
                    is_code=piece.is_code,
                    metadata={"heading": heading} if heading else {},
                )
            )
    return chunks
