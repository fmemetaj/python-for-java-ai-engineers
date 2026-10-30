from course_kit.loader import load_concept_module

skip = load_concept_module("1_12", "skip")


def test_backoff_grows() -> None:
    assert skip.backoff_grows_between_attempts() is True


def test_not_all_4xx() -> None:
    assert skip.retry_all_4xx() is False
