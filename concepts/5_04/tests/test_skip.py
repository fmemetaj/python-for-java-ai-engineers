from course_kit.loader import load_concept_module

skip = load_concept_module("5_04", "skip")


def test_true_fact() -> None:
    assert skip.an_agent_trace_is_a_span_tree() is True


def test_false_fact() -> None:
    assert skip.ci_must_export_spans_to_jaeger() is False
