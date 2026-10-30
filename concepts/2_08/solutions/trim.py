"""Drop oldest messages until the token budget fits (solution)."""

from __future__ import annotations

from course_kit.llm.tokens import estimate_tokens


def trim_oldest(messages: list[str], *, budget: int) -> list[str]:
    """Keep the last message. Drop from the front while course tokens exceed budget."""
    if budget < 0:
        raise ValueError("budget must be >= 0")
    if not messages:
        return []
    kept = list(messages)
    while len(kept) > 1 and sum(estimate_tokens(item) for item in kept) > budget:
        kept.pop(0)
    return kept
