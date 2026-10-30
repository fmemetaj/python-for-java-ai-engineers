from collections.abc import Iterator

from course_kit.loader import load_concept_module

gen = load_concept_module("0_14", "generators")


def test_iter_errors_is_lazy() -> None:
    result = gen.iter_errors(["INFO ok", "ERROR disk", "ERROR timeout"])
    assert isinstance(result, Iterator)
    assert list(result) == ["ERROR disk", "ERROR timeout"]
    assert list(result) == []


def test_take() -> None:
    assert list(gen.take(0, [1, 2, 3])) == []
    assert list(gen.take(2, [1, 2, 3])) == [1, 2]


def test_replay_count_empty_second_pass() -> None:
    assert gen.replay_count(iter([1, 2, 3])) == 0
    assert gen.replay_count(gen.iter_errors(["ERROR a"])) == 0
