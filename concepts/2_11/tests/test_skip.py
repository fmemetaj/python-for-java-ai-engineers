from course_kit.loader import load_concept_module

skip = load_concept_module("2_11", "skip")


def test_true_fact() -> None:
    assert skip.reasoning_tokens_bill_as_output() is True


def test_false_fact() -> None:
    assert skip.short_visible_answer_means_cheap() is False
