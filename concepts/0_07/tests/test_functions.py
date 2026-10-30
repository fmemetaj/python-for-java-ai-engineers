from course_kit.loader import load_concept_module

fns = load_concept_module("0_07", "functions")


def test_greet_default_and_keyword() -> None:
    assert fns.greet("Ada") == "Hello, Ada"
    assert fns.greet("Ada", prefix="Hi") == "Hi, Ada"
    assert fns.greet(prefix="Hey", name="Ada") == "Hey, Ada"


def test_add_tag_does_not_share_state() -> None:
    first = fns.add_tag("login")
    second = fns.add_tag("billing")
    assert first == ["login"]
    assert second == ["billing"]
    assert first is not second


def test_add_tag_does_not_mutate_input() -> None:
    original = ["login"]
    result = fns.add_tag("api", original)
    assert result == ["login", "api"]
    assert original == ["login"]
