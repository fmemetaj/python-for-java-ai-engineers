import pytest
from course_kit.loader import load_concept_module

size = load_concept_module("4_03", "size")


def test_windows_and_ids() -> None:
    chunks = size.chunk_by_size("abcdefghij", max_chars=4, overlap=1, path="refunds.md")
    assert [c.chunk_id for c in chunks] == ["refunds:0", "refunds:1", "refunds:2"]
    assert chunks[0].text == "abcd"
    assert chunks[1].start == 3


def test_rejects_bad_overlap() -> None:
    with pytest.raises(ValueError):
        size.chunk_by_size("abcd", max_chars=4, overlap=4)
