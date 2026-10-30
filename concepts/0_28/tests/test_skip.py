from course_kit.loader import load_concept_module

skip = load_concept_module("0_28", "skip")


def test_gil_limits_cpu_threads() -> None:
    assert skip.gil_limits_cpu_threads() is True


def test_threads_help_io() -> None:
    assert skip.threads_help_io() is True
