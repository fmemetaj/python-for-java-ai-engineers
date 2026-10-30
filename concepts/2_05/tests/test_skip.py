from course_kit.loader import load_concept_module

skip = load_concept_module("2_05", "skip")


def test_true_fact() -> None:
    assert skip.default_provider_is_fake() is True


def test_false_fact() -> None:
    assert skip.assistants_is_a_valid_provider() is False
