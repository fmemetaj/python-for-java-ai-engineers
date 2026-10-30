from course_kit.loader import load_concept_module

types = load_concept_module("0_04", "types")


def test_identity_of_none() -> None:
    assert types.same_identity(None, None) is True


def test_distinct_lists_are_not_the_same_object() -> None:
    assert types.same_identity([1], [1]) is False
    assert types.same_value([1], [1]) is True


def test_none_label() -> None:
    assert types.none_label(None) == "missing"
    assert types.none_label("") == "present"
    assert types.none_label(0) == "present"
