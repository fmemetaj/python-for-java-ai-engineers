"""2–3 minute skip check for 0.24."""


def python_has_checked_exceptions() -> bool:
    """Must Python methods declare checked exceptions like Java?"""
    raise NotImplementedError


def raise_from_chains() -> bool:
    """Does `raise NewError() from exc` chain the cause (like getCause())?"""
    raise NotImplementedError
