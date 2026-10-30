"""Solutions for the 0.14 skip check."""


def generator_is_single_use() -> bool:
    """After you iterate a generator once, is a second pass empty?"""
    return True


def yield_builds_a_list_immediately() -> bool:
    """Does a yield function return a finished list?"""
    return False
