"""Solutions for the 0.17 skip check."""


def should_write_get_x_methods() -> bool:
    """Should a typical Python class expose getX()/setX() like JavaBeans?"""
    return False


def property_looks_like_an_attribute() -> bool:
    """Does @property let callers use obj.field syntax?"""
    return True
