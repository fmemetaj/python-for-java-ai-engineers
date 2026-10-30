import pytest
from course_kit.loader import load_concept_module

judge = load_concept_module("6_01", "judge")


def test_verdict_passes() -> None:
    assert judge.verdict_passes(5, 4) is True
    assert judge.verdict_passes(4, 4) is True
    assert judge.verdict_passes(3, 4) is False


def test_agreement_rate() -> None:
    predicted = [True, True, False, True]
    labeled = [True, False, False, True]
    assert judge.agreement_rate(predicted, labeled) == 0.75


def test_agreement_rejects_length_mismatch() -> None:
    with pytest.raises(ValueError):
        judge.agreement_rate([True], [True, False])
