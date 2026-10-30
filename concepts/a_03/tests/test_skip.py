from course_kit.loader import load_concept_module

skip = load_concept_module("a_03", "skip")


def test_true_fact() -> None:
    assert skip.low_detail_images_cost_a_flat_token_count() is True


def test_false_fact() -> None:
    assert skip.images_are_billed_as_output_tokens() is False
