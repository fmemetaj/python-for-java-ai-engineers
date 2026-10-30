from course_kit.loader import load_concept_module

skip = load_concept_module("2_06", "skip")


def test_true_fact() -> None:
    assert skip.prices_come_from_dated_yaml() is True


def test_false_fact() -> None:
    assert skip.previous_response_id_waives_input_fees() is False
