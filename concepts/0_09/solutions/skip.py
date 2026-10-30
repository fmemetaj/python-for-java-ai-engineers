"""Solutions for the 0.9 skip check."""


def if_creates_a_new_scope() -> bool:
    """Does `if` create a block scope like Java `{ }`?"""
    return False


def nonlocal_needed_to_rebind_enclosing() -> bool:
    """Do you need `nonlocal` to rebind a name from an enclosing def?"""
    return True
