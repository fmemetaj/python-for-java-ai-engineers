"""Solutions for the 0.15 skip check."""


def stdlib_has_parallel_streams() -> bool:
    """Does the Python standard library ship Java-style parallel streams?"""
    return False


def comprehension_is_the_usual_stream_replacement() -> bool:
    """Is a comprehension the usual replacement for a small Stream pipeline?"""
    return True
