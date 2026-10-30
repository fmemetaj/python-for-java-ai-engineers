"""Pick the cheaper effort when only output tokens change (solution)."""

from __future__ import annotations


def cheaper_effort(effort_a: str, tokens_a: int, effort_b: str, tokens_b: int) -> str:
    """Return the effort name with fewer billed output tokens. Tie → the first."""
    if tokens_b < tokens_a:
        return effort_b
    return effort_a
