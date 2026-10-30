from course_kit.loader import load_concept_module

skip = load_concept_module("0_27", "skip")


def test_file_is_a_module() -> None:
    assert skip.file_is_a_module() is True


def test_init_marks_a_package() -> None:
    assert skip.init_marks_a_package() is True
