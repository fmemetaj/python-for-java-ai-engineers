"""Map files under src/ to import names and console-script entry points."""


def import_name(relative_path: str) -> str:
    """src/docsdesk/client.py -> docsdesk.client  (POSIX slashes)."""
    raise NotImplementedError


def console_script(module: str, func: str) -> str:
    """Return the hatch/setuptools entry spec `module:func`."""
    raise NotImplementedError


def is_src_layout(relative_path: str) -> bool:
    """True when the path starts with src/ and ends with .py."""
    raise NotImplementedError
