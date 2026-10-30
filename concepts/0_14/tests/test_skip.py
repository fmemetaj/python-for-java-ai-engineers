from course_kit.loader import load_concept_module

skip = load_concept_module("0_14", "skip")


def test_generator_is_single_use() -> None:
    assert skip.generator_is_single_use() is True


def test_yield_is_lazy() -> None:
    assert skip.yield_builds_a_list_immediately() is False
