"""2–3 minute skip check for 0.28."""


def gil_limits_cpu_threads() -> bool:
    """Does the GIL stop multiple Python threads from running CPU bytecode in parallel?"""
    raise NotImplementedError


def threads_help_io() -> bool:
    """Can threads overlap waiting on I/O (sleep, HTTP, disk)?"""
    raise NotImplementedError
