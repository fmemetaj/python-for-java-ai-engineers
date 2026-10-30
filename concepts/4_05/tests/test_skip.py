from course_kit.loader import load_concept_module

skip = load_concept_module("4_05", "skip")


def test_true_fact() -> None:
    assert skip.rag_retrieves_then_generates() is True


def test_false_fact() -> None:
    assert skip.assistants_api_is_required_for_rag() is False
