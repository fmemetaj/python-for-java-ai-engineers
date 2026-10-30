from course_kit.loader import load_concept_module

replay = load_concept_module("2_06", "replay")


def test_three_equal_turns() -> None:
    # sizes 100,100,100 → billed 100 + 200 + 300 = 600
    assert replay.billed_input_tokens([100, 100, 100], replay=True) == 600
    assert replay.billed_input_tokens([100, 100, 100], replay=False) == 600


def test_tripled() -> None:
    total = replay.billed_input_tokens([100, 100, 100], replay=True)
    assert replay.bill_tripled_because_replay(total, 100) is True
    assert replay.bill_tripled_because_replay(150, 100) is False
