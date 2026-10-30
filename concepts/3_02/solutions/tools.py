"""Tool definitions and function_call / function_call_output item shapes."""

from __future__ import annotations

import json
from typing import Any


def search_docs_tool() -> dict[str, Any]:
    """Responses tool: type=function, name at the top level, JSON Schema parameters."""
    return {
        "type": "function",
        "name": "search_docs",
        "description": "Search internal DocsDesk pages by keyword.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
            "additionalProperties": False,
        },
        "strict": True,
    }


def is_responses_tool(spec: dict[str, Any]) -> bool:
    """True when name sits on the tool itself, not nested under a 'function' key."""
    return spec.get("type") == "function" and "name" in spec and "function" not in spec


def parse_function_call(item: dict[str, Any]) -> dict[str, Any]:
    """Return {call_id, name, arguments} with arguments parsed from a JSON string."""
    if item.get("type") != "function_call":
        raise ValueError("expected a function_call item")
    raw = item.get("arguments", "{}")
    parsed = json.loads(str(raw))
    if not isinstance(parsed, dict):
        raise ValueError("arguments must be a JSON object")
    return {
        "call_id": str(item.get("call_id", "")),
        "name": str(item.get("name", "")),
        "arguments": parsed,
    }


def function_call_output_item(call_id: str, output: str) -> dict[str, str]:
    """Input item that returns a tool result, keyed by the model's call_id."""
    return {"type": "function_call_output", "call_id": call_id, "output": output}
