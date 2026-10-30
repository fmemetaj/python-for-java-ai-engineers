"""Solutions for the 0.7 skip check."""


def mutable_default_is_shared() -> bool:
    """Is a default list shared across calls?"""
    return True


def keyword_args_allowed() -> bool:
    """Can a caller pass greet(name='Ada', prefix='Hi')?"""
    return True
