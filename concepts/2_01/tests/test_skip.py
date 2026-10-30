from course_kit.loader import load_concept_module

skip = load_concept_module("2_01", "skip")


def test_true_fact() -> None:
    assert skip.sdk_is_configured_from_env() is True


def test_false_fact() -> None:
    assert skip.assistants_api_is_the_current_api() is False
