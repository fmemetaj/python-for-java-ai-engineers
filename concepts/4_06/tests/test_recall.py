from course_kit.loader import load_concept_module

recall = load_concept_module("4_06", "recall")


def test_perfect_and_miss() -> None:
    assert recall.recall_at_k(["refunds", "payments"], ["refunds"], k=5) == 1.0
    assert recall.recall_at_k(["payments"], ["refunds"], k=5) == 0.0


def test_partial_and_k_cutoff() -> None:
    assert recall.recall_at_k(["a"], ["a", "b"], k=5) == 0.5
    assert recall.recall_at_k(["noise", "hit"], ["hit"], k=1) == 0.0


def test_empty_gold() -> None:
    assert recall.recall_at_k(["a"], [], k=5) == 0.0
