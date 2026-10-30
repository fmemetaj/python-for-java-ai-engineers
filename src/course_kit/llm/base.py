"""LLM client Protocol — a typed interface, like a Java interface for RestClient."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Usage:
    """Token accounting from a Responses-shaped payload (`response.usage`).

    Official Responses fields: `input_tokens`, `output_tokens`, `total_tokens`,
    plus `input_tokens_details.cached_tokens` and
    `output_tokens_details.reasoning_tokens`.
    https://platform.openai.com/docs/guides/migrate-to-responses
    """

    input_tokens: int
    output_tokens: int
    total_tokens: int
    cached_tokens: int = 0
    reasoning_tokens: int = 0


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
class ReasoningItem:
    """A Responses `reasoning` output item. Not visible answer text."""

    type: str = "reasoning"
    summary: tuple[str, ...] = ()
    effort: str | None = None


@dataclass(frozen=True)
class FunctionCall:
    """A Responses `function_call` output item. Arguments are a JSON string."""

    type: str = "function_call"
    call_id: str = ""
    name: str = ""
    arguments: str = ""


OutputItem = OutputMessage | ReasoningItem | FunctionCall


@dataclass(frozen=True)
class LLMResponse:
    """Subset of the OpenAI Responses object used by this course."""

    id: str
    output: tuple[OutputItem, ...]
    usage: Usage
    object: str = "response"
    previous_response_id: str | None = None
    store: bool = False
    model: str = "gpt-4.1-mini"
    refusal: str | None = None
    output_parsed: dict[str, object] | None = None

    @property
    def output_text(self) -> str:
        parts: list[str] = []
        for item in self.output:
            if item.type != "message":
                continue
            if not isinstance(item, OutputMessage):
                continue
            for block in item.content:
                if block.type == "output_text":
                    parts.append(block.text)
        return "".join(parts)

    @property
    def function_calls(self) -> tuple[FunctionCall, ...]:
        return tuple(item for item in self.output if isinstance(item, FunctionCall))


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ChatChoice:
    index: int
    message: ChatMessage
    finish_reason: str = "stop"


@dataclass(frozen=True)
class ChatUsage:
    """Chat Completions `usage` names (`prompt_tokens` / `completion_tokens`)."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass(frozen=True)
class ChatCompletion:
    """Subset of a Chat Completions object (`object: chat.completion`)."""

    id: str
    choices: tuple[ChatChoice, ...]
    usage: ChatUsage
    object: str = "chat.completion"
    model: str = "gpt-4.1-mini"


@dataclass(frozen=True)
class StreamEvent:
    """One typed Responses SSE event (not a Chat Completions `delta` chunk)."""

    type: str
    delta: str = ""
    response: LLMResponse | None = None


class LLMClient(Protocol):
    def complete(self, prompt: str, *, instructions: str = "") -> LLMResponse:
        """Return a Responses-shaped result. Implementations must not require a network."""
        ...
