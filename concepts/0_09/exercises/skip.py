"""2–3 minute skip check for 0.9."""


def if_creates_a_new_scope() -> bool:
    """Does `if` create a block scope like Java `{ }`?"""
    raise NotImplementedError


def nonlocal_needed_to_rebind_enclosing() -> bool:
    """Do you need `nonlocal` to rebind a name from an enclosing def?"""
    raise NotImplementedError
