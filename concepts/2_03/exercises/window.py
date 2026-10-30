"""Context window remaining budget."""

from __future__ import annotations


def remaining_budget(window: int, input_tokens: int, reserved_output: int) -> int:
    """Return leftover input capacity. Raise ValueError if the call already overflows."""
    raise NotImplementedError


def would_overflow(window: int, token_counts: list[int], reserved_output: int) -> bool:
    """True when sum(token_counts) + reserved_output exceeds window."""
    raise NotImplementedError
