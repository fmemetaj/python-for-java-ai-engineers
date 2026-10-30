from course_kit.loader import load_concept_module

skip = load_concept_module("3_01", "skip")


def test_true_fact() -> None:
    assert skip.structured_outputs_use_json_schema() is True


def test_false_fact() -> None:
    assert skip.assistants_api_is_required_for_json() is False
