from course_kit.loader import load_concept_module

skip = load_concept_module("4_03", "skip")


def test_true_fact() -> None:
    assert skip.chunking_is_more_than_substring() is True


def test_false_fact() -> None:
    assert skip.one_file_must_be_one_chunk() is False
