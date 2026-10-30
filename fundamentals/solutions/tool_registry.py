"""Module 0B deliverable — Protocol-typed tool registry (solution)."""

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
        return self._fn(payload)


class ToolRegistry:
    """Name → Tool map with decorator registration."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def add(self, tool: Tool) -> Tool:
        self._tools[tool.name] = tool
        return tool

    def register(self, name: str) -> Callable[[ToolFn], ToolFn]:
        def decorator(fn: ToolFn) -> ToolFn:
            self.add(FunctionTool(name, fn))
            return fn

        return decorator

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            known = ", ".join(self.names()) or "(none)"
            raise KeyError(f"unknown tool {name!r}; registered: {known}") from exc

    def names(self) -> list[str]:
        return sorted(self._tools)

    def call(self, name: str, payload: str) -> str:
        return self.get(name).run(payload)
