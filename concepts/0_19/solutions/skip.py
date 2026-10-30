"""Solutions for the 0.19 skip check."""


def dataclass_validates_at_runtime() -> bool:
    """Does @dataclass reject the wrong field types at runtime by itself?"""
    return False


def pydantic_validates_at_runtime() -> bool:
    """Does a Pydantic BaseModel validate input at runtime?"""
    return True
