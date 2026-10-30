from course_kit.loader import load_concept_module

skip = load_concept_module("5_02", "skip")


def test_true_fact() -> None:
    assert skip.max_steps_is_an_engineering_cap() is True


def test_false_fact() -> None:
    assert skip.the_model_executes_python_tools_itself() is False
