from course_kit.loader import load_concept_module

skip = load_concept_module("4_07", "skip")


def test_true_fact() -> None:
    assert skip.hybrid_combines_bm25_and_vectors() is True


def test_false_fact() -> None:
    assert skip.hosted_file_search_is_required_in_ci() is False
