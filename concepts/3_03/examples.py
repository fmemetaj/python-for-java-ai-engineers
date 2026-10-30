"""The tool-call loop, step by step. Offline FakeLLM. The model decides control flow."""

from __future__ import annotations

from course_kit.llm import FakeLLM, function_call_output
from docsdesk.loop import collect_call_outputs, run_tool_loop
from docsdesk.tools import SEARCH_DOCS_TOOL, ToolRunner

# Example 1 — a function_call is not a final answer.
fake = FakeLLM(
    tool_calls={
        "Search the docs for authentication": [
            {
                "call_id": "call_search_auth",
                "name": "search_docs",
                "arguments": '{"query":"auth"}',
            }
        ]
    },
    after_tools={
        "Search the docs for authentication": (
            '{"answer":"Clients send a Bearer token.","citations":'
            '[{"slug":"auth","quote":"Clients send a Bearer token."}],"confidence":0.9}'
        )
    },
)
first = fake.complete("Search the docs for authentication", tools=[SEARCH_DOCS_TOOL])
assert first.function_calls[0].call_id == "call_search_auth"
assert first.output_text == ""

# Example 2 — you execute the tool in *your* process.
with ToolRunner() as runner:
    outputs = collect_call_outputs(first.function_calls, runner)
assert outputs[0]["call_id"] == "call_search_auth"
output_text = str(outputs[0]["output"])
assert "auth" in output_text.lower() or output_text.startswith("[")

# Example 3 — send function_call_output with the same call_id.
assert function_call_output("call_search_auth", "ok")["type"] == "function_call_output"

# Example 4 — the second complete() yields a message (loop done).
second = fake.complete(
    "Search the docs for authentication",
    tools=[SEARCH_DOCS_TOOL],
    input_items=outputs,
    previous_response_id=first.id,
    store=True,
)
assert second.function_calls == ()
assert "Bearer" in second.output_text or "answer" in second.output_text

# Example 5 — the packaged loop stops at max_steps.
with ToolRunner() as runner:
    final = run_tool_loop(
        FakeLLM(
            tool_calls={
                "Search the docs for authentication": [
                    {
                        "call_id": "call_search_auth",
                        "name": "search_docs",
                        "arguments": '{"query":"auth"}',
                    }
                ]
            },
            after_tools={
                "Search the docs for authentication": (
                    '{"answer":"ok","citations":[{"slug":"auth","quote":"Bearer"}],'
                    '"confidence":0.5}'
                )
            },
        ),
        "Search the docs for authentication",
        runner=runner,
    )
assert final.function_calls == ()

print("3.3 examples ok")
