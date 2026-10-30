from course_kit.loader import load_concept_module

scope = load_concept_module("0_09", "scope")


def test_counter_closes_over_start() -> None:
    counter = scope.make_counter(3)
    assert counter() == 4
    assert counter() == 5


def test_two_counters_are_independent() -> None:
    left = scope.make_counter(0)
    right = scope.make_counter(100)
    assert left() == 1
    assert right() == 101
    assert left() == 2


def test_if_does_not_hide_the_name() -> None:
    assert scope.visible_after_if(True) == "on"
    assert scope.visible_after_if(False) == "off"
