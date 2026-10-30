from course_kit.loader import load_concept_module

skip = load_concept_module("a_07", "skip")


def test_true_fact() -> None:
    assert skip.lockfile_pin_must_match_the_declared_version() is True


def test_false_fact() -> None:
    assert skip.a_maven_range_in_python_is_as_reproducible_as_uv_lock() is False
