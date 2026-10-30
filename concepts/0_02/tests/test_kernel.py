import pytest
from course_kit.loader import load_concept_module

kernel = load_concept_module("0_02", "kernel")


def test_last_assignment_wins() -> None:
    assert kernel.last_value([("x", 1), ("x", 2), ("y", 9)], "x") == 2


def test_reads_other_names() -> None:
    tickets = ["login"]
    assert kernel.last_value([("tickets", tickets), ("n", 1)], "tickets") is tickets


def test_missing_when_cell_skipped() -> None:
    assert kernel.missing_after_partial_run(["tickets"], "client") is True
    assert kernel.missing_after_partial_run(["tickets", "client"], "client") is False


def test_last_value_unknown_name() -> None:
    with pytest.raises(KeyError):
        kernel.last_value([("x", 1)], "y")
