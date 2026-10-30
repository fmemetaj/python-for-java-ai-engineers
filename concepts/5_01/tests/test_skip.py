from course_kit.loader import load_concept_module

skip = load_concept_module("5_01", "skip")


def test_true_fact() -> None:
    assert skip.a_workflow_is_a_path_you_wrote() is True


def test_false_fact() -> None:
    assert skip.every_tool_loop_is_an_agent() is False
