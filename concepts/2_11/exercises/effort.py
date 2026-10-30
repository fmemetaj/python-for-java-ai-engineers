"""Course FakeLLM effort → reasoning tokens."""

from __future__ import annotations


def reasoning_tokens_for(effort: str | None) -> int:
    """none/None → 0, low → 16, medium → 64, high → 256. Unknown → ValueError."""
    raise NotImplementedError


def billed_output(visible_tokens: int, effort: str | None) -> int:
    """visible + reasoning tokens for that effort."""
    raise NotImplementedError
