from course_kit.loader import load_concept_module

skip = load_concept_module("6_05", "skip")


def test_true_fact() -> None:
    assert skip.retrieved_docs_can_carry_injected_instructions() is True


def test_false_fact() -> None:
    assert skip.prompt_injection_is_the_same_as_sql_injection() is False
