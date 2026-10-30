from course_kit.loader import load_concept_module

skip = load_concept_module("1_08", "skip")


def test_plain_assert() -> None:
    assert skip.pytest_uses_plain_assert() is True


def test_fixture_names() -> None:
    assert skip.fixtures_inject_by_name() is True
