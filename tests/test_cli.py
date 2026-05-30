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


def test_cli_review_completed_example_passes(capsys) -> None:
    assert cli.main(["review", "stages/01_discovery", "--workspace", str(COMPLETED_EXAMPLE)]) == 0

    output = capsys.readouterr().out
    assert "Review: 01_discovery" in output
    assert "Result: review checks passed." in output
