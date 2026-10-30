from pathlib import Path

from course_kit.loader import load_concept_module

ctx = load_concept_module("0_25", "context")


def test_timed_block_records_seconds() -> None:
    with ctx.timed_block() as data:
        total = sum(range(1000))
    assert total >= 0
    assert "seconds" in data
    assert data["seconds"] >= 0


def test_timed_block_records_on_error() -> None:
    try:
        with ctx.timed_block() as data:
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    assert data["seconds"] >= 0


def test_utf8_file(tmp_path: Path) -> None:
    path = tmp_path / "note.txt"
    path.write_text("café", encoding="utf-8")
    with ctx.Utf8File(path) as handle:
        assert handle.read() == "café"
