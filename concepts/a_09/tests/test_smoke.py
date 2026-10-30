from course_kit.loader import load_concept_module
from course_kit.upgrade import SmokeCall

smoke = load_concept_module("a_09", "smoke")


def test_under_cap() -> None:
    report = smoke.capped(
        [SmokeCall("a", 0.004), SmokeCall("b", 0.004), SmokeCall("c", 0.004)],
        0.01,
    )
    assert report.ran == ("a", "b")
    assert report.skipped == ("c",)
    assert report.within_budget is True
    assert abs(report.spent_usd - 0.008) < 1e-9


def test_zero_cap_skips_all() -> None:
    report = smoke.capped([SmokeCall("a", 0.001)], 0.0)
    assert report.ran == ()
    assert report.skipped == ("a",)
