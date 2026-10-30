"""DocsDesk CLI entry helper (solution)."""


def run_mode(module_name: str) -> str:
    """Return 'script' if this module is the process entry point, else 'imported'."""
    return "script" if module_name == "__main__" else "imported"


def banner(module_name: str, script_name: str) -> str:
    """Return '<script_name>: script' or '<script_name>: imported'."""
    return f"{script_name}: {run_mode(module_name)}"
