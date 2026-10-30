from course_kit.loader import load_concept_module

tools = load_concept_module("3_02", "tools")


def test_search_docs_is_responses_shaped() -> None:
    spec = tools.search_docs_tool()
    assert spec["type"] == "function"
    assert spec["name"] == "search_docs"
    assert "function" not in spec
    params = spec["parameters"]
    assert params["required"] == ["query"]
    assert params["additionalProperties"] is False
    assert tools.is_responses_tool(spec) is True


def test_chat_nested_function_is_not_responses() -> None:
    nested = {
        "type": "function",
        "function": {"name": "search_docs", "parameters": {"type": "object"}},
    }
    assert tools.is_responses_tool(nested) is False


def test_parse_function_call() -> None:
    item = {
        "type": "function_call",
        "call_id": "call_search_1",
        "name": "search_docs",
        "arguments": '{"query":"auth"}',
    }
    parsed = tools.parse_function_call(item)
    assert parsed["call_id"] == "call_search_1"
    assert parsed["name"] == "search_docs"
    assert parsed["arguments"] == {"query": "auth"}


def test_output_keeps_call_id() -> None:
    item = tools.function_call_output_item("call_search_1", "[]")
    assert item["type"] == "function_call_output"
    assert item["call_id"] == "call_search_1"
    assert item["output"] == "[]"
