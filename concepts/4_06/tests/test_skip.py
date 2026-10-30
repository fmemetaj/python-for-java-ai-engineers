from course_kit.loader import load_concept_module

skip = load_concept_module("4_06", "skip")


def test_true_fact() -> None:
    assert skip.recall_at_k_measures_retrieval() is True


def test_false_fact() -> None:
    assert skip.junit_equals_on_live_prose_is_the_rag_gate() is False
