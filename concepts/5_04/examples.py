"""In-process agent spans. Offline; no collector."""

from __future__ import annotations

from course_kit.agent import AgentTrace

# Example 1 — a root span.
trace = AgentTrace(request_id="req_demo")
with trace.span("agent.run", "agent"):
    pass
assert trace.spans[0].name == "agent.run"
assert trace.spans[0].duration_ms >= 0.0

# Example 2 — nested tool span.
trace = AgentTrace()
with trace.span("agent.run", "agent"):
    with trace.span("tool.search_docs", "tool", call_id="c1"):
        pass
tree = trace.as_list()
assert tree[0]["children"][0]["name"] == "tool.search_docs"
assert tree[0]["children"][0]["attributes"]["call_id"] == "c1"

# Example 3 — request_id is the correlation key.
assert trace.request_id

# Example 4 — kinds you will see in triage.
kinds = {"agent", "llm", "tool", "approval"}
assert "tool" in kinds

# Example 5 — secrets stay out of attributes (Module 1 habit).
secret = "course-test-secret-value"
safe = AgentTrace()
with safe.span("llm.step_1", "llm", provider="fake"):
    pass
blob = str(safe.as_list())
assert secret not in blob

print("5.4 examples ok")
