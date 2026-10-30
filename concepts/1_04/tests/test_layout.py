from course_kit.loader import load_concept_module
import pytest

layout = load_concept_module("1_04", "layout")


def test_import_name() -> None:
    assert layout.import_name("src/docsdesk/client.py") == "docsdesk.client"


def test_import_name_init() -> None:
    assert layout.import_name("src/docsdesk/__init__.py") == "docsdesk.__init__"


def test_console_script() -> None:
    assert layout.console_script("docsdesk.__main__", "main") == "docsdesk.__main__:main"


def test_is_src_layout() -> None:
    assert layout.is_src_layout("src/docsdesk/settings.py") is True
    assert layout.is_src_layout("concepts/1_04/examples.py") is False


def test_rejects_non_src() -> None:
    with pytest.raises(ValueError):
        layout.import_name("docsdesk/client.py")
