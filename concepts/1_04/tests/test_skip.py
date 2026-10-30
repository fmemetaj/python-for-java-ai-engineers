from course_kit.loader import load_concept_module

skip = load_concept_module("1_04", "skip")


def test_src_layout() -> None:
    assert skip.src_layout_keeps_imports_clean() is True


def test_entry_points_differ() -> None:
    assert skip.console_scripts_equal_public_static_void_main() is False
