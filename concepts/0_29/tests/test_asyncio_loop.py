import asyncio

from course_kit.loader import load_concept_module

aio = load_concept_module("0_29", "asyncio_loop")


def test_gather_names_order() -> None:
    assert asyncio.run(aio.gather_names(["kb", "user", "ticket"])) == ["kb", "user", "ticket"]
    assert asyncio.run(aio.gather_names([])) == []


def test_fake_lookup() -> None:
    assert asyncio.run(aio.fake_lookup("docs")) == "docs"


def test_max_concurrent_overlaps() -> None:
    peak = asyncio.run(aio.max_concurrent(5))
    assert peak == 5
