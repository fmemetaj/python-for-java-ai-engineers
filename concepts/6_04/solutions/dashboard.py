"""Open: sum costs from log rows; compute the cached-token discount."""

from __future__ import annotations

from typing import Any


def total_cost(rows: list[dict[str, Any]]) -> float:
    """Sum the cost_usd field (missing → 0)."""
    return sum(float(row.get("cost_usd") or 0.0) for row in rows)


def cache_discount(
    cached_tokens: int,
    input_per_million: float,
    cached_input_per_million: float,
    unit_tokens: int = 1_000_000,
) -> float:
    """USD saved versus billing cached tokens at the full input rate."""
    if cached_tokens < 0:
        raise ValueError("cached_tokens must be >= 0")
    return cached_tokens * (input_per_million - cached_input_per_million) / float(unit_tokens)
