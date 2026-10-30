from course_kit.loader import load_concept_module

trace_mod = load_concept_module("5_04", "trace")


class Clock:
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        current = self.t
        self.t += 5.0
        return current


def test_duration() -> None:
    clock = Clock()
    tree = trace_mod.Trace(clock, request_id="r1")
    span = tree.start_span("llm.step_1", "llm")
    tree.end_span(span)
    assert span.duration_ms == 5.0
    assert tree.request_id == "r1"


def test_nesting_and_as_list() -> None:
    clock = Clock()
    tree = trace_mod.Trace(clock)
    root = tree.start_span("agent.run", "agent")
    child = tree.start_span("tool.search_docs", "tool", call_id="c1")
    tree.end_span(child)
    tree.end_span(root)
    payload = tree.as_list()
    assert payload[0]["name"] == "agent.run"
    assert payload[0]["children"][0]["name"] == "tool.search_docs"
    assert payload[0]["children"][0]["attributes"]["call_id"] == "c1"
    assert payload[0]["duration_ms"] == 15.0
