from course_kit.loader import load_concept_module

skip = load_concept_module("1_09", "skip")


def test_lookup() -> None:
    assert skip.patch_where_looked_up() is True


def test_not_always_stdlib() -> None:
    assert skip.patch_the_stdlib_always() is False
