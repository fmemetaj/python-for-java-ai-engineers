from collections.abc import Iterator

from course_kit.loader import load_fundamentals, repo_root

log_stats = load_fundamentals()
SAMPLE = repo_root() / "fundamentals" / "sample.log"


def test_parse_line_skips_blanks_and_comments() -> None:
    assert log_stats.parse_line("") is None
    assert log_stats.parse_line("   ") is None
    assert log_stats.parse_line("# comment") is None


def test_parse_line_splits_level_and_message() -> None:
    parsed = log_stats.parse_line("ERROR disk full\n")
    assert parsed is not None
    assert parsed.level == "ERROR"
    assert parsed.message == "disk full"


def test_iter_logs_is_lazy_and_utf8() -> None:
    rows = log_stats.iter_logs(SAMPLE)
    assert isinstance(rows, Iterator)
    levels = [row.level for row in rows]
    assert levels == ["INFO", "ERROR", "WARNING", "ERROR", "INFO", "ERROR"]


def test_count_by_level_first_seen_order() -> None:
    counts = log_stats.count_by_level(SAMPLE)
    assert counts == {"INFO": 2, "ERROR": 3, "WARNING": 1}
    assert list(counts) == ["INFO", "ERROR", "WARNING"]


def test_messages_for_level() -> None:
    assert log_stats.messages_for_level(SAMPLE, "ERROR") == [
        "disk full",
        "timeout",
        "disk full",
    ]


def test_top_levels() -> None:
    assert log_stats.top_levels(SAMPLE, 2) == [("ERROR", 3), ("INFO", 2)]


def test_sample_log_exists() -> None:
    assert SAMPLE.is_file()
    assert "ERROR" in SAMPLE.read_text(encoding="utf-8")
