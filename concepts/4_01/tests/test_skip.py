from course_kit.loader import load_concept_module

skip = load_concept_module("4_01", "skip")


def test_true_fact() -> None:
    assert skip.embeddings_are_dense_vectors() is True


def test_false_fact() -> None:
    assert skip.assistants_api_is_used_for_embeddings() is False
