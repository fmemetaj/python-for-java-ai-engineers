"""Guided: remaining USD and model routing."""

from __future__ import annotations

CHEAP = "gpt-4.1-nano"
DEFAULT = "gpt-4.1-mini"


def remaining(limit_usd: float, spent_usd: float) -> float:
    """Return max(0, limit - spent). Reject negatives."""
    raise NotImplementedError


def route_model(remaining_usd: float, estimated_usd: float) -> str:
    """Return DEFAULT if remaining covers estimated, else CHEAP.

    Raise ValueError on negatives. Raise RuntimeError if remaining cannot
    cover a 0.00001 stub (the cheap floor used in this exercise).
    """
    raise NotImplementedError
