"""Drop oldest messages until the token budget fits."""

from __future__ import annotations


def trim_oldest(messages: list[str], *, budget: int) -> list[str]:
    """Keep the last message. Drop from the front while course tokens exceed budget."""
    raise NotImplementedError
