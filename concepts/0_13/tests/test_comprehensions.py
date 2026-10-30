from course_kit.loader import load_concept_module

comp = load_concept_module("0_13", "comprehensions")

ROWS = [
    {"id": 1, "level": "INFO", "message": "started"},
    {"id": 2, "level": "ERROR", "message": "disk full"},
    {"id": 3, "level": "ERROR", "message": "timeout"},
    {"id": 2, "level": "ERROR", "message": "disk full again"},
]


def test_error_messages() -> None:
    assert comp.error_messages(ROWS) == ["disk full", "timeout", "disk full again"]


def test_index_by_id_last_wins() -> None:
    index = comp.index_by_id(ROWS)
    assert index[1] == "started"
    assert index[2] == "disk full again"
    assert index[3] == "timeout"


def test_unique_levels() -> None:
    assert comp.unique_levels(ROWS) == {"INFO", "ERROR"}
