from course_kit.loader import load_concept_module

skip = load_concept_module("4_02", "skip")


def test_true_fact() -> None:
    assert skip.cosine_of_parallel_unit_vectors_is_one() is True


def test_false_fact() -> None:
    assert skip.cosine_is_the_same_as_euclidean_distance() is False
