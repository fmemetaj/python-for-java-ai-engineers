from course_kit.loader import load_concept_module

slicing = load_concept_module("0_12", "slicing")


def test_tail() -> None:
    source = [10, 20, 30, 40]
    result = slicing.tail(source, 2)
    assert result == [30, 40]
    result.append(99)
    assert source == [10, 20, 30, 40]


def test_tail_non_positive() -> None:
    assert slicing.tail([1, 2], 0) == []
    assert slicing.tail([1, 2], -1) == []


def test_every_other() -> None:
    assert slicing.every_other([10, 20, 30, 40, 50]) == [10, 30, 50]


def test_split_head() -> None:
    assert slicing.split_head([10]) == (10, [])
    assert slicing.split_head([10, 20, 30]) == (10, [20, 30])
