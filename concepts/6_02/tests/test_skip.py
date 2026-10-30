from course_kit.loader import load_concept_module

skip = load_concept_module("6_02", "skip")


def test_true_fact() -> None:
    assert skip.every_log_line_should_carry_a_request_id() is True


def test_false_fact() -> None:
    assert skip.response_id_and_http_request_id_are_the_same_field() is False
