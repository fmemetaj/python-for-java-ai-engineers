from course_kit.loader import load_concept_module

skip = load_concept_module("0_07", "skip")


def test_mutable_default_is_shared() -> None:
    assert skip.mutable_default_is_shared() is True


def test_keyword_args_allowed() -> None:
    assert skip.keyword_args_allowed() is True
