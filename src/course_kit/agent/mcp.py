"""Fake MCP server: JSON-RPC 2.0 initialize / tools/list / tools/call.

Official protocol: https://modelcontextprotocol.io/specification/2025-06-18
This module does not open sockets. It is an in-process fake so graded
tests stay offline. Hosted remote MCP on OpenAI is optional and paid.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

PROTOCOL_VERSION = "2025-06-18"

JsonRpc = dict[str, Any]
ToolHandler = Callable[[Mapping[str, Any]], str]


class FakeMcpServer:
    """In-memory MCP-shaped tool host. Java SPI is a misleading analog."""

    def __init__(
        self,
        tools: Mapping[str, Mapping[str, Any]],
        handlers: Mapping[str, ToolHandler] | None = None,
        *,
        name: str = "docsdesk-fake-mcp",
        version: str = "0.3.0",
    ) -> None:
        self._tools = {key: dict(value) for key, value in tools.items()}
        self._handlers = dict(handlers or {})
        self.name = name
        self.version = version
        self.initialized = False

    def handle(self, request: Mapping[str, Any]) -> JsonRpc:
        jsonrpc = request.get("jsonrpc", "2.0")
        identifier = request.get("id")
        method = request.get("method")
        params = request.get("params") if isinstance(request.get("params"), dict) else {}
        if jsonrpc != "2.0":
            return _error(identifier, -32600, "Invalid Request")
        if method == "initialize":
            self.initialized = True
            return _result(
                identifier,
                {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": self.name, "version": self.version},
                },
            )
        if method == "notifications/initialized":
            return {"jsonrpc": "2.0"}
        if method == "tools/list":
            return _result(identifier, {"tools": self.list_tools()})
        if method == "tools/call":
            name = str(params.get("name", "")) if isinstance(params, dict) else ""
            arguments = params.get("arguments") if isinstance(params, dict) else {}
            if not isinstance(arguments, dict):
                arguments = {}
            try:
                text = self.call_tool(name, arguments)
            except KeyError:
                return _error(identifier, -32602, f"Unknown tool {name!r}")
            return _result(
                identifier,
                {"content": [{"type": "text", "text": text}], "isError": False},
            )
        return _error(identifier, -32601, f"Method not found: {method}")

    def list_tools(self) -> list[dict[str, Any]]:
        listed: list[dict[str, Any]] = []
        for name, spec in self._tools.items():
            listed.append(
                {
                    "name": name,
                    "description": str(spec.get("description", "")),
                    "inputSchema": spec.get("inputSchema") or spec.get("parameters") or {},
                }
            )
        return listed

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> str:
        handler = self._handlers.get(name)
        if handler is None:
            raise KeyError(name)
        return handler(arguments)


def mcp_tools_to_openai(tools: Sequence[Mapping[str, Any]]) -> list[dict[str, object]]:
    """Map MCP tools/list entries to Responses function tools."""
    converted: list[dict[str, object]] = []
    for tool in tools:
        name = str(tool.get("name", ""))
        schema = tool.get("inputSchema") or tool.get("parameters") or {}
        converted.append(
            {
                "type": "function",
                "name": name,
                "description": str(tool.get("description", "")),
                "parameters": schema if isinstance(schema, dict) else {},
                "strict": True,
            }
        )
    return converted


def _result(identifier: object, result: object) -> JsonRpc:
    return {"jsonrpc": "2.0", "id": identifier, "result": result}


def _error(identifier: object, code: int, message: str) -> JsonRpc:
    return {"jsonrpc": "2.0", "id": identifier, "error": {"code": code, "message": message}}
