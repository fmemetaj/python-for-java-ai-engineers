from course_kit.loader import load_concept_module

duck = load_concept_module("0_21", "duck")


class Countable:
    def line_count(self) -> int:
        return 3


class HasLines:
    def __init__(self) -> None:
        self.lines = ["a", "b"]


class Reader:
    def read(self) -> str:
        return "ok"


def test_line_count_method() -> None:
    assert duck.line_count(Countable()) == 3


def test_line_count_from_lines() -> None:
    assert duck.line_count(HasLines()) == 2


def test_line_count_rejects_unknown() -> None:
    try:
        duck.line_count(object())
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")


def test_can_stream() -> None:
    assert duck.can_stream(Reader()) is True
    assert duck.can_stream("not a stream") is False
