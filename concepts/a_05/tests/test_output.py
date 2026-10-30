from course_kit.hosted import RetrievalHit
from course_kit.loader import load_concept_module

output = load_concept_module("a_05", "output")
HITS = [RetrievalHit("hosted-refund", "hosted:refunds.md", "POST refunds", 0.9)]


def test_two_steps() -> None:
    turns = output.run_two_steps("refund?", HITS)
    assert [turn.kind for turn in turns] == ["tool", "message"]
    assert output.citation_line(turns[1]) == "cited: hosted-refund"
    assert output.citation_line(turns[0]) == "cited: none"
