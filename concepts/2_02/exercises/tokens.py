"""Course token estimator (not tiktoken)."""

from __future__ import annotations


def estimate_tokens(text: str) -> int:
    """4 characters ≈ 1 token. Empty string is 0. Non-empty is at least 1."""
    raise NotImplementedError


def whitespace_token_count(text: str) -> int:
    """How many pieces do you get if you split on whitespace?"""
    raise NotImplementedError
