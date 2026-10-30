from course_kit.loader import load_concept_module

skip = load_concept_module("a_09", "skip")


def test_true_fact() -> None:
    assert skip.smoke_tests_must_stop_when_the_next_call_would_exceed_the_cap() is True


def test_false_fact() -> None:
    assert skip.recorded_fixtures_may_include_live_api_keys() is False
