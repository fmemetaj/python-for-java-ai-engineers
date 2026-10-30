from course_kit.loader import load_concept_module

entry = load_concept_module("0_01", "entry")


def test_run_mode_script() -> None:
    assert entry.run_mode("__main__") == "script"


def test_run_mode_imported() -> None:
    assert entry.run_mode("hello") == "imported"


def test_banner_uses_run_mode() -> None:
    assert entry.banner("__main__", "log_stats.py") == "log_stats.py: script"
    assert entry.banner("log_stats", "log_stats.py") == "log_stats.py: imported"
