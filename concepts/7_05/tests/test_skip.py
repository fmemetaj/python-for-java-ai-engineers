from course_kit.loader import load_concept_module

skip = load_concept_module("7_05", "skip")


def test_true_fact() -> None:
    assert skip.cost_report_must_state_assumptions_and_price_date() is True


def test_false_fact() -> None:
    assert skip.you_should_hard_code_usd_prices_in_the_readme() is False
