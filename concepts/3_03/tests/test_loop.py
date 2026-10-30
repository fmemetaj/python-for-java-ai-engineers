from course_kit.loader import load_concept_module

loop = load_concept_module("3_03", "loop")

CALL = {
    "type": "function_call",
    "call_id": "call_search_1",
    "name": "search_docs",
    "arguments": '{"query":"auth"}',
}


def test_loop_done_on_message_only() -> None:
    assert loop.loop_is_done([{"type": "message"}]) is True
    assert loop.loop_is_done([CALL]) is False


def test_collect_outputs_preserves_call_id() -> None:
    def execute(name: str, arguments: str) -> str:
        assert name == "search_docs"
        assert "auth" in arguments
        return "[{}]"

    outputs = loop.collect_outputs([CALL], execute)
    assert outputs == [
        {"type": "function_call_output", "call_id": "call_search_1", "output": "[{}]"}
    ]


def test_mismatched_call_id() -> None:
    outputs = [{"type": "function_call_output", "call_id": "other", "output": "x"}]
    assert loop.mismatched_call_id([CALL], outputs) == "call_search_1"
    matched = [{"type": "function_call_output", "call_id": "call_search_1", "output": "x"}]
    assert loop.mismatched_call_id([CALL], matched) is None
