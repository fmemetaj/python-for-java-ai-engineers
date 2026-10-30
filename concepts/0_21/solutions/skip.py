"""Solutions for the 0.21 skip check."""


def needs_shared_base_class() -> bool:
    """Must two classes share a base type before a function can call the same method on both?"""
    return False


def hasattr_checks_behavior() -> bool:
    """Can you check for a method with hasattr/callable instead of instanceof?"""
    return True
