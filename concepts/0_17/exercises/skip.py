"""2–3 minute skip check for 0.17."""


def should_write_get_x_methods() -> bool:
    """Should a typical Python class expose getX()/setX() like JavaBeans?"""
    raise NotImplementedError


def property_looks_like_an_attribute() -> bool:
    """Does @property let callers use obj.field syntax?"""
    raise NotImplementedError
