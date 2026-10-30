from collections.abc import Iterator

from course_kit.loader import load_placement

place = load_placement()


def test_run_mode() -> None:
    assert place.run_mode("__main__") == "script"
    assert place.run_mode("placement.self_check") == "imported"


def test_after_rebind_keeps_original_object() -> None:
    source = [1, 2]
    alias = place.after_rebind(source)
    assert alias is source
    assert alias == [1, 2]


def test_none_label() -> None:
    assert place.none_label(None) == "missing"
    assert place.none_label(0) == "present"


def test_keep_truthy() -> None:
    assert place.keep_truthy([0, "", "ok", None, "0"]) == ["ok", "0"]


def test_label_status() -> None:
    assert place.label_status(200) == "ok"
    assert place.label_status(404) == "client"
    assert place.label_status(500) == "server"
    assert place.label_status(1) == "other"


def test_add_tag_isolated() -> None:
    first = place.add_tag("login")
    second = place.add_tag("billing")
    assert first == ["login"]
    assert second == ["billing"]
    original = ["x"]
    assert place.add_tag("y", original) == ["x", "y"]
    assert original == ["x"]


def test_join_fields() -> None:
    assert place.join_fields("a", "b", sep="|") == "a|b"


def test_make_counter() -> None:
    counter = place.make_counter(4)
    assert counter() == 5
    assert counter() == 6


def test_error_messages() -> None:
    rows = [
        {"level": "INFO", "message": "up"},
        {"level": "ERROR", "message": "down"},
    ]
    assert place.error_messages(rows) == ["down"]


def test_iter_errors() -> None:
    result = place.iter_errors(["INFO x", "ERROR y"])
    assert isinstance(result, Iterator)
    assert list(result) == ["ERROR y"]
    assert list(result) == []
