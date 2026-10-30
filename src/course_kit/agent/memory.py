"""Working memory for an agent: observations plus a token budget.

Not a database and not an HTTP session. Oldest observations drop first;
the pinned user incident is never trimmed. Token counts use the course
4-characters ≈ 1 token helper, not tiktoken.
https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens
"""

from __future__ import annotations

from dataclasses import dataclass

from course_kit.llm.tokens import estimate_tokens


@dataclass(frozen=True)
class MemoryItem:
    role: str
    text: str
    tokens: int
    pinned: bool = False


class AgentMemory:
    """A small, budgeted list of notes the loop re-sends as instructions."""

    def __init__(self, budget_tokens: int = 400) -> None:
        if budget_tokens < 1:
            raise ValueError("budget_tokens must be >= 1")
        self.budget_tokens = budget_tokens
        self.items: list[MemoryItem] = []

    def add(self, role: str, text: str, *, pinned: bool = False) -> MemoryItem:
        item = MemoryItem(
            role=role,
            text=text,
            tokens=estimate_tokens(text),
            pinned=pinned,
        )
        self.items.append(item)
        self.trim()
        return item

    @property
    def used_tokens(self) -> int:
        return sum(item.tokens for item in self.items)

    def trim(self) -> list[MemoryItem]:
        """Drop oldest unpinned items until the budget holds (or only pinned remain)."""
        dropped: list[MemoryItem] = []
        while self.used_tokens > self.budget_tokens:
            index = next(
                (i for i, item in enumerate(self.items) if not item.pinned),
                None,
            )
            if index is None:
                break
            dropped.append(self.items.pop(index))
        return dropped

    def scratchpad(self, *, max_chars: int = 240) -> str:
        """A short summary of observations — not the raw tool JSON dump."""
        observations = [item.text for item in self.items if item.role == "observation"]
        if not observations:
            return ""
        joined = " | ".join(observations)
        if len(joined) <= max_chars:
            return joined
        return joined[: max_chars - 3].rstrip() + "..."

    def as_context(self) -> str:
        lines = [f"{item.role}: {item.text}" for item in self.items]
        return "\n".join(lines)
