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
    raise NotImplementedError


def run_named(
    agent: Agent,
    prompt: str,
    *,
    run_loop: Callable[..., Any],
    max_steps: int,
) -> Any:
    """Call run_loop with prompt, tools, instructions, and max_steps."""
    raise NotImplementedError


def what_it_bought() -> tuple[str, ...]:
    """Return the honest comparison notes (see the lesson)."""
    raise NotImplementedError
