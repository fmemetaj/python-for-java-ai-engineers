"""Tool definitions and function_call / function_call_output item shapes."""

from __future__ import annotations

from typing import Any


def search_docs_tool() -> dict[str, Any]:
    """Responses tool: type=function, name at the top level, JSON Schema parameters."""
    raise NotImplementedError


def is_responses_tool(spec: dict[str, Any]) -> bool:
    """True when name sits on the tool itself, not nested under a 'function' key."""
    raise NotImplementedError


def parse_function_call(item: dict[str, Any]) -> dict[str, Any]:
    """Return {call_id, name, arguments} with arguments parsed from a JSON string."""
    raise NotImplementedError


def function_call_output_item(call_id: str, output: str) -> dict[str, str]:
    """Input item that returns a tool result, keyed by the model's call_id."""
    raise NotImplementedError
