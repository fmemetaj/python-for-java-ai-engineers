"""A budgeted working memory. Pin the incident; drop oldest observations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    role: str
    text: str
    tokens: int
    pinned: bool = False


def token_count(text: str) -> int:
    """Course rule: 4 characters ≈ 1 token. Empty string is 0."""
    raise NotImplementedError


class WorkingMemory:
    def __init__(self, budget_tokens: int) -> None:
        self.budget_tokens = budget_tokens
        self.items: list[Item] = []

    def add(self, role: str, text: str, *, pinned: bool = False) -> Item:
        raise NotImplementedError

    @property
    def used_tokens(self) -> int:
        raise NotImplementedError

    def trim(self) -> None:
        raise NotImplementedError
