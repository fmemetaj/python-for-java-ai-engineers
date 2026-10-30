from course_kit.loader import load_concept_module

skip = load_concept_module("a_06", "skip")


def test_true_fact() -> None:
    assert skip.a_decision_record_belongs_in_the_portfolio() is True


def test_false_fact() -> None:
    assert skip.vendor_chunking_is_ci_honest() is False
