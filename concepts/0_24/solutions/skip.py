"""Solutions for the 0.24 skip check."""


def python_has_checked_exceptions() -> bool:
    """Must Python methods declare checked exceptions like Java?"""
    return False


def raise_from_chains() -> bool:
    """Does `raise NewError() from exc` chain the cause (like getCause())?"""
    return True
