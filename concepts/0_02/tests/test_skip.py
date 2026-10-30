from course_kit.loader import load_concept_module

skip = load_concept_module("0_02", "skip")


def test_cells_share_one_kernel() -> None:
    assert skip.cells_share_one_kernel() is True


def test_restart_clears_names() -> None:
    assert skip.restart_clears_names() is True
