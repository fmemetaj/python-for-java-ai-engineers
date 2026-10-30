"""Context-window helpers: remaining budget and trimming. Offline, no model."""

from __future__ import annotations

from .tokens import estimate_tokens


def remaining_budget(window: int, input_tokens: int, reserved_output: int) -> int:
    """Tokens left for more input after reserving output space.

    A context window counts input + output (+ reasoning) together.
    https://platform.openai.com/docs/guides/conversation-state
    """
    if window <= 0 or input_tokens < 0 or reserved_output < 0:
        raise ValueError("window and token counts must be non-negative; window > 0")
    remaining = window - input_tokens - reserved_output
    if remaining < 0:
        raise ValueError("input plus reserved output exceeds the context window")
    return remaining


def would_overflow(window: int, texts: list[str], reserved_output: int) -> bool:
    used = sum(estimate_tokens(text) for text in texts)
    return used + reserved_output > window


def trim_oldest(messages: list[str], *, budget: int) -> list[str]:
    """Drop oldest messages until estimate_tokens of the rest fits in budget.

    Always keeps the last message (the current user turn) even if it alone
    exceeds the budget — callers should fail that case separately.
    """
    if budget < 0:
        raise ValueError("budget must be >= 0")
    if not messages:
        return []
    kept = list(messages)
    while len(kept) > 1 and sum(estimate_tokens(item) for item in kept) > budget:
        kept.pop(0)
    return kept
