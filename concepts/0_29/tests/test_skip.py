from course_kit.loader import load_concept_module

skip = load_concept_module("0_29", "skip")


def test_asyncio_speeds_up_cpu() -> None:
    assert skip.asyncio_speeds_up_cpu() is False


def test_gather_overlaps_io() -> None:
    assert skip.gather_overlaps_io() is True
