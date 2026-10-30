from course_kit.loader import load_concept_module

skip = load_concept_module("2_07", "skip")


def test_true_fact() -> None:
    assert skip.responses_uses_input_not_messages() is True


def test_false_fact() -> None:
    assert skip.assistants_api_is_current() is False
