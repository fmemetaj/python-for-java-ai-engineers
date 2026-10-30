from course_kit.loader import load_concept_module

artifacts = load_concept_module("7_01", "artifacts")


def test_required_artifacts() -> None:
    names = artifacts.required_artifacts()
    for item in (
        "README",
        "architecture",
        "eval report",
        "cost report",
        "threat model",
        "demo",
    ):
        assert item in names
    assert len(names) >= 6
