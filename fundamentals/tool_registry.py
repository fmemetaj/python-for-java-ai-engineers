"""Module 0B deliverable — Protocol-typed tool registry (starter).

Fill this in after concepts 0.16–0.29. Grade with:

    uv run pytest fundamentals/test_tool_registry.py
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, runtime_checkable

ToolFn = Callable[[str], str]


@runtime_checkable
class Tool(Protocol):
    """Anything with a ``name`` and a ``run(payload) -> str`` method."""

    name: str

    def run(self, payload: str) -> str: ...


class FunctionTool:
    """Adapt a ``(str) -> str`` function to the Tool protocol."""

    def __init__(self, name: str, fn: ToolFn) -> None:
        self.name = name
        self._fn = fn

    def run(self, payload: str) -> str:
        raise NotImplementedError


class ToolRegistry:
    """Name → Tool map with decorator registration."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def add(self, tool: Tool) -> Tool:
        raise NotImplementedError

    def register(self, name: str) -> Callable[[ToolFn], ToolFn]:
        raise NotImplementedError

    def get(self, name: str) -> Tool:
        raise NotImplementedError

    def names(self) -> list[str]:
        raise NotImplementedError

    def call(self, name: str, payload: str) -> str:
        raise NotImplementedError
