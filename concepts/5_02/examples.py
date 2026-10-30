"""Agent loop with a step cap. Offline FakeLLM trajectory."""

from __future__ import annotations

from course_kit.agent import run_agent_loop
from course_kit.llm import FakeLLM
from docsdesk.triage import INCIDENT_REFUND_500, scripted_triage_llm
from docsdesk.tools import TRIAGE_TOOL_SPECS, ToolRunner, WRITE_TOOLS, TRIAGE_ALLOWED

# Example 1 — a tiny two-turn script: one tool, then a message.
tiny = FakeLLM(
    trajectories={
        "ping": [
            {
                "tools": [
                    {
                        "call_id": "call_1",
                        "name": "search_docs",
                        "arguments": '{"query":"ping"}',
                    }
                ]
            },
            {"message": "pong"},
        ]
    }
)
executed: list[str] = []


def record(name: str, arguments: str) -> str:
    executed.append(name)
    return "{}"


result = run_agent_loop(
    tiny,
    "ping",
    execute=record,
    tools=[{"type": "function", "name": "search_docs"}],
    max_steps=4,
)
assert result.status == "done"
assert result.steps == 2
assert executed == ["search_docs"]

# Example 2 — stop reason: no function_call.
assert result.output_text == "pong"

# Example 3 — cap: a runaway script cannot exceed max_steps.
runaway = FakeLLM(
    trajectories={
        "spin": [
            {
                "tools": [
                    {
                        "call_id": f"c{i}",
                        "name": "search_docs",
                        "arguments": '{"query":"x"}',
                    }
                ]
            }
            for i in range(20)
        ]
    }
)
capped = run_agent_loop(
    runaway,
    "spin",
    execute=lambda n, a: "{}",
    tools=[{"type": "function", "name": "search_docs"}],
    max_steps=3,
)
assert capped.status == "capped"
assert capped.steps == 3

# Example 4 — approval denied does not execute the write.
denied = FakeLLM(
    trajectories={
        "write": [
            {
                "tools": [
                    {
                        "call_id": "w1",
                        "name": "propose_page",
                        "arguments": '{"slug":"x","title":"t","body":"b"}',
                    }
                ]
            }
        ]
    }
)
wrote: list[str] = []
blocked = run_agent_loop(
    denied,
    "write",
    execute=lambda n, a: wrote.append(n) or "{}",
    tools=[{"type": "function", "name": "propose_page"}],
    max_steps=4,
    approve=False,
    write_tools=frozenset({"propose_page"}),
)
assert blocked.status == "denied"
assert wrote == []

# Example 5 — DocsDesk 5-step refund-500 trajectory.
with ToolRunner(allow=TRIAGE_ALLOWED, approved=True) as runner:
    five = run_agent_loop(
        scripted_triage_llm(),
        INCIDENT_REFUND_500,
        execute=runner.invoke_handled,
        tools=list(TRIAGE_TOOL_SPECS),
        max_steps=8,
        approve=True,
        write_tools=WRITE_TOOLS,
    )
assert five.status == "done"
assert five.steps == 5
assert "propose_page" in five.tool_names

print("5.2 examples ok")
