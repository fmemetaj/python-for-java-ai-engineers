from course_kit.loader import load_concept_module
import pytest

retry = load_concept_module("1_12", "retry")


def test_should_retry() -> None:
    assert retry.should_retry(429) is True
    assert retry.should_retry(503) is True
    assert retry.should_retry(404) is False
    assert retry.should_retry(400) is False


def test_backoff() -> None:
    assert retry.backoff_seconds(0, 0.05) == 0.05
    assert retry.backoff_seconds(1, 0.05) == 0.1
    assert retry.backoff_seconds(2, 0.05) == 0.2


def test_run_with_retry_eventually_succeeds() -> None:
    calls = {"n": 0}

    def flaky() -> str:
        calls["n"] += 1
        if calls["n"] < 3:
            raise retry.TransientError("upstream")
        return "ok"

    slept: list[float] = []
    assert retry.run_with_retry(flaky, attempts=3, sleeper=slept.append) == "ok"
    assert slept == [0.05, 0.1]


def test_run_with_retry_gives_up() -> None:
    def always_fail() -> str:
        raise retry.TransientError("nope")

    with pytest.raises(retry.TransientError):
        retry.run_with_retry(always_fail, attempts=2, sleeper=lambda _d: None)
