"""Handle tools/call and JSON-RPC method-not-found."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


def handle_call(
    request: Mapping[str, Any],
    handlers: Mapping[str, Callable[[Mapping[str, Any]], str]],
) -> dict[str, Any]:
    """Run tools/call. Unknown tool → error -32602. Return JSON-RPC result or error."""
    identifier = request.get("id")
    params = request.get("params") if isinstance(request.get("params"), dict) else {}
    name = str(params.get("name", "")) if isinstance(params, dict) else ""
    arguments = params.get("arguments") if isinstance(params, dict) else {}
    if not isinstance(arguments, dict):
        arguments = {}
    handler = handlers.get(name)
    if handler is None:
        return {
            "jsonrpc": "2.0",
            "id": identifier,
            "error": {"code": -32602, "message": f"Unknown tool {name!r}"},
        }
    text = handler(arguments)
    return {
        "jsonrpc": "2.0",
        "id": identifier,
        "result": {"content": [{"type": "text", "text": text}], "isError": False},
    }


def method_not_found(request_id: object, method: str) -> dict[str, Any]:
    """JSON-RPC error -32601."""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }
