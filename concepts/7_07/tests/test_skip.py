from course_kit.loader import load_concept_module

skip = load_concept_module("7_07", "skip")


def test_true_fact() -> None:
    assert skip.the_demo_is_five_minutes_and_simulated() is True


def test_false_fact() -> None:
    assert skip.the_readme_can_skip_limitations_if_evals_pass() is False
