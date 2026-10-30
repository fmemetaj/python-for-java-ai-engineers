from course_kit.loader import load_concept_module

skip = load_concept_module("0_11", "skip")


def test_dict_order() -> None:
    assert skip.dict_preserves_insertion_order() is True


def test_missing_key_raises() -> None:
    assert skip.missing_key_with_brackets_returns_none() is False
