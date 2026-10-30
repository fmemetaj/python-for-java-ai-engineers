from course_kit.loader import load_concept_module

grounded = load_concept_module("4_06", "grounded")


def test_groundedness() -> None:
    assert grounded.groundedness(["a:0"], ["a:0", "b:1"]) == 1.0
    assert grounded.groundedness(["invented"], ["a:0"]) == 0.0
    assert grounded.groundedness([], ["a:0"]) == 0.0


def test_structured_beats_naive_on_controller() -> None:
    naive = grounded.controller_hit_texts("naive")
    structured = grounded.controller_hit_texts("structured")
    assert any("@PostMapping" in text for text in structured)
    assert not any("@PostMapping" in text for text in naive)
