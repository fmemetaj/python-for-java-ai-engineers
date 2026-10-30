import pytest
from course_kit.loader import load_concept_module

dec = load_concept_module("0_26", "decorators")


def test_timed_returns_result_and_duration() -> None:
    @dec.timed
    def add(left: int, right: int) -> int:
        return left + right

    result, seconds = add(2, 3)
    assert result == 5
    assert seconds >= 0
    assert add.__name__ == "add"


def test_retry_eventually_succeeds() -> None:
    attempts = {"n": 0}

    @dec.retry(3)
    def flaky() -> str:
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise RuntimeError("not yet")
        return "ok"

    assert flaky() == "ok"
    assert attempts["n"] == 3


def test_retry_gives_up() -> None:
    @dec.retry(2)
    def always() -> str:
        raise ValueError("nope")

    with pytest.raises(ValueError, match="nope"):
        always()
