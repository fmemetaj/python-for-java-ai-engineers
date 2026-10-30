"""2–3 minute skip check for 0.29."""


def asyncio_speeds_up_cpu() -> bool:
    """Does asyncio.gather make a CPU-heavy Python loop finish sooner?"""
    raise NotImplementedError


def gather_overlaps_io() -> bool:
    """Does asyncio.gather overlap waiting coroutines on one thread?"""
    raise NotImplementedError
