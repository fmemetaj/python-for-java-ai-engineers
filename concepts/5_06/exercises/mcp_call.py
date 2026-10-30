"""Handle tools/call and JSON-RPC method-not-found."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


def handle_call(
    request: Mapping[str, Any],
    handlers: Mapping[str, Callable[[Mapping[str, Any]], str]],
) -> dict[str, Any]:
    """Run tools/call. Unknown tool → error -32602. Return JSON-RPC result or error."""
    raise NotImplementedError


def method_not_found(request_id: object, method: str) -> dict[str, Any]:
    """JSON-RPC error -32601."""
    raise NotImplementedError
