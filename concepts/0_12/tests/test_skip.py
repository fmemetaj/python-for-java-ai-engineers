from course_kit.loader import load_concept_module

skip = load_concept_module("0_12", "skip")


def test_slice_excludes_stop() -> None:
    assert skip.slice_includes_the_stop_index() is False


def test_slice_copies() -> None:
    assert skip.list_slice_copies() is True
