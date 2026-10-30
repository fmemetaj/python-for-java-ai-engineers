from course_kit.loader import load_concept_module

skip = load_concept_module("3_03", "skip")


def test_true_fact() -> None:
    assert skip.the_model_decides_whether_to_call_a_tool() is True


def test_false_fact() -> None:
    assert skip.outputs_can_omit_call_id() is False
