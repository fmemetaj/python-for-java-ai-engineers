"""Course FakeLLM effort → reasoning tokens (solution)."""

from __future__ import annotations

TABLE = {None: 0, "none": 0, "low": 16, "medium": 64, "high": 256}


def reasoning_tokens_for(effort: str | None) -> int:
    """none/None → 0, low → 16, medium → 64, high → 256. Unknown → ValueError."""
    try:
        return TABLE[effort]
    except KeyError as exc:
        raise ValueError(f"unknown effort {effort!r}") from exc


def billed_output(visible_tokens: int, effort: str | None) -> int:
    """visible + reasoning tokens for that effort."""
    if visible_tokens < 0:
        raise ValueError("visible_tokens must be >= 0")
    return visible_tokens + reasoning_tokens_for(effort)
