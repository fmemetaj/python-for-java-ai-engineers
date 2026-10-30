from course_kit.loader import load_concept_module

intent = load_concept_module("7_03", "intent")


def test_route_intent() -> None:
    assert intent.route_intent("How do I refund a captured payment?") == "ask"
    assert intent.route_intent("POST /payments/{id}/refunds returns 500") == "investigate"
    assert intent.route_intent("Investigate the refund incident") == "investigate"
    assert intent.route_intent("triage this outage") == "investigate"
