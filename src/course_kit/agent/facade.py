"""A thin Agent / Runner facade over the from-scratch loop.

This is *not* the OpenAI Agents SDK and not LangChain. It exists so
lesson 5.5 can compare names (Agent, Runner, tools) with Spring AI /
LangChain4j without adding a framework dependency.
https://openai.github.io/openai-agents-python/
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from course_kit.llm import FakeLLM, FunctionCall

from .loop import AgentResult, ApprovalGate, run_agent_loop
from .memory import AgentMemory
from .trace import AgentTrace


@dataclass
class Agent:
    """What a framework would call an agent: name, instructions, tool specs."""

    name: str
    instructions: str
    tools: list[dict[str, object]] = field(default_factory=list)


class Runner:
    """``Runner.run(agent, input)`` — one function that hides the loop.

    What it buys you: fewer lines at the call site. What it does not buy
    you: a different control-flow model. The loop underneath is still
    ``run_agent_loop``.
    """

    def run(
        self,
        agent: Agent,
        prompt: str,
        *,
        client: FakeLLM,
        execute: Callable[[str, str], str],
        max_steps: int = 8,
        approve: ApprovalGate = False,
        write_tools: frozenset[str] | None = None,
        memory: AgentMemory | None = None,
        trace: AgentTrace | None = None,
        text_format: dict[str, object] | None = None,
    ) -> AgentResult:
        return run_agent_loop(
            client,
            prompt,
            execute=execute,
            tools=agent.tools,
            instructions=agent.instructions,
            max_steps=max_steps,
            approve=approve,
            write_tools=write_tools,
            memory=memory,
            trace=trace,
            text_format=text_format,
        )


def function_tool(
    name: str,
    description: str,
    parameters: dict[str, object],
) -> dict[str, object]:
    """Responses-shaped tool dict. Not a decorator that talks to a network."""
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": parameters,
        "strict": True,
    }


def approval_from_flag(approved: bool) -> Callable[[FunctionCall], bool]:
    """Turn a boolean into an approval gate (tests / simulated humans)."""

    def gate(_call: FunctionCall) -> bool:
        return approved

    return gate


def framework_bought_us() -> tuple[str, ...]:
    """Honest comparison notes for the 5.5 check."""
    return (
        "call-site brevity (Runner.run)",
        "a named Agent object that bundles instructions and tools",
        "not a different loop — still your max_steps and approval gate",
    )
