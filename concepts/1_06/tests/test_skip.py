from course_kit.loader import load_concept_module

skip = load_concept_module("1_06", "skip")


def test_module_logger() -> None:
    assert skip.use_module_logger_not_print() is True


def test_never_log_keys() -> None:
    assert skip.log_the_api_key_at_debug() is False
