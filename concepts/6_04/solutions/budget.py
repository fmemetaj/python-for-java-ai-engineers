"""Guided: remaining USD and model routing."""

from __future__ import annotations

CHEAP = "gpt-4.1-nano"
DEFAULT = "gpt-4.1-mini"


def remaining(limit_usd: float, spent_usd: float) -> float:
    """Return max(0, limit - spent). Reject negatives."""
    if spent_usd < 0 or limit_usd < 0:
        raise ValueError("limit and spent must be >= 0")
    return max(0.0, limit_usd - spent_usd)


def route_model(remaining_usd: float, estimated_usd: float) -> str:
    """Return DEFAULT if remaining covers estimated, else CHEAP.

    Raise ValueError on negatives. Raise RuntimeError if remaining cannot
    cover a 0.00001 stub (the cheap floor used in this exercise).
    """
    if remaining_usd < 0 or estimated_usd < 0:
        raise ValueError("usd amounts must be >= 0")
    floor = 0.00001
    if remaining_usd < floor:
        raise RuntimeError("remaining budget cannot cover the next call")
    if remaining_usd < estimated_usd:
        return CHEAP
    return DEFAULT
