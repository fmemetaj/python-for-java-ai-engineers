from course_kit.loader import load_concept_module

skip = load_concept_module("6_04", "skip")


def test_true_fact() -> None:
    assert skip.cached_input_tokens_are_cheaper_than_uncached() is True


def test_false_fact() -> None:
    assert skip.over_budget_calls_should_still_run() is False
