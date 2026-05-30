from pathlib import Path

from icm import cli


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPLETED_EXAMPLE = REPO_ROOT / "examples" / "completed-content-plan"


def test_cli_new_validate_status_and_review(tmp_path: Path, capsys) -> None:
    target = tmp_path / "cli-demo"

    assert cli.main(["new", str(target), "--name", "CLI Demo"]) == 0
    assert "Created ICM workspace" in capsys.readouterr().out

    assert cli.main(["validate", str(target), "--strict"]) == 0
    assert "OK: workspace passed validation" in capsys.readouterr().out

    assert cli.main(["status", str(target)]) == 0
    assert "needs_input" in capsys.readouterr().out

    assert cli.main(["review", "00_intake", "--workspace", str(target)]) == 1
    assert "Project brief is missing" in capsys.readouterr().out


def test_cli_init_preserves_existing_project_files(tmp_path: Path, capsys) -> None:
    target = tmp_path / "existing"
    target.mkdir()
    (target / "README.md").write_text("# Existing\n", encoding="utf-8")

    assert cli.main(["init", str(target), "--name", "Existing"]) == 0
    output = capsys.readouterr().out

    assert "Initialized ICM workspace" in output
    assert "Skipped existing files" in output
    assert (target / "README.md").read_text(encoding="utf-8") == "# Existing\n"
    assert (target / "stages" / "00_intake" / "CONTEXT.md").is_file()


def test_cli_doctor_reports_content_checks(tmp_path: Path, capsys) -> None:
    target = tmp_path / "doctor-demo"
    cli.main(["new", str(target), "--name", "Doctor Demo"])
    capsys.readouterr()

    assert cli.main(["doctor", str(target), "--strict"]) == 1
    output = capsys.readouterr().out

    assert "Content checks: needs attention" in output
    assert "Project brief needs required sections" in output


def test_cli_review_completed_example_passes(capsys) -> None:
    assert cli.main(["review", "stages/01_discovery", "--workspace", str(COMPLETED_EXAMPLE)]) == 0

    output = capsys.readouterr().out
    assert "Review: 01_discovery" in output
    assert "Result: review checks passed." in output
