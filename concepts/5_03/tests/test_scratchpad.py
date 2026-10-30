from course_kit.loader import load_concept_module

scratch = load_concept_module("5_03", "scratchpad")


def test_join() -> None:
    assert scratch.scratchpad(["a", "b"], max_chars=10) == "a | b"


def test_ellipsize() -> None:
    text = scratch.scratchpad(["NPE in RefundService after capture"], max_chars=12)
    assert len(text) == 12
    assert text.endswith("...")
