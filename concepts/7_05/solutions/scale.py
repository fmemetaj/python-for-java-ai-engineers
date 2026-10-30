"""Guided: scale one request to n requests."""

from __future__ import annotations


def cost_per_n(usd_per_request: float, n: int = 100) -> float:
    """Return usd_per_request * n. Both must be >= 0."""
    if usd_per_request < 0 or n < 0:
        raise ValueError("usd_per_request and n must be >= 0")
    return usd_per_request * n
