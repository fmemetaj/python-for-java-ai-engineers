"""2–3 minute skip check for 0.19."""


def dataclass_validates_at_runtime() -> bool:
    """Does @dataclass reject the wrong field types at runtime by itself?"""
    raise NotImplementedError


def pydantic_validates_at_runtime() -> bool:
    """Does a Pydantic BaseModel validate input at runtime?"""
    raise NotImplementedError
