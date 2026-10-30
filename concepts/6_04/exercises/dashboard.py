"""Open: sum costs from log rows; compute the cached-token discount."""

from __future__ import annotations

from typing import Any


def total_cost(rows: list[dict[str, Any]]) -> float:
    """Sum the cost_usd field (missing → 0)."""
    raise NotImplementedError


def cache_discount(
    cached_tokens: int,
    input_per_million: float,
    cached_input_per_million: float,
    unit_tokens: int = 1_000_000,
) -> float:
    """USD saved versus billing cached tokens at the full input rate."""
    raise NotImplementedError
