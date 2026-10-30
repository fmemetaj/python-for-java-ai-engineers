from course_kit.loader import load_concept_module

skip = load_concept_module("0_10", "skip")


def test_lambda_is_one_expression() -> None:
    assert skip.lambda_can_contain_a_for_loop() is False


def test_functions_are_values() -> None:
    assert skip.functions_are_values() is True
