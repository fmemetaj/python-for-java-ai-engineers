from course_kit.loader import load_concept_module

assemble = load_concept_module("4_05", "assemble")


def test_labels_and_budget() -> None:
    chunks = [
        {"chunk_id": "a:0", "text": "AAA"},
        {"chunk_id": "b:0", "text": "BBB"},
    ]
    text = assemble.assemble_context(chunks, budget=80)
    assert "[a:0]" in text
    assert "AAA" in text
    tiny = assemble.assemble_context(chunks, budget=12)
    assert "[a:0]" in tiny
    assert "[b:0]" not in tiny
