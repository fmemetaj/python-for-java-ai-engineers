"""Open exercise: replay a two-step scripted tool trajectory on FakeLLM."""

from __future__ import annotations

from collections.abc import Callable, Sequence

from course_kit.llm import FakeLLM, LLMResponse, function_call_output


def replay_tool_turn(
    client: FakeLLM,
    prompt: str,
    execute: Callable[[str, str], str],
    *,
    tools: Sequence[dict[str, object]] | None = None,
) -> LLMResponse:
    """complete() → if function_call items, execute them, complete() again with outputs."""
    first = client.complete(prompt, tools=tools)
    if not first.function_calls:
        return first
    outputs = [
        function_call_output(call.call_id, execute(call.name, call.arguments))
        for call in first.function_calls
    ]
    return client.complete(
        prompt,
        tools=tools,
        input_items=outputs,
        previous_response_id=first.id,
        store=True,
    )
