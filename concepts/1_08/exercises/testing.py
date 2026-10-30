"""Translate JUnit 5 annotations into pytest forms."""


def junit_to_pytest(kind: str) -> str:
    """Map @Test, @BeforeEach, @ParameterizedTest, assertEquals to pytest."""
    raise NotImplementedError


def parametrize_cases(slugs: list[str]) -> list[tuple[str]]:
    """Return a list of 1-tuples pytest can unpack as @parametrize args."""
    raise NotImplementedError
