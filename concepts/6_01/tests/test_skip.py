from course_kit.loader import load_concept_module

skip = load_concept_module("6_01", "skip")


def test_true_fact() -> None:
    assert skip.llm_judge_needs_calibration_before_it_is_a_gate() is True


def test_false_fact() -> None:
    assert skip.live_model_text_is_an_honest_junit_assert_equals() is False
