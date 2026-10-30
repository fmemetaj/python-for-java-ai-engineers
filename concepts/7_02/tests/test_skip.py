from course_kit.loader import load_concept_module

skip = load_concept_module("7_02", "skip")


def test_true_fact() -> None:
    assert skip.docsdesk_v1_is_one_product_not_six_demos() is True


def test_false_fact() -> None:
    assert skip.optional_fastapi_must_bind_0_0_0_0_in_ci() is False
