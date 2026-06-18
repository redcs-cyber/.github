from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "ai_ecosystem.php"


pytestmark = pytest.mark.skipif(shutil.which("php") is None, reason="PHP CLI is not installed")


def run_php(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["php", str(SCRIPT), *args],
        check=False,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_ai_ecosystem_php_lints() -> None:
    result = subprocess.run(
        ["php", "-l", str(SCRIPT)],
        check=False,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert "No syntax errors detected" in result.stdout


def test_ai_ecosystem_text_output_contains_complete_sections() -> None:
    result = run_php()

    assert result.returncode == 0, result.stderr
    assert "=== Comprehensive AI Ecosystem ===" in result.stdout
    assert "--- Core AI Technologies ---" in result.stdout
    assert "--- Infrastructure ---" in result.stdout
    assert "--- Tools & Platforms ---" in result.stdout
    assert "--- Applications ---" in result.stdout
    assert "Transformer Architecture:" in result.stdout
    assert "Governance:" in result.stdout


def test_ai_ecosystem_json_output_is_machine_readable() -> None:
    result = run_php("--format=json")

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)

    assert payload["title"] == "Comprehensive AI Ecosystem"
    assert payload["status"]["validation_errors"] == 0
    assert payload["status"]["components"] == 15
    assert set(payload["categories"]) == {
        "Core AI Technologies",
        "Infrastructure",
        "Tools & Platforms",
        "Applications",
    }
    assert payload["categories"]["Applications"][0]["name"] == "Healthcare"
    assert payload["categories"]["Applications"][0]["category"] == "Applications"
    assert payload["categories"]["Infrastructure"][0]["capabilities"]


def test_ai_ecosystem_validate_reports_zero_errors() -> None:
    result = run_php("--validate")

    assert result.returncode == 0, result.stderr
    assert "=== AI Ecosystem Health Summary ===" in result.stdout
    assert "Validation errors: 0" in result.stdout
    assert "Exit code: 0" in result.stdout


def test_ai_ecosystem_accepts_space_separated_format() -> None:
    result = run_php("--format", "summary")

    assert result.returncode == 0, result.stderr
    assert "Components: 15" in result.stdout
    assert "Validation errors: 0" in result.stdout


def test_ai_ecosystem_rejects_missing_format_value() -> None:
    result = run_php("--format")

    assert result.returncode == 1
    assert "Missing value for --format" in result.stderr


def test_ai_ecosystem_rejects_unknown_format() -> None:
    result = run_php("--format=xml")

    assert result.returncode == 1
    assert "Unsupported format: xml" in result.stderr
