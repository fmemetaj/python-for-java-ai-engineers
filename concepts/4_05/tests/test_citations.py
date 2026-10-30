from course_kit.loader import load_concept_module

citations = load_concept_module("4_05", "citations")


def test_drops_invented_ids() -> None:
    kept = citations.cite_only_retrieved(
        ["refunds:0", "invented:9", "payments:1"],
        ["payments:1", "refunds:0"],
    )
    assert kept == ["refunds:0", "payments:1"]


def test_empty_proposed() -> None:
    assert citations.cite_only_retrieved([], ["a:0"]) == []
