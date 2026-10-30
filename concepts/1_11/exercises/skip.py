"""2–3 minute skip check for 1.11."""


def pydantic_validates_at_runtime() -> bool:
    """Does Pydantic validate JSON at runtime (unlike dataclass type hints)?"""
    raise NotImplementedError


def type_hints_alone_validate_json() -> bool:
    """Do `list[int]` hints on a dataclass reject a JSON string at runtime?"""
    raise NotImplementedError
