"""A 20-line Agent/Runner over a provided run_loop callable."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Agent:
    name: str
    instructions: str
    tools: list[dict[str, object]] = field(default_factory=list)


def make_agent(
    name: str,
    instructions: str,
    tools: Sequence[dict[str, object]],
) -> Agent:
    """Bundle name, instructions, and tool dicts."""
    return Agent(name=name, instructions=instructions, tools=list(tools))


def run_named(
    agent: Agent,
    prompt: str,
    *,
    run_loop: Callable[..., Any],
    max_steps: int,
) -> Any:
    """Call run_loop with prompt, tools, instructions, and max_steps."""
    return run_loop(
        prompt,
        tools=agent.tools,
        instructions=agent.instructions,
        max_steps=max_steps,
    )


def what_it_bought() -> tuple[str, ...]:
    """Return the honest comparison notes (see the lesson)."""
    return (
        "call-site brevity (Runner.run)",
        "a named Agent object that bundles instructions and tools",
        "not a different loop — still your max_steps and approval gate",
    )
