"""2–3 minute skip check for 0.25."""


def with_always_closes() -> bool:
    """Does `with` call __exit__ even when the block raises?"""
    raise NotImplementedError


def writing_one_needs_enter_exit() -> bool:
    """Does writing a context manager mean implementing __enter__/__exit__ (or contextlib)?"""
    raise NotImplementedError
