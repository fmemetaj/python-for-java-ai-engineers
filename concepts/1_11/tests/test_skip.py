from course_kit.loader import load_concept_module

skip = load_concept_module("1_11", "skip")


def test_pydantic_runtime() -> None:
    assert skip.pydantic_validates_at_runtime() is True


def test_hints_not_enough() -> None:
    assert skip.type_hints_alone_validate_json() is False
