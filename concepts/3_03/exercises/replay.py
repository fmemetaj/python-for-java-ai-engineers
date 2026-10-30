"""Open exercise: replay a two-step scripted tool trajectory on FakeLLM."""

from __future__ import annotations

from collections.abc import Callable, Sequence

from course_kit.llm import FakeLLM, LLMResponse


def replay_tool_turn(
    client: FakeLLM,
    prompt: str,
    execute: Callable[[str, str], str],
    *,
    tools: Sequence[dict[str, object]] | None = None,
) -> LLMResponse:
    """complete() → if function_call items, execute them, complete() again with outputs."""
    raise NotImplementedError
