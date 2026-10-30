"""Solutions for the 0.25 skip check."""


def with_always_closes() -> bool:
    """Does `with` call __exit__ even when the block raises?"""
    return True


def writing_one_needs_enter_exit() -> bool:
    """Does writing a context manager mean implementing __enter__/__exit__ (or contextlib)?"""
    return True
