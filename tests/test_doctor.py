"""Doctor is a local health check; it must not require Gradio or a network."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_doctor_offline_passes_in_dev_environment():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "doctor.py"), "--offline"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ready for Modules 0A/0B and the core notebooks" in result.stdout
    assert "OPENAI_API_KEY set:" in result.stdout
    assert "sk-" not in result.stdout
