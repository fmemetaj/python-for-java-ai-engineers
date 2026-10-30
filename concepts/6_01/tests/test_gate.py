import pytest
from course_kit.loader import load_concept_module

gate = load_concept_module("6_01", "gate")

CASES = [
    {"id": "exact-auth", "expected_answer": "Clients send a Bearer token."},
    {"id": "exact-tickets", "expected_answer": "GET /tickets/{id} returns a ticket."},
]


def test_gate_ok() -> None:
    assert gate.gate_ok(15, 15, 1.0) is True
    assert gate.gate_ok(14, 15, 1.0) is False
    assert gate.gate_ok(12, 15, 0.8) is True


def test_gate_empty_is_not_ok() -> None:
    assert gate.gate_ok(0, 0, 1.0) is False


def test_inject_wrong_answer() -> None:
    mutated = gate.inject_wrong_answer(CASES, "exact-auth", "WRONG")
    assert mutated[0]["expected_answer"] == "WRONG"
    assert mutated[1]["expected_answer"] == "GET /tickets/{id} returns a ticket."
    assert CASES[0]["expected_answer"] == "Clients send a Bearer token."


def test_inject_unknown_id() -> None:
    with pytest.raises(KeyError):
        gate.inject_wrong_answer(CASES, "missing", "WRONG")
