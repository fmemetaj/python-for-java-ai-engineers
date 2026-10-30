"""Solutions for the 1.11 skip check."""


def pydantic_validates_at_runtime() -> bool:
    """Does Pydantic validate JSON at runtime (unlike dataclass type hints)?"""
    return True


def type_hints_alone_validate_json() -> bool:
    """Do `list[int]` hints on a dataclass reject a JSON string at runtime?"""
    return False
