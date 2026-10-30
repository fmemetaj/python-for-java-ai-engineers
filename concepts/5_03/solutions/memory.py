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
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


class WorkingMemory:
    def __init__(self, budget_tokens: int) -> None:
        self.budget_tokens = budget_tokens
        self.items: list[Item] = []

    def add(self, role: str, text: str, *, pinned: bool = False) -> Item:
        item = Item(role=role, text=text, tokens=token_count(text), pinned=pinned)
        self.items.append(item)
        self.trim()
        return item

    @property
    def used_tokens(self) -> int:
        return sum(item.tokens for item in self.items)

    def trim(self) -> None:
        while self.used_tokens > self.budget_tokens:
            index = next((i for i, item in enumerate(self.items) if not item.pinned), None)
            if index is None:
                break
            self.items.pop(index)
