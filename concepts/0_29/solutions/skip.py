"""Solutions for the 0.29 skip check."""


def asyncio_speeds_up_cpu() -> bool:
    """Does asyncio.gather make a CPU-heavy Python loop finish sooner?"""
    return False


def gather_overlaps_io() -> bool:
    """Does asyncio.gather overlap waiting coroutines on one thread?"""
    return True
