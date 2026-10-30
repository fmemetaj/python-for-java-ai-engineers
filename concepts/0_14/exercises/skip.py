"""2–3 minute skip check for 0.14."""


def generator_is_single_use() -> bool:
    """After you iterate a generator once, is a second pass empty?"""
    raise NotImplementedError


def yield_builds_a_list_immediately() -> bool:
    """Does a yield function return a finished list?"""
    raise NotImplementedError
