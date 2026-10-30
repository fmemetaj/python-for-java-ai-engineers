"""Groundedness and a chunker comparison."""

from __future__ import annotations

from collections.abc import Sequence


def groundedness(citation_ids: Sequence[str], retrieved_ids: Sequence[str]) -> float:
    """|citations ∩ retrieved| / |citations|. Empty citations is 0.0."""
    raise NotImplementedError


def controller_hit_texts(kind: str) -> list[str]:
    """Return top-5 chunk texts for 'Which Spring annotation maps POST /payments?'.

    kind='naive': one 40-character prefix per file (drops the Java fence).
    kind='structured': DocsDesk structure-aware chunks (keeps the fence).
    """
    raise NotImplementedError
