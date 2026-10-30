import pytest
from course_kit.hosted import RetrievalHit, next_hosted_turn
from course_kit.loader import load_concept_module

loop = load_concept_module("a_05", "loop")
HITS = [RetrievalHit("hosted-refund", "hosted:refunds.md", "POST /payments/{id}/refunds", 0.9)]


def test_first_is_tool() -> None:
    turn = loop.first_turn("refund?", HITS)
    assert turn.kind == "tool"
    assert turn.call is not None
    assert turn.call.type == "file_search_call"
    assert turn.call.call_id == "fs_1"


def test_second_is_message() -> None:
    turn = loop.second_turn("refund?", HITS)
    assert turn.kind == "message"
    assert "refunds" in turn.text.lower() or "POST" in turn.text
    assert "hosted-refund" in turn.citations


def test_step_two_raises() -> None:
    with pytest.raises(ValueError):
        next_hosted_turn(2, "refund?", HITS)
