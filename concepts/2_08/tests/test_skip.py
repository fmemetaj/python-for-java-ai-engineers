from course_kit.loader import load_concept_module

skip = load_concept_module("2_08", "skip")


def test_true_fact() -> None:
    assert skip.stored_state_still_bills_input() is True


def test_false_fact() -> None:
    assert skip.http_session_means_free_tokens() is False
