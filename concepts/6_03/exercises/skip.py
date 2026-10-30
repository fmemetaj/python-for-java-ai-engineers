"""2–3 minute skip check for 6.3."""


def cache_hits_must_still_honor_ttl() -> bool:
    """After a TTL expires, should the next lookup be a miss?"""
    raise NotImplementedError


def asyncio_gather_makes_cpu_work_parallel() -> bool:
    """Does asyncio.gather run CPU-bound work on multiple cores?"""
    raise NotImplementedError
