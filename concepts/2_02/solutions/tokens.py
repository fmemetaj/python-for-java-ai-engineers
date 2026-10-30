"""Course token estimator (not tiktoken) (solution)."""

from __future__ import annotations


def estimate_tokens(text: str) -> int:
    """4 characters ≈ 1 token. Empty string is 0. Non-empty is at least 1."""
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


def whitespace_token_count(text: str) -> int:
    """How many pieces do you get if you split on whitespace?"""
    return len([part for part in text.split() if part])
