from course_kit.loader import load_concept_module

collections = load_concept_module("0_11", "collections")


def test_count_levels_first_seen_order() -> None:
    counts = collections.count_levels(["INFO", "ERROR", "INFO", "WARN"])
    assert counts == {"INFO": 2, "ERROR": 1, "WARN": 1}
    assert list(counts) == ["INFO", "ERROR", "WARN"]


def test_unique_in_order() -> None:
    assert collections.unique_in_order(["INFO", "ERROR", "INFO"]) == ["INFO", "ERROR"]


def test_pair_as_tuple() -> None:
    row = collections.pair_as_tuple("ERROR", 3)
    assert row == ("ERROR", 3)
    assert type(row) is tuple
