import json
from pathlib import Path

from icm import cli


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPLETED_EXAMPLE = REPO_ROOT / "examples" / "completed-content-plan"
RESEARCH_EXAMPLE = REPO_ROOT / "examples" / "completed-research-brief"
DOCS_EXAMPLE = REPO_ROOT / "examples" / "completed-documentation-refresh"
PROJECT_EXAMPLE = REPO_ROOT / "examples" / "completed-project-plan"


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


def test_cli_json_outputs_are_machine_readable(capsys) -> None:
    assert cli.main(["status", str(COMPLETED_EXAMPLE), "--json"]) == 0
    status_payload = json.loads(capsys.readouterr().out)
    assert status_payload["passed"] is True
    assert status_payload["next_action"]["type"] == "review_or_accept_handoff"
    assert status_payload["stages"][0]["name"] == "00_intake"
    assert status_payload["stages"][0]["path"] == "stages/00_intake"
    assert status_payload["stages"][0]["accepted_outputs"] == []

    assert cli.main(["review", "stages/01_discovery", "--workspace", str(COMPLETED_EXAMPLE), "--json"]) == 0
    review_payload = json.loads(capsys.readouterr().out)
    assert review_payload["passed"] is True
    assert review_payload["stage"] == "01_discovery"
    assert review_payload["summary"]["fail"] == 0
    assert review_payload["findings"][0]["level"] == "PASS"
    assert review_payload["acceptance"]["accepted"] is False

    assert cli.main(["doctor", str(COMPLETED_EXAMPLE), "--json"]) == 0
    doctor_payload = json.loads(capsys.readouterr().out)
    assert doctor_payload["passed"] is True
    assert doctor_payload["structure"]["passed"] is True
    assert doctor_payload["content"]["passed"] is True
    assert doctor_payload["next_action"]["type"] == "review_or_accept_handoff"


def test_cli_accept_marks_handoff_in_plain_file(tmp_path: Path, capsys) -> None:
    target = tmp_path / "accept-demo"
    assert cli.main(["new", str(target), "--name", "Accept Demo"]) == 0
    capsys.readouterr()
    (target / "stages" / "00_intake" / "output" / "project-brief.md").write_text(
        """# Project Brief

## Desired Outcome

Create a tiny accepted handoff.

## Audience Or Users

The maintainer.

## Success Criteria

The accepted output appears in status JSON.
""",
        encoding="utf-8",
    )

    assert cli.main(["review", "stages/00_intake", "--workspace", str(target)]) == 0
    assert "Human acceptance: 0/1 accepted" in capsys.readouterr().out

    assert (
        cli.main(
            [
                "accept",
                "stages/00_intake",
                "--workspace",
                str(target),
                "--reviewer",
                "Hobo",
                "--note",
                "Ready for discovery.",
                "--json",
            ]
        )
        == 0
    )
    accept_payload = json.loads(capsys.readouterr().out)
    assert accept_payload["entries"][0]["output"] == "stages/00_intake/output/project-brief.md"

    assert cli.main(["status", str(target), "--json"]) == 0
    status_payload = json.loads(capsys.readouterr().out)
    assert status_payload["stages"][0]["state"] == "accepted"
    assert status_payload["stages"][0]["accepted_outputs"] == ["project-brief.md"]
    assert "Ready for discovery." in (target / "shared" / "acceptance-log.md").read_text(encoding="utf-8")


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


def test_cli_init_can_add_common_artifact_starters(tmp_path: Path, capsys) -> None:
    target = tmp_path / "existing"
    target.mkdir()

    assert cli.main(["init", str(target), "--name", "Existing", "--with-common-artifacts"]) == 0
    output = capsys.readouterr().out

    assert "Common artifact starters" in output
    assert "shared/source-inventory.md" in output
    assert "shared/release-calendar.md" in output
    assert (target / "shared" / "source-inventory.md").is_file()
    assert (target / "shared" / "release-calendar.md").is_file()


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
    assert "Review rubric loaded" in output
    assert "Rubric required source cited" in output


def test_cli_review_research_example_passes(capsys) -> None:
    assert cli.main(["review", "stages/01_discovery", "--workspace", str(RESEARCH_EXAMPLE)]) == 0

    output = capsys.readouterr().out
    assert "Review: 01_discovery" in output
    assert "Rubric required term present" in output


def test_cli_review_documentation_example_passes(capsys) -> None:
    assert cli.main(["review", "stages/01_discovery", "--workspace", str(DOCS_EXAMPLE)]) == 0

    output = capsys.readouterr().out
    assert "Review: 01_discovery" in output
    assert "Rubric required table columns present" in output
    assert "Rubric link/path reference count met" in output

    assert cli.main(["review", "stages/05_validation", "--workspace", str(DOCS_EXAMPLE)]) == 0

    output = capsys.readouterr().out
    assert "Review: 05_validation" in output
    assert "Rubric source-inventory artifact shape valid" in output
    assert "Rubric calendar artifact shape valid" in output
    assert "Rubric decision-log artifact shape valid" in output


def test_cli_review_project_plan_example_passes(capsys) -> None:
    assert cli.main(["review", "stages/01_discovery", "--workspace", str(PROJECT_EXAMPLE)]) == 0

    output = capsys.readouterr().out
    assert "Review: 01_discovery" in output
    assert "Rubric required table columns present" in output
    assert "Rubric link/path reference count met" in output

    assert cli.main(["review", "stages/05_validation", "--workspace", str(PROJECT_EXAMPLE)]) == 0

    output = capsys.readouterr().out
    assert "Review: 05_validation" in output
    assert "Rubric source-inventory artifact shape valid" in output
    assert "Rubric calendar artifact shape valid" in output
    assert "Rubric decision-log artifact shape valid" in output
