from course_kit.loader import load_concept_module

report = load_concept_module("7_04", "report")


def test_merge_counts() -> None:
    assert report.merge_counts([]) == (0, 0)
    assert report.merge_counts([(18, 18), (10, 10), (4, 4)]) == (32, 32)
    assert report.merge_counts([(15, 18), (10, 10)]) == (25, 28)
