from course_kit.loader import load_concept_module

skip = load_concept_module("7_03", "skip")


def test_true_fact() -> None:
    assert skip.write_tools_need_an_approval_gate() is True


def test_false_fact() -> None:
    assert skip.rag_answers_may_omit_citations_in_v1() is False
