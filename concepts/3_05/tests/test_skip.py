from course_kit.loader import load_concept_module

skip = load_concept_module("3_05", "skip")


def test_true_fact() -> None:
    assert skip.evals_can_run_offline_on_fixtures() is True


def test_false_fact() -> None:
    assert skip.junit_of_a_pure_function_is_the_same_as_an_llm_eval() is False
