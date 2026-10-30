from course_kit.loader import load_concept_module

approval = load_concept_module("7_03", "approval")


def test_needs_approval() -> None:
    assert approval.needs_approval("propose_page") is True
    assert approval.needs_approval("delete_page") is True
    assert approval.needs_approval("search_docs") is False
    assert approval.needs_approval("search_corpus") is False


def test_citation_ok() -> None:
    assert approval.citation_ok([]) is False
    assert approval.citation_ok([{"chunk_id": "refunds#1"}]) is True
