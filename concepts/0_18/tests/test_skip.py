from course_kit.loader import load_concept_module

skip = load_concept_module("0_18", "skip")


def test_eq_defaults_to_identity() -> None:
    assert skip.eq_defaults_to_identity() is True


def test_repr_is_for_developers() -> None:
    assert skip.repr_is_for_developers() is True
