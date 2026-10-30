from course_kit.loader import load_concept_module

skip = load_concept_module("2_04", "skip")


def test_true_fact() -> None:
    assert skip.temperature_scales_randomness() is True


def test_false_fact() -> None:
    assert skip.tests_should_assert_exact_live_wording() is False
