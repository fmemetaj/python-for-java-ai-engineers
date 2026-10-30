"""Agent/Runner facade over the from-scratch loop. No extra dependency."""

from __future__ import annotations

from course_kit.agent import Agent, Runner, run_agent_loop
from course_kit.agent.facade import framework_bought_us, function_tool
from course_kit.llm import FakeLLM

# Example 1 — an Agent is a bundle, not a network client.
search = function_tool(
    "search_docs",
    "Search fixture docs",
    {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
)
agent = Agent(name="triage", instructions="Investigate.", tools=[search])
assert agent.name == "triage"
assert agent.tools[0]["name"] == "search_docs"

# Example 2 — Runner.run is run_agent_loop with the bundle filled in.
fake = FakeLLM(
    trajectories={
        "q": [
            {
                "tools": [
                    {
                        "call_id": "c1",
                        "name": "search_docs",
                        "arguments": '{"query":"q"}',
                    }
                ]
            },
            {"message": "ok"},
        ]
    }
)
result = Runner().run(
    agent,
    "q",
    client=fake,
    execute=lambda n, a: "{}",
    max_steps=4,
)
assert result.status == "done"
assert result.steps == 2

# Example 3 — same loop, two call sites.
assert run_agent_loop.__name__ == "run_agent_loop"

# Example 4 — honesty: what the facade bought us.
bought = framework_bought_us()
assert any("brevity" in item for item in bought)
assert any("not a different loop" in item for item in bought)

# Example 5 — Spring AI analog is ChatClient, not RestTemplate (that was Module 2).
assert "ChatClient" != "RestTemplate"

print("5.5 examples ok")
