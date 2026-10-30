from course_kit.loader import load_concept_module

skip = load_concept_module("a_01", "skip")


def test_true_fact() -> None:
    assert skip.responses_image_items_use_input_image_type() is True


def test_false_fact() -> None:
    assert skip.graded_work_may_fetch_https_image_urls() is False
