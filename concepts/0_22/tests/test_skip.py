from course_kit.loader import load_concept_module

skip = load_concept_module("0_22", "skip")


def test_protocol_is_structural() -> None:
    assert skip.protocol_is_structural() is True


def test_abc_is_nominal() -> None:
    assert skip.abc_is_nominal() is True
