"""Context window remaining budget (solution)."""

from __future__ import annotations


def remaining_budget(window: int, input_tokens: int, reserved_output: int) -> int:
    """Return leftover input capacity. Raise ValueError if the call already overflows."""
    if window <= 0 or input_tokens < 0 or reserved_output < 0:
        raise ValueError("window and token counts must be non-negative; window > 0")
    remaining = window - input_tokens - reserved_output
    if remaining < 0:
        raise ValueError("input plus reserved output exceeds the context window")
    return remaining


def would_overflow(window: int, token_counts: list[int], reserved_output: int) -> bool:
    """True when sum(token_counts) + reserved_output exceeds window."""
    return sum(token_counts) + reserved_output > window
