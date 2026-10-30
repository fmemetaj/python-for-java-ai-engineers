from course_kit.loader import load_concept_module

skip = load_concept_module("0_08", "skip")


def test_star_args_is_a_tuple() -> None:
    assert skip.star_args_is_a_tuple() is True


def test_kwargs_collects_named_arguments() -> None:
    assert skip.kwargs_collects_named_arguments() is True
