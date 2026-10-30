from course_kit.loader import load_concept_module

skip = load_concept_module("0_13", "skip")


def test_list_comp_is_eager() -> None:
    assert skip.list_comprehension_is_lazy() is False


def test_set_comp_unique() -> None:
    assert skip.set_comprehension_keeps_duplicates() is False
