from course_kit.loader import load_concept_module

compare = load_concept_module("a_04", "compare")


def test_overlap() -> None:
    assert compare.overlap_rate(["a", "b"], ["b", "c"]) == 1 / 3
    assert compare.overlap_rate([], ["a"]) == 0.0
    assert compare.overlap_rate(["a"], ["a"]) == 1.0
