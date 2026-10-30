from course_kit.loader import load_concept_module

skip = load_concept_module("7_01", "skip")


def test_true_fact() -> None:
    assert skip.capstone_is_a_portfolio_not_a_certificate() is True


def test_false_fact() -> None:
    assert skip.paid_api_key_is_required_for_the_capstone() is False
