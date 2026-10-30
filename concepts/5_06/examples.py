"""Fake MCP over JSON-RPC 2.0. In-process; no sockets."""

from __future__ import annotations

from course_kit.agent.mcp import FakeMcpServer, mcp_tools_to_openai

server = FakeMcpServer(
    tools={
        "search_docs": {
            "description": "Search fixture docs",
            "inputSchema": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        }
    },
    handlers={"search_docs": lambda args: f"hit:{args.get('query')}"},
)

# Example 1 — JSON-RPC envelope for initialize.
init = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
assert init["jsonrpc"] == "2.0"
assert init["result"]["protocolVersion"] == "2025-06-18"

# Example 2 — tools/list.
listed = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
names = [tool["name"] for tool in listed["result"]["tools"]]
assert names == ["search_docs"]

# Example 3 — tools/call.
called = server.handle(
    {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "search_docs", "arguments": {"query": "refund"}},
    }
)
assert called["result"]["content"][0]["text"] == "hit:refund"

# Example 4 — unknown method is -32601.
missing = server.handle({"jsonrpc": "2.0", "id": 4, "method": "nope"})
assert missing["error"]["code"] == -32601

# Example 5 — map MCP tools to Responses function tools.
openai_tools = mcp_tools_to_openai(listed["result"]["tools"])
assert openai_tools[0]["type"] == "function"
assert openai_tools[0]["name"] == "search_docs"

print("5.6 examples ok")
