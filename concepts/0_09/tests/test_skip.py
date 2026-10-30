from course_kit.loader import load_concept_module

skip = load_concept_module("0_09", "skip")


def test_if_is_not_a_scope() -> None:
    assert skip.if_creates_a_new_scope() is False


def test_nonlocal_is_required() -> None:
    assert skip.nonlocal_needed_to_rebind_enclosing() is True
