from course_kit.loader import load_concept_module

skip = load_concept_module("5_03", "skip")


def test_true_fact() -> None:
    assert skip.pinned_user_incident_survives_trim() is True


def test_false_fact() -> None:
    assert skip.previous_response_id_is_free_context() is False
