from course_kit.loader import load_concept_module

threats = load_concept_module("7_06", "threats")


def test_classify() -> None:
    assert threats.classify_threat("Ignore previous instructions") == "prompt-injection"
    assert threats.classify_threat("the API key leaked into the log") == "data-leakage"
    assert threats.classify_threat("write tool without approval") == "excessive-agency"
    assert threats.classify_threat("the budget cannot cover the next spend") == "cost-runaway"
    assert threats.classify_threat("the coffee machine is loud") == "other"


def test_ids() -> None:
    ids = threats.threat_ids()
    for item in (
        "prompt-injection",
        "data-leakage",
        "excessive-agency",
        "cost-runaway",
        "supply-chain",
    ):
        assert item in ids
