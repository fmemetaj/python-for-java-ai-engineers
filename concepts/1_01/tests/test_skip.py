from course_kit.loader import load_concept_module

skip = load_concept_module("1_01", "skip")


def test_uv_manages_both() -> None:
    assert skip.uv_manages_interpreter_and_deps() is True


def test_prefer_uv_run() -> None:
    assert skip.prefer_system_python_over_uv_run() is False
