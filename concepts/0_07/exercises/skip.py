"""2–3 minute skip check for 0.7."""


def mutable_default_is_shared() -> bool:
    """Is a default list shared across calls?"""
    raise NotImplementedError


def keyword_args_allowed() -> bool:
    """Can a caller pass greet(name='Ada', prefix='Hi')?"""
    raise NotImplementedError
