from course_kit.loader import load_concept_module

skip = load_concept_module("3_04", "skip")


def test_true_fact() -> None:
    assert skip.tool_args_must_be_validated() is True


def test_false_fact() -> None:
    assert skip.unknown_tools_should_run_anyway() is False
