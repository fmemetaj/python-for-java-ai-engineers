"""Tool safety: allow-list, validation, approval, idempotency. Offline."""

from __future__ import annotations

from pydantic import ValidationError

from course_kit.llm import FakeLLM
from docsdesk.tools import (
    ALLOWED_TOOLS,
    ApprovalRequiredError,
    ToolBlockedError,
    ToolRunner,
    validate_args,
)

assert "search_docs" in ALLOWED_TOOLS
assert "delete_page" not in ALLOWED_TOOLS

try:
    validate_args("search_docs", {"query": 1})
    raise AssertionError("int query must fail strict validation")
except ValidationError:
    pass

with ToolRunner() as runner:
    blocked = False
    try:
        runner.invoke("delete_page", {"slug": "auth"})
    except ToolBlockedError:
        blocked = True
    assert blocked

    runner.approved = False
    try:
        runner.invoke("delete_page", {"slug": "auth"}, approved=False)
    except (ToolBlockedError, ApprovalRequiredError):
        pass

    first = runner.invoke("search_docs", '{"query":"auth"}', idempotency_key="auth-1")
    second = runner.invoke("search_docs", '{"query":"auth"}', idempotency_key="auth-1")
    assert first == second

fake = FakeLLM(
    tool_calls={
        "bad": [
            {
                "call_id": "call_bad",
                "name": "search_docs",
                "arguments": '{"query":1}',
            }
        ]
    }
)
call = fake.complete("bad", tools=[{"type": "function", "name": "search_docs"}]).function_calls[0]
handled = ToolRunner().invoke_handled(call.name, call.arguments)
assert "error" in handled
print("3.4 examples ok")
