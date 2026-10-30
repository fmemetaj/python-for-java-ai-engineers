from course_kit.loader import load_concept_module

truthy = load_concept_module("0_05", "truthy")


def test_keep_truthy_drops_empty_and_zero() -> None:
    assert truthy.keep_truthy([0, "", None, [], {}, "ok", "0", 2]) == ["ok", "0", 2]


def test_first_present_skips_falsy() -> None:
    assert truthy.first_present(None, "", 0, "ready") == "ready"


def test_first_present_all_falsy() -> None:
    assert truthy.first_present(None, "", 0, []) is None
