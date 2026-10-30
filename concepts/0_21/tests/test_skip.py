from course_kit.loader import load_concept_module

skip = load_concept_module("0_21", "skip")


def test_needs_shared_base_class() -> None:
    assert skip.needs_shared_base_class() is False


def test_hasattr_checks_behavior() -> None:
    assert skip.hasattr_checks_behavior() is True
