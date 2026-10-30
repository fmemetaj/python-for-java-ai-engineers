from course_kit.loader import load_concept_module

skip = load_concept_module("5_05", "skip")


def test_true_fact() -> None:
    assert skip.a_framework_hides_the_loop_not_replaces_it() is True


def test_false_fact() -> None:
    assert skip.this_course_requires_openai_agents_sdk() is False
