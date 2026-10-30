"""Deterministic FakeLLM — recorded-style Responses and Chat Completions objects."""

from __future__ import annotations

from collections.abc import Iterator

from .base import (
    ChatChoice,
    ChatCompletion,
    ChatMessage,
    ChatUsage,
    LLMResponse,
    OutputMessage,
    OutputText,
    ReasoningItem,
    StreamEvent,
    Usage,
)
from .tokens import estimate_tokens

EFFORT_REASONING_TOKENS = {
    None: 0,
    "none": 0,
    "low": 16,
    "medium": 64,
    "high": 256,
}


class FakeLLM:
    """Scripted or default replies. Java analogy: a `@Primary` test stub bean.

    The fake cannot teach live latency, tokenizer drift, or temperature
    variance. Graded tests check *your* parsing, cost math, and loops.
    """

    def __init__(self, script: dict[str, str] | None = None) -> None:
        self._script = dict(script or {})
        self._store: dict[str, LLMResponse] = {}
        self._counter = 0

    def complete(
        self,
        prompt: str,
        *,
        instructions: str = "",
        previous_response_id: str | None = None,
        store: bool = False,
        temperature: float = 1.0,
        reasoning_effort: str | None = None,
        model: str = "gpt-4.1-mini",
        cached_tokens: int = 0,
    ) -> LLMResponse:
        del temperature  # Fake is deterministic; live sampling is optional later.
        text = self._script.get(prompt) or self._default_text(prompt, instructions)
        prior = self._lookup(previous_response_id)
        prior_input = prior.usage.input_tokens if prior is not None else 0
        input_tokens = estimate_tokens(instructions + prompt) + prior_input
        reasoning_tokens = EFFORT_REASONING_TOKENS.get(reasoning_effort, 0)
        visible_output = estimate_tokens(text)
        output_tokens = visible_output + reasoning_tokens
        if cached_tokens > input_tokens:
            cached_tokens = input_tokens
        usage = Usage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cached_tokens=cached_tokens,
            reasoning_tokens=reasoning_tokens,
        )
        items: list[OutputMessage | ReasoningItem] = []
        if reasoning_tokens:
            items.append(ReasoningItem(effort=reasoning_effort, summary=("fake reasoning",)))
        items.append(OutputMessage(content=(OutputText(text=text),)))
        self._counter += 1
        response = LLMResponse(
            id=f"resp_fake_{self._counter:04d}",
            output=tuple(items),
            usage=usage,
            previous_response_id=previous_response_id,
            store=store,
            model=model,
        )
        if store:
            self._store[response.id] = response
        return response

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = "gpt-4.1-mini",
    ) -> ChatCompletion:
        prompt = "\n".join(item.get("content", "") for item in messages)
        instructions = next(
            (item.get("content", "") for item in messages if item.get("role") == "system"),
            "",
        )
        user = next(
            (item.get("content", "") for item in messages if item.get("role") == "user"),
            prompt,
        )
        text = self._script.get(user) or self._default_text(user, instructions)
        prompt_tokens = estimate_tokens(prompt)
        completion_tokens = estimate_tokens(text)
        self._counter += 1
        return ChatCompletion(
            id=f"chatcmpl_fake_{self._counter:04d}",
            model=model,
            choices=(ChatChoice(index=0, message=ChatMessage(role="assistant", content=text)),),
            usage=ChatUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            ),
        )

    def stream(self, prompt: str, *, instructions: str = "") -> Iterator[StreamEvent]:
        response = self.complete(prompt, instructions=instructions)
        text = response.output_text
        step = max(1, len(text) // 4)
        if not text:
            yield StreamEvent(type="response.completed", response=response)
            return
        for index in range(0, len(text), step):
            yield StreamEvent(
                type="response.output_text.delta",
                delta=text[index : index + step],
            )
        yield StreamEvent(type="response.completed", response=response)

    def _lookup(self, response_id: str | None) -> LLMResponse | None:
        if not response_id:
            return None
        return self._store.get(response_id)

    def _default_text(self, prompt: str, instructions: str) -> str:
        lowered = f"{instructions}\n{prompt}".lower()
        if "auth" in lowered:
            return "Auth uses a Bearer token. DocsDesk never logs the token."
        if "ticket" in lowered:
            return "Tickets are fetched over HTTP with a timeout and retries."
        if "population" in lowered or "follow-up" in lowered:
            return "Follow-up: the previous turn is still billed as input tokens."
        return "DocsDesk fake provider: offline, deterministic, no paid API."
