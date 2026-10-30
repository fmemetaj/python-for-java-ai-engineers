import json
from course_kit.loader import load_concept_module

observe = load_concept_module("6_02", "observe")


def test_pick_request_id() -> None:
    assert observe.pick_request_id("req_fake_0001", "req_local") == "req_fake_0001"
    assert observe.pick_request_id("", "req_local") == "req_local"
    assert observe.pick_request_id("  ", "") == "req_local"


def test_json_log_line() -> None:
    line = observe.json_log_line("docsdesk.ask", "req_fake_0001", 0.00004)
    payload = json.loads(line)
    assert payload["event"] == "docsdesk.ask"
    assert payload["request_id"] == "req_fake_0001"
    assert payload["cost_usd"] == 0.00004


def test_span_ms() -> None:
    assert observe.span_ms(10.0, 25.0) == 15.0
    assert observe.span_ms(25.0, 10.0) == 0.0
