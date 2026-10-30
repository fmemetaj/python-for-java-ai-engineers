from course_kit.loader import load_concept_module

skip = load_concept_module("5_06", "skip")


def test_true_fact() -> None:
    assert skip.mcp_is_json_rpc() is True


def test_false_fact() -> None:
    assert skip.mcp_requires_the_assistants_api() is False
