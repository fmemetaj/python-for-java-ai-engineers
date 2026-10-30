from course_kit.loader import load_concept_module

skip = load_concept_module("2_03", "skip")


def test_true_fact() -> None:
    assert skip.window_includes_output_tokens() is True


def test_false_fact() -> None:
    assert skip.context_window_is_unlimited() is False
