"""Identity, value equality, and None."""


def same_identity(left: object, right: object) -> bool:
    """Return True if left and right are the same object."""
    raise NotImplementedError


def same_value(left: object, right: object) -> bool:
    """Return True if left and right compare equal."""
    raise NotImplementedError


def none_label(value: object) -> str:
    """Return 'missing' if value is None, otherwise 'present'."""
    raise NotImplementedError
