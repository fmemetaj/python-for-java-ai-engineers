"""Solutions for the 0.8 skip check."""


def star_args_is_a_tuple() -> bool:
    """Does *args collect leftover positional arguments into a tuple?"""
    return True


def kwargs_collects_named_arguments() -> bool:
    """Does **kwargs collect leftover keyword arguments into a dict?"""
    return True
