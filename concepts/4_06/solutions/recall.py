"""recall@k (solution)."""

from __future__ import annotations

from collections.abc import Sequence


def recall_at_k(retrieved: Sequence[str], gold: Sequence[str], *, k: int) -> float:
    """|gold ∩ retrieved[:k]| / |gold|. Empty gold is 0.0."""
    if not gold:
        return 0.0
    top = set(list(retrieved)[:k])
    hits = sum(1 for item in gold if item in top)
    return hits / len(gold)
