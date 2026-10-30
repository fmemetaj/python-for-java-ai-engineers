from course_kit.loader import load_concept_module

harness = load_concept_module("3_05", "harness")

CASES = [{"id": str(index), "ok": index != 3} for index in range(15)]


def test_harness_counts() -> None:
    def grader(case: dict[str, object]) -> bool:
        if case["id"] == "2":
            raise RuntimeError("boom")
        return bool(case["ok"])

    result = harness.run_harness(CASES, grader)
    assert result["total"] == 15
    assert result["passed"] + result["failed"] == 15
    assert result["failed"] >= 2
    assert result["passed"] == 13


def test_live_rate_has_no_threshold() -> None:
    line = harness.live_rate_line(12, 15)
    assert "12/15" in line
    assert "no threshold" in line.lower()
