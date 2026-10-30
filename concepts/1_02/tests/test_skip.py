from course_kit.loader import load_concept_module

skip = load_concept_module("1_02", "skip")


def test_commit_lock() -> None:
    assert skip.lockfile_should_be_committed() is True


def test_ranges_not_in_lock() -> None:
    assert skip.ranges_live_in_the_lockfile() is False
