"""LLM client Protocol — a typed interface, like a Java interface for RestClient."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Usage:
    """Token accounting from a Responses-shaped payload (`response.usage`)."""

    input_tokens: int
    output_tokens: int
    total_tokens: int
    cached_tokens: int = 0


@dataclass(frozen=True)
class OutputText:
    type: str = "output_text"
    text: str = ""


@dataclass(frozen=True)
class OutputMessage:
    """One Responses API `message` item (a sealed-hierarchy analog)."""

    type: str = "message"
    role: str = "assistant"
    content: tuple[OutputText, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class LLMResponse:
    """Subset of the OpenAI Responses object used by this course."""

    id: str
    output: tuple[OutputMessage, ...]
    usage: Usage
    object: str = "response"

    @property
    def output_text(self) -> str:
        parts: list[str] = []
        for item in self.output:
            if item.type != "message":
                continue
            for block in item.content:
                if block.type == "output_text":
                    parts.append(block.text)
        return "".join(parts)


class LLMClient(Protocol):
    def complete(self, prompt: str, *, instructions: str = "") -> LLMResponse:
        """Return a Responses-shaped result. Implementations must not require a network."""
        ...
