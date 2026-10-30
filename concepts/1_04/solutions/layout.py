"""Map files under src/ to import names and console-script entry points (solution)."""


def import_name(relative_path: str) -> str:
    """src/docsdesk/client.py -> docsdesk.client  (POSIX slashes)."""
    path = relative_path.replace("\\", "/")
    if not path.startswith("src/") or not path.endswith(".py"):
        raise ValueError(f"not a src-layout module: {relative_path}")
    body = path.removeprefix("src/").removesuffix(".py")
    return body.replace("/", ".")


def console_script(module: str, func: str) -> str:
    """Return the hatch/setuptools entry spec `module:func`."""
    return f"{module}:{func}"


def is_src_layout(relative_path: str) -> bool:
    """True when the path starts with src/ and ends with .py."""
    path = relative_path.replace("\\", "/")
    return path.startswith("src/") and path.endswith(".py")
