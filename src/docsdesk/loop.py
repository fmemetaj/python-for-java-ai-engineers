"""The tool-call loop: function_call items in, function_call_output items back.

The model decides control flow. Your code only executes allow-listed tools
and always correlates results by `call_id`.
https://platform.openai.com/docs/guides/function-calling
"""

from __future__ import annotations

from collections.abc import Sequence

from course_kit.llm import (
    FakeLLM,
    FunctionCall,
    LLMResponse,
    function_call_output,
    json_schema_from_model,
    responses_text_format,
)

from .models import TypedAnswer
from .tools import TOOL_SPECS, ToolRunner

MAX_TOOL_STEPS = 4


def collect_call_outputs(
    calls: Sequence[FunctionCall],
    runner: ToolRunner,
) -> list[dict[str, object]]:
    """Run each function_call and pair the result with the same call_id."""
    outputs: list[dict[str, object]] = []
    for call in calls:
        result = runner.invoke_handled(call.name, call.arguments)
        outputs.append(function_call_output(call.call_id, result))
    return outputs


def run_tool_loop(
    client: FakeLLM,
    prompt: str,
    *,
    runner: ToolRunner,
    instructions: str = "",
    tools: Sequence[dict[str, object]] | None = None,
    max_steps: int = MAX_TOOL_STEPS,
) -> LLMResponse:
    """Repeat complete() until the model returns no function_call items."""
    spec = tools if tools is not None else list(TOOL_SPECS)
    text_format = responses_text_format("typed_answer", json_schema_from_model(TypedAnswer))
    response = client.complete(
        prompt,
        instructions=instructions,
        tools=spec,
        text_format=text_format,
        store=True,
    )
    input_items: list[dict[str, object]] = []
    steps = 0
    while response.function_calls:
        steps += 1
        if steps > max_steps:
            raise RuntimeError(f"tool loop exceeded {max_steps} steps")
        input_items.extend(collect_call_outputs(response.function_calls, runner))
        response = client.complete(
            prompt,
            instructions=instructions,
            tools=spec,
            text_format=text_format,
            input_items=input_items,
            previous_response_id=response.id,
            store=True,
        )
    return response
