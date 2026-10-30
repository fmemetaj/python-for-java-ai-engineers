"""recall@k."""

from __future__ import annotations

from collections.abc import Sequence


def recall_at_k(retrieved: Sequence[str], gold: Sequence[str], *, k: int) -> float:
    """|gold ∩ retrieved[:k]| / |gold|. Empty gold is 0.0."""
    raise NotImplementedError
