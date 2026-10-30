from course_kit.loader import load_concept_module

first_class = load_concept_module("0_10", "first_class")


def test_apply_each() -> None:
    assert first_class.apply_each(lambda x: x + 1, [10, 20]) == [11, 21]


def test_sort_by_length() -> None:
    assert first_class.sort_by_length(["login", "api", "ok"]) == ["ok", "api", "login"]


def test_make_adder() -> None:
    add_three = first_class.make_adder(3)
    assert add_three(4) == 7
    assert first_class.make_adder(0)(9) == 9
