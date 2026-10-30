from course_kit.loader import load_concept_module

skip = load_concept_module("1_07", "skip")


def test_example_ok() -> None:
    assert skip.env_example_is_safe_to_commit() is True


def test_env_not_committed() -> None:
    assert skip.env_file_with_keys_is_safe_to_commit() is False
