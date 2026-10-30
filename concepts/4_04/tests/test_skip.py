from course_kit.loader import load_concept_module

skip = load_concept_module("4_04", "skip")


def test_true_fact() -> None:
    assert skip.vector_index_ranks_nearest_neighbors() is True


def test_false_fact() -> None:
    assert skip.lucene_inverted_index_stores_the_same_thing_as_a_vector_index() is False
