"""2–3 minute skip check for A.9. Still recommended — this concept is NEW."""


def smoke_tests_must_stop_when_the_next_call_would_exceed_the_cap() -> bool:
    """Should a spend cap skip remaining calls instead of going over?"""
    raise NotImplementedError


def recorded_fixtures_may_include_live_api_keys() -> bool:
    """May committed recorded fixtures include sk-... keys?"""
    raise NotImplementedError
