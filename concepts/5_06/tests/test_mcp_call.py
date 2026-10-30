from course_kit.loader import load_concept_module

mcp_call = load_concept_module("5_06", "mcp_call")


def test_handle_call() -> None:
    response = mcp_call.handle_call(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "search_docs", "arguments": {"query": "refund"}},
        },
        {"search_docs": lambda args: f"hit:{args['query']}"},
    )
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 3
    assert response["result"]["content"][0]["text"] == "hit:refund"


def test_unknown_tool() -> None:
    response = mcp_call.handle_call(
        {"jsonrpc": "2.0", "id": 9, "params": {"name": "shell", "arguments": {}}},
        {"search_docs": lambda args: "nope"},
    )
    assert response["error"]["code"] == -32602


def test_method_not_found() -> None:
    error = mcp_call.method_not_found(4, "nope")
    assert error["error"]["code"] == -32601
    assert error["id"] == 4
    assert "nope" in error["error"]["message"]
