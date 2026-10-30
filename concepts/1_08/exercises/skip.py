"""2–3 minute skip check for 1.8."""


def pytest_uses_plain_assert() -> bool:
    """Does pytest use a plain `assert` instead of Assertions.assertEquals?"""
    raise NotImplementedError


def fixtures_inject_by_name() -> bool:
    """Are pytest fixtures injected by parameter name (not by type)?"""
    raise NotImplementedError
