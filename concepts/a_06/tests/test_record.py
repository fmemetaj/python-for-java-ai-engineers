from course_kit.hosted import choose_stack
from course_kit.loader import load_concept_module

record = load_concept_module("a_06", "record")


def test_record_shape() -> None:
    decision = choose_stack(
        own_recall=0.8,
        hosted_available=True,
        can_export=True,
        can_eval=True,
        overlap=0.1,
    )
    payload = record.make_record(decision, {"ci_honest": True})
    assert payload["choice"] == "own"
    assert payload["api"] == "responses"
    assert payload["assistants"] is False
    assert payload["own_recall"] == 0.8
