"""Solutions for the 0.3 skip check."""


def assignment_copies_a_list() -> bool:
    """Does `alias = items` copy the list?"""
    return False


def append_is_visible_through_aliases() -> bool:
    """If `alias is items`, does `items.append(1)` change `alias`?"""
    return True
