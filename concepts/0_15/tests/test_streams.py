from collections.abc import Iterator

from course_kit.loader import load_concept_module

streams = load_concept_module("0_15", "streams")

TICKETS = [
    {"id": 101, "priority": "high"},
    {"id": 102, "priority": "low"},
    {"id": 103, "priority": "high"},
]


def test_three_styles_agree() -> None:
    expected = [101, 103]
    assert streams.high_priority_ids(TICKETS) == expected
    assert streams.high_priority_ids_loop(TICKETS) == expected
    generated = streams.high_priority_ids_gen(TICKETS)
    assert isinstance(generated, Iterator)
    assert list(generated) == expected
    assert list(generated) == []


def test_empty() -> None:
    assert streams.high_priority_ids([]) == []
    assert streams.high_priority_ids_loop([]) == []
    assert list(streams.high_priority_ids_gen([])) == []
