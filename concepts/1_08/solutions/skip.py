"""Solutions for the 1.8 skip check."""


def pytest_uses_plain_assert() -> bool:
    """Does pytest use a plain `assert` instead of Assertions.assertEquals?"""
    return True


def fixtures_inject_by_name() -> bool:
    """Are pytest fixtures injected by parameter name (not by type)?"""
    return True
