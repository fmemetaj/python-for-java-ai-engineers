"""Groundedness and a chunker comparison (solution)."""

from __future__ import annotations

from collections.abc import Sequence

from course_kit.rag import Chunk, FakeEmbedder, VectorIndex, chunk_structured
from docsdesk.corpus import load_markdown_docs


def groundedness(citation_ids: Sequence[str], retrieved_ids: Sequence[str]) -> float:
    """|citations ∩ retrieved| / |citations|. Empty citations is 0.0."""
    if not citation_ids:
        return 0.0
    retrieved = set(retrieved_ids)
    return sum(1 for item in citation_ids if item in retrieved) / len(citation_ids)


def controller_hit_texts(kind: str) -> list[str]:
    """Return top-5 chunk texts for 'Which Spring annotation maps POST /payments?'."""
    docs = load_markdown_docs()
    chunks: list[Chunk] = []
    for path, text in docs:
        relative = path.name
        if kind == "naive":
            chunks.append(Chunk(chunk_id=f"{path.stem}:0", text=text[:40], path=relative))
        else:
            chunks.extend(chunk_structured(text, max_chars=400, overlap=40, path=relative))
    index = VectorIndex.from_chunks(chunks, embedder=FakeEmbedder())
    hits = index.search(
        FakeEmbedder().embed("Which Spring annotation maps POST /payments?"),
        k=5,
    )
    return [str(hit.get("text", "")) for hit in hits]
