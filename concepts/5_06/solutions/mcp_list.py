"""Parse MCP initialize + tools/list JSON-RPC results."""

from __future__ import annotations

from typing import Any


def initialize_ok(response: dict[str, Any]) -> bool:
    """True when jsonrpc is 2.0 and result.protocolVersion is a non-empty str."""
    if response.get("jsonrpc") != "2.0":
        return False
    result = response.get("result")
    if not isinstance(result, dict):
        return False
    version = result.get("protocolVersion")
    return isinstance(version, str) and bool(version)


def parse_tools_list(response: dict[str, Any]) -> list[str]:
    """Return tool names from a tools/list result, in order."""
    result = response.get("result")
    if not isinstance(result, dict):
        return []
    tools = result.get("tools")
    if not isinstance(tools, list):
        return []
    names: list[str] = []
    for tool in tools:
        if isinstance(tool, dict) and "name" in tool:
            names.append(str(tool["name"]))
    return names
