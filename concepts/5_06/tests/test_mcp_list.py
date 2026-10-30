from course_kit.loader import load_concept_module

mcp_list = load_concept_module("5_06", "mcp_list")


def test_initialize_ok() -> None:
    assert (
        mcp_list.initialize_ok(
            {"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2025-06-18"}}
        )
        is True
    )
    assert mcp_list.initialize_ok({"jsonrpc": "2.0", "result": {}}) is False
    assert mcp_list.initialize_ok({"jsonrpc": "1.0", "result": {"protocolVersion": "x"}}) is False


def test_parse_tools_list() -> None:
    names = mcp_list.parse_tools_list(
        {
            "jsonrpc": "2.0",
            "result": {
                "tools": [
                    {"name": "search_docs", "inputSchema": {}},
                    {"name": "get_endpoint_spec", "inputSchema": {}},
                ]
            },
        }
    )
    assert names == ["search_docs", "get_endpoint_spec"]
    assert mcp_list.parse_tools_list({"result": {}}) == []
