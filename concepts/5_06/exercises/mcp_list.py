"""Parse MCP initialize + tools/list JSON-RPC results."""

from __future__ import annotations

from typing import Any


def initialize_ok(response: dict[str, Any]) -> bool:
    """True when jsonrpc is 2.0 and result.protocolVersion is a non-empty str."""
    raise NotImplementedError


def parse_tools_list(response: dict[str, Any]) -> list[str]:
    """Return tool names from a tools/list result, in order."""
    raise NotImplementedError
