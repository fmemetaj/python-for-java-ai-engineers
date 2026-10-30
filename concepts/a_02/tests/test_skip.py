from course_kit.loader import load_concept_module

skip = load_concept_module("a_02", "skip")


def test_true_fact() -> None:
    assert skip.fake_vision_reads_catalog_text_not_pixels() is True


def test_still_ties_to_fixture() -> None:
    assert skip.screenshot_answers_must_cite_the_fixture_id() is True
