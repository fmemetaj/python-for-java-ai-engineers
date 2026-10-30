from course_kit.loader import load_concept_module

sampling = load_concept_module("2_04", "sampling")


def test_more_random() -> None:
    assert sampling.is_more_random(1.2, 0.2) is True
    assert sampling.is_more_random(0.0, 0.8) is False


def test_fake_deterministic() -> None:
    assert sampling.fake_is_deterministic() is True
