from course_kit.loader import load_concept_module

skip = load_concept_module("0_15", "skip")


def test_no_parallel_streams() -> None:
    assert skip.stdlib_has_parallel_streams() is False


def test_comprehension_is_default() -> None:
    assert skip.comprehension_is_the_usual_stream_replacement() is True
