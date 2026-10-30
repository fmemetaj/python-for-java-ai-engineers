from course_kit.loader import load_concept_module

skip = load_concept_module("0_19", "skip")


def test_dataclass_validates_at_runtime() -> None:
    assert skip.dataclass_validates_at_runtime() is False


def test_pydantic_validates_at_runtime() -> None:
    assert skip.pydantic_validates_at_runtime() is True
