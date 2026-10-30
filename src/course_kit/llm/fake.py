"""Deterministic FakeLLM — recorded-style Responses objects, no network."""

from __future__ import annotations

from .base import LLMResponse, OutputMessage, OutputText, Usage


def _tokens(text: str) -> int:
    return max(1, len(text) // 4)


class FakeLLM:
    """Scripted or default replies. Java analogy: a `@Primary` test stub bean."""

    def __init__(self, script: dict[str, str] | None = None) -> None:
        self._script = dict(script or {})

    def complete(self, prompt: str, *, instructions: str = "") -> LLMResponse:
        text = self._script.get(prompt) or self._default_text(prompt, instructions)
        usage = Usage(
            input_tokens=_tokens(instructions + prompt),
            output_tokens=_tokens(text),
            total_tokens=_tokens(instructions + prompt) + _tokens(text),
        )
        message = OutputMessage(content=(OutputText(text=text),))
        return LLMResponse(id="resp_fake_docsdesk", output=(message,), usage=usage)

    def _default_text(self, prompt: str, instructions: str) -> str:
        lowered = f"{instructions}\n{prompt}".lower()
        if "auth" in lowered:
            return "Auth uses a Bearer token. DocsDesk never logs the token."
        if "ticket" in lowered:
            return "Tickets are fetched over HTTP with a timeout and retries."
        return "DocsDesk fake provider: offline, deterministic, no paid API."
