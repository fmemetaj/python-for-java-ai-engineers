"""DocsDesk CLI entry helper. Fill in the bodies."""


def run_mode(module_name: str) -> str:
    """Return 'script' if this module is the process entry point, else 'imported'."""
    raise NotImplementedError


def banner(module_name: str, script_name: str) -> str:
    """Return '<script_name>: script' or '<script_name>: imported'."""
    raise NotImplementedError
