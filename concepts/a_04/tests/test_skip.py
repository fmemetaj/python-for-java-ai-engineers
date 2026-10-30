from course_kit.loader import load_concept_module

skip = load_concept_module("a_04", "skip")


def test_true_fact() -> None:
    assert skip.owned_rag_is_the_ci_honest_default() is True


def test_false_fact() -> None:
    assert skip.hosted_file_search_is_the_same_as_lucene() is False
