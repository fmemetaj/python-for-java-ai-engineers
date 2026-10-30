from course_kit.loader import load_concept_module

skip = load_concept_module("7_06", "skip")


def test_true_fact() -> None:
    assert skip.a_threat_model_must_list_residual_risk() is True


def test_false_fact() -> None:
    assert skip.sql_injection_is_an_honest_analog_for_prompt_injection() is False
