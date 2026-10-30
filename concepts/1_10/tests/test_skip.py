from course_kit.loader import load_concept_module

skip = load_concept_module("1_10", "skip")


def test_default_timeout() -> None:
    assert skip.httpx_has_a_default_timeout() is True


def test_timeouts_required() -> None:
    assert skip.skipping_timeouts_is_fine_in_prod() is False
