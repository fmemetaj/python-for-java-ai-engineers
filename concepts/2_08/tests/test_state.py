from course_kit.loader import load_concept_module

state = load_concept_module("2_08", "state")


def test_running_sum() -> None:
    assert state.billed_input([100, 50, 50]) == 100 + 150 + 200
