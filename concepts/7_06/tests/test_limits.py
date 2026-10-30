from course_kit.loader import load_concept_module

limits = load_concept_module("7_06", "limits")


def test_lists_limitations() -> None:
    good = [
        "FakeLLM cannot teach live latency.",
        "CI does not docker build or deploy.",
    ]
    assert limits.lists_limitations(good) is True
    assert limits.lists_limitations(["everything is production-ready"]) is False
    assert limits.lists_limitations(["FakeLLM is deterministic"]) is False
