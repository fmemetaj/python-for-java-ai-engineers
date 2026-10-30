"""Function calling: Responses tool specs and function_call items. Offline."""

from __future__ import annotations

from course_kit.llm import FakeLLM, FunctionCall, responses_create_kwargs
from docsdesk.tools import SEARCH_DOCS_TOOL, GET_ENDPOINT_SPEC_TOOL

assert SEARCH_DOCS_TOOL["type"] == "function"
assert SEARCH_DOCS_TOOL["name"] == "search_docs"
assert "function" not in SEARCH_DOCS_TOOL

body = responses_create_kwargs(
    model="gpt-4.1-mini",
    instructions="Use tools when you need docs.",
    input="Search the docs for authentication",
    tools=[SEARCH_DOCS_TOOL, GET_ENDPOINT_SPEC_TOOL],
    store=False,
)
tools = body["tools"]
assert isinstance(tools, list)
first_tool = tools[0]
assert isinstance(first_tool, dict)
assert first_tool["name"] == "search_docs"
assert "assistant_id" not in body

fake = FakeLLM(
    tool_calls={
        "Search the docs for authentication": [
            {
                "call_id": "call_search_1",
                "name": "search_docs",
                "arguments": '{"query":"auth"}',
            }
        ]
    }
)
response = fake.complete(
    "Search the docs for authentication",
    tools=[SEARCH_DOCS_TOOL],
)
assert len(response.function_calls) == 1
call: FunctionCall = response.function_calls[0]
assert call.call_id == "call_search_1"
assert call.name == "search_docs"
assert response.output_text == ""
print("3.2 examples ok")
