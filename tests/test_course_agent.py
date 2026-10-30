"""From-scratch agent loop, memory, trace, facade, and fake MCP."""

from __future__ import annotations

from course_kit.agent import (
    Agent,
    AgentMemory,
    AgentTrace,
    FakeMcpServer,
    Runner,
    classify_orchestration,
    mcp_tools_to_openai,
    run_agent_loop,
    should_use_agent,
)
from course_kit.llm import FakeLLM


def test_classify_and_should_use_agent() -> None:
    assert classify_orchestration(steps_known=True, model_picks_tools=False) == "workflow"
    assert classify_orchestration(steps_known=False, model_picks_tools=True) == "agent"
    assert should_use_agent(
        steps_known=False,
        model_picks_tools=True,
        branching=True,
    )


def test_memory_pins_and_trims() -> None:
    memory = AgentMemory(budget_tokens=8)
    memory.add("user", "keep", pinned=True)
    memory.add("observation", "drop-me-please-now")
    memory.add("observation", "newer-observation")
    roles = [item.role for item in memory.items]
    assert "user" in roles
    assert memory.used_tokens <= memory.budget_tokens or all(item.pinned for item in memory.items)


def test_trace_nests_and_is_non_negative() -> None:
    trace = AgentTrace(request_id="req_test")
    with trace.span("agent.run", "agent"):
        with trace.span("tool.search_docs", "tool", call_id="c1"):
            pass
    tree = trace.as_list()
    assert tree[0]["name"] == "agent.run"
    assert tree[0]["children"][0]["attributes"]["call_id"] == "c1"
    assert tree[0]["duration_ms"] >= 0.0


def test_loop_five_step_script_and_cap() -> None:
    fake = FakeLLM(
        trajectories={
            "job": [
                {
                    "tools": [
                        {
                            "call_id": "c1",
                            "name": "search_docs",
                            "arguments": '{"query":"x"}',
                        }
                    ]
                },
                {
                    "tools": [
                        {
                            "call_id": "c2",
                            "name": "search_docs",
                            "arguments": '{"query":"y"}',
                        }
                    ]
                },
                {"message": "done"},
            ]
        }
    )
    result = run_agent_loop(
        fake,
        "job",
        execute=lambda n, a: "{}",
        tools=[{"type": "function", "name": "search_docs"}],
        max_steps=8,
    )
    assert result.status == "done"
    assert result.steps == 3
    assert result.tool_names == ["search_docs", "search_docs"]

    runaway = FakeLLM(
        trajectories={
            "spin": [
                {
                    "tools": [
                        {
                            "call_id": f"c{i}",
                            "name": "search_docs",
                            "arguments": "{}",
                        }
                    ]
                }
                for i in range(10)
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


def test_facade_matches_loop() -> None:
    fake = FakeLLM(trajectories={"q": [{"message": "hello"}]})
    agent = Agent(name="x", instructions="y", tools=[])
    result = Runner().run(agent, "q", client=fake, execute=lambda n, a: "{}", max_steps=2)
    assert result.status == "done"
    assert result.output_text == "hello"


def test_fake_mcp_jsonrpc() -> None:
    server = FakeMcpServer(
        tools={"search_docs": {"description": "d", "inputSchema": {"type": "object"}}},
        handlers={"search_docs": lambda args: "ok"},
    )
    listed = server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    converted = mcp_tools_to_openai(listed["result"]["tools"])
    assert converted[0]["type"] == "function"
    called = server.handle(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "search_docs", "arguments": {}},
        }
    )
    assert called["result"]["content"][0]["text"] == "ok"
    missing = server.handle({"jsonrpc": "2.0", "id": 3, "method": "nope"})
    assert missing["error"]["code"] == -32601
