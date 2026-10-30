from course_kit.loader import load_concept_module

flow = load_concept_module("0_06", "flow")


def test_label_status() -> None:
    assert flow.label_status(200) == "ok"
    assert flow.label_status(400) == "client"
    assert flow.label_status(404) == "client"
    assert flow.label_status(500) == "server"
    assert flow.label_status(302) == "other"


def test_sum_to() -> None:
    assert flow.sum_to(0) == 0
    assert flow.sum_to(1) == 1
    assert flow.sum_to(4) == 10


def test_first_error() -> None:
    assert flow.first_error(["INFO", "WARN", "ERROR"]) == "ERROR"
    assert flow.first_error(["INFO", "WARN"]) is None
