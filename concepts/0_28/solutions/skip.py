"""Solutions for the 0.28 skip check."""


def gil_limits_cpu_threads() -> bool:
    """Does the GIL stop multiple Python threads from running CPU bytecode in parallel?"""
    return True


def threads_help_io() -> bool:
    """Can threads overlap waiting on I/O (sleep, HTTP, disk)?"""
    return True
