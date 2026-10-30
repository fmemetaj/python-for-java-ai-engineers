from course_kit.loader import load_concept_module

limits = load_concept_module("2_03", "limits")


def test_max_input() -> None:
    assert limits.max_input_for(128, 28) == 100


def test_clamp() -> None:
    assert limits.clamp_output(50, 32) == 32
    assert limits.clamp_output(-1, 32) == 0
    assert limits.clamp_output(10, 32) == 10
