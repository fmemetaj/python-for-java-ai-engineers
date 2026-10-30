from course_kit.loader import load_concept_module

skip = load_concept_module("3_02", "skip")


def test_true_fact() -> None:
    assert skip.responses_tools_are_internally_tagged() is True


def test_false_fact() -> None:
    assert skip.chat_tool_messages_use_call_id_items() is False
