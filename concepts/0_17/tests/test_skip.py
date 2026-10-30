from course_kit.loader import load_concept_module

skip = load_concept_module("0_17", "skip")


def test_should_write_get_x_methods() -> None:
    assert skip.should_write_get_x_methods() is False


def test_property_looks_like_an_attribute() -> None:
    assert skip.property_looks_like_an_attribute() is True
