from course_kit.loader import load_concept_module

skip = load_concept_module("7_04", "skip")


def test_true_fact() -> None:
    assert skip.capstone_eval_needs_at_least_thirty_cases() is True


def test_false_fact() -> None:
    assert skip.a_live_pass_rate_is_a_claimed_ci_threshold() is False
