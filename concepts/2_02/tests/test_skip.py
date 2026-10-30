from course_kit.loader import load_concept_module

skip = load_concept_module("2_02", "skip")


def test_true_fact() -> None:
    assert skip.tokens_are_the_billing_unit() is True


def test_false_fact() -> None:
    assert skip.tokens_equal_whitespace_words() is False
