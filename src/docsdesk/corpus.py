"""Load the original Northwind Payments Spring Boot fixture (Markdown docs)."""

from __future__ import annotations

from pathlib import Path

from course_kit.loader import repo_root
from course_kit.rag import Chunk, chunk_structured

CORPUS_DIR = Path("data") / "corpus" / "payments-api"
DOC_DIR = CORPUS_DIR / "docs"


def corpus_root(path: Path | None = None) -> Path:
    return path if path is not None else repo_root() / CORPUS_DIR


def load_markdown_docs(root: Path | None = None) -> list[tuple[Path, str]]:
    docs_dir = (root if root is not None else corpus_root()) / "docs"
    files = sorted(docs_dir.glob("*.md"))
    if not files:
        raise FileNotFoundError(f"no Markdown docs in {docs_dir}")
    return [(path, path.read_text(encoding="utf-8")) for path in files]


def load_corpus_chunks(
    *,
    root: Path | None = None,
    max_chars: int = 400,
    overlap: int = 40,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    base = root if root is not None else corpus_root()
    for path, text in load_markdown_docs(base):
        relative = str(path.relative_to(base))
        chunks.extend(chunk_structured(text, max_chars=max_chars, overlap=overlap, path=relative))
    if not chunks:
        raise ValueError("corpus produced zero chunks")
    return chunks
