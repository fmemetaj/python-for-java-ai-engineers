"""Smoke tests for the optional Gradio app without opening a server."""

import importlib.util
from pathlib import Path

import pytest

_gradio = pytest.importorskip("gradio")
if not hasattr(_gradio, "Blocks"):
    pytest.skip("optional demo extra (gradio) is not installed", allow_module_level=True)

APP_PATH = Path(__file__).resolve().parents[1] / "examples" / "gradio_app.py"
spec = importlib.util.spec_from_file_location("gradio_app", APP_PATH)
assert spec is not None
app = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(app)


def test_mock_demo_runs_without_ollama():
    category, draft, status = app.analyze_ticket(
        "Invoice unavailable", "Where is my invoice?", "Mock (no model)", "unused"
    )
    assert category == "billing"
    assert draft
    assert "no LLM" in status


def test_demo_rejects_bad_inputs():
    category, draft, status = app.analyze_ticket("x", "y", "Mock (no model)", "unused")
    assert (category, draft) == ("", "")
    assert "validation" in status


def test_ui_has_components():
    assert app.build_demo() is not None


def test_approval_does_not_send():
    assert "Nothing was sent" in app.simulate_approval(False, "A draft")
    assert "No email" in app.simulate_approval(True, "A draft")
