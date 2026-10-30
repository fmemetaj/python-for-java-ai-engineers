"""Identity, value equality, and None (solution)."""


def same_identity(left: object, right: object) -> bool:
    """Return True if left and right are the same object."""
    return left is right


def same_value(left: object, right: object) -> bool:
    """Return True if left and right compare equal."""
    return left == right


def none_label(value: object) -> str:
    """Return 'missing' if value is None, otherwise 'present'."""
    return "missing" if value is None else "present"
