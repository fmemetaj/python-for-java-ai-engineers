from course_kit.loader import load_concept_module

trim = load_concept_module("2_08", "trim")


def test_keeps_latest() -> None:
    kept = trim.trim_oldest(["aaaa", "bbbb", "ccccdddd"], budget=2)
    assert kept[-1] == "ccccdddd"
    assert "aaaa" not in kept


def test_empty() -> None:
    assert trim.trim_oldest([], budget=10) == []
