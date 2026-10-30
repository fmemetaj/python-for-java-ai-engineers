from course_kit.loader import load_concept_module

skip = load_concept_module("0_01", "skip")


def test_main_is_the_entry_point() -> None:
    assert skip.is_entry_point("__main__") is True


def test_imported_module_is_not_the_entry_point() -> None:
    assert skip.is_entry_point("fundamentals.log_stats") is False


def test_repl_uses_uv_run_python() -> None:
    assert skip.repl_command() == "uv run python"
