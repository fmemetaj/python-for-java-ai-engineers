from course_kit.loader import load_concept_module

skip = load_concept_module("6_06", "skip")


def test_true_fact() -> None:
    assert skip.health_endpoint_should_not_call_the_model() is True


def test_false_fact() -> None:
    assert skip.ci_must_bind_port_8000() is False
