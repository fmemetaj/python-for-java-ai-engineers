from course_kit.loader import load_concept_module

unpacking = load_concept_module("0_08", "unpacking")


def test_join_fields_default_sep() -> None:
    assert unpacking.join_fields("ERROR", "disk", "full") == "ERROR,disk,full"


def test_join_fields_keyword_sep() -> None:
    assert unpacking.join_fields("ERROR", "disk", sep="|") == "ERROR|disk"


def test_with_defaults_merges_options() -> None:
    assert unpacking.with_defaults("docsdesk", timeout=5, retries=2) == {
        "name": "docsdesk",
        "timeout": 5,
        "retries": 2,
    }


def test_apply_unpacked() -> None:
    assert unpacking.apply_unpacked(unpacking.join_fields, ("a", "b"), {"sep": "-"}) == "a-b"
