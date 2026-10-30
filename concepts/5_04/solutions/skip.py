"""Solutions for the skip check for 5.4."""


def an_agent_trace_is_a_span_tree() -> bool:
    """Is an agent trace a tree of spans for one run?"""
    return True


def ci_must_export_spans_to_jaeger() -> bool:
    """Must CI export agent spans to Jaeger or an OTel collector?"""
    return False
