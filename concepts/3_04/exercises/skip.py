"""2–3 minute skip check for 3.4."""


def tool_args_must_be_validated() -> bool:
    """Should tool arguments be validated before your code runs them?"""
    raise NotImplementedError


def unknown_tools_should_run_anyway() -> bool:
    """If the model names a tool that is not on your allow-list, should you run it?"""
    raise NotImplementedError
