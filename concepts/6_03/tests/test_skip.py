from course_kit.loader import load_concept_module

skip = load_concept_module("6_03", "skip")


def test_true_fact() -> None:
    assert skip.cache_hits_must_still_honor_ttl() is True


def test_false_fact() -> None:
    assert skip.asyncio_gather_makes_cpu_work_parallel() is False
