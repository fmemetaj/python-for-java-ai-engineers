from course_kit.loader import load_concept_module

readme = load_concept_module("7_07", "readme")


def test_sections() -> None:
    names = readme.readme_sections()
    for item in (
        "objective",
        "architecture",
        "how to run",
        "eval report",
        "cost report",
        "threat model",
        "limitations",
        "demo",
    ):
        assert item in names


def test_demo_minutes() -> None:
    assert readme.demo_minutes() == 5


def test_self_assessment() -> None:
    items = readme.self_assessment_items()
    blob = " ".join(items).lower()
    assert "30" in blob
    assert "citation" in blob
    assert "approval" in blob
    assert "secret" in blob
    assert len(items) >= 8
