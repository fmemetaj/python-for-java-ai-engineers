from course_kit.loader import load_concept_module

skip = load_concept_module("2_10", "skip")


def test_true_fact() -> None:
    assert skip.prompts_belong_in_versioned_files() is True


def test_false_fact() -> None:
    assert skip.evals_require_a_paid_key() is False
