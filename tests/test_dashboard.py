import json
import threading
from pathlib import Path
from urllib.request import urlopen

from icm.dashboard import bind_dashboard_server, collect_dashboard_payload, render_dashboard_html, resolve_workspace_file


def test_dashboard_payload_uses_cli_json_contract(tmp_path: Path) -> None:
    stage_root = tmp_path / "stages" / "00_intake"
    output_root = stage_root / "output"
    shared_root = tmp_path / "shared"
    output_root.mkdir(parents=True)
    shared_root.mkdir()
    (stage_root / "CONTEXT.md").write_text(
        "# Intake Contract\n\nCapture the brief before discovery.\n",
        encoding="utf-8",
    )
    (output_root / "project-brief.md").write_text(
        "# Project Brief\n\n## Source Traceability\n\n- README.md confirms the setup path.\n",
        encoding="utf-8",
    )
    (shared_root / "acceptance-log.md").write_text(
        "| Date | Stage | Output | Reviewer | Status | Notes |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| 2026-05-31 | stages/00_intake | stages/00_intake/output/project-brief.md | Hobo | Accepted | Accepted during dashboard preview test. |\n",
        encoding="utf-8",
    )
    calls: list[list[str]] = []

    def fake_runner(args: list[str], workspace_root: Path) -> dict:
        calls.append(args)
        if args[0] == "status":
            return {
                "command": "icm status /workspace --json",
                "passed": True,
                "stages": [
                    {
                        "name": "00_intake",
                        "path": "stages/00_intake",
                        "purpose": "Capture the brief.",
                        "state": "accepted",
                        "existing_outputs": ["project-brief.md"],
                        "accepted_outputs": ["project-brief.md"],
                        "pending_acceptance_outputs": [],
                    },
                    {
                        "name": "01_discovery",
                        "path": "stages/01_discovery",
                        "purpose": "Discover the workflow.",
                        "state": "waiting",
                        "existing_outputs": [],
                        "accepted_outputs": [],
                        "pending_acceptance_outputs": [],
                    },
                ],
                "next_action": {"type": "run_or_repair_stage", "message": "Run discovery."},
            }
        if args[0] == "doctor":
            return {
                "command": "icm doctor /workspace --json",
                "passed": True,
                "structure": {"findings": []},
                "content": {"findings": []},
            }
        if args[0] == "review":
            return {
                "command": "icm review stages/00_intake --workspace /workspace --json",
                "passed": True,
                "stage": "00_intake",
                "stage_path": "stages/00_intake",
                "output_path": "stages/00_intake/output/project-brief.md",
                "summary": {"fail": 0, "warn": 1, "pass": 3},
                "acceptance": {
                    "accepted": True,
                    "outputs": [
                        {
                            "path": "stages/00_intake/output/project-brief.md",
                            "accepted": True,
                            "status": "Accepted",
                            "reviewer": "Hobo",
                        }
                    ],
                },
                "findings": [
                    {
                        "level": "WARN",
                        "message": "Source Traceability in project-brief.md should name at least one source.",
                        "suggested_fix": "Add the source filename or URL used for the brief.",
                    }
                ],
            }
        raise AssertionError(f"Unexpected command: {args}")

    payload = collect_dashboard_payload(tmp_path, cli_runner=fake_runner)

    assert payload["read_only"] is True
    assert payload["summary"]["stages"] == 2
    assert payload["summary"]["accepted_stages"] == 1
    assert payload["summary"]["ready_for_review"] == 0
    assert payload["summary"]["review_failures"] == 0
    assert payload["summary"]["review_warnings"] == 1
    assert [call[0] for call in calls] == ["status", "doctor", "review"]
    assert calls[2][1] == "stages/00_intake"
    review = payload["reviews"][0]
    assert review["stage"] == "00_intake"
    assert review["commands"]["review"] == f"icm review stages/00_intake --workspace {tmp_path.resolve().as_posix()}"
    assert review["commands"]["accept"] == f"icm accept stages/00_intake --workspace {tmp_path.resolve().as_posix()}"
    preview_by_path = {preview["path"]: preview for preview in review["source_previews"]}
    assert "stages/00_intake/CONTEXT.md" in preview_by_path
    assert "stages/00_intake/output/project-brief.md" in preview_by_path
    assert "Capture the brief" in preview_by_path["stages/00_intake/CONTEXT.md"]["excerpt"]
    assert "Source Traceability" in preview_by_path["stages/00_intake/output/project-brief.md"]["excerpt"]
    log_preview = review["acceptance"]["log_preview"]
    assert log_preview["path"] == "shared/acceptance-log.md"
    assert log_preview["exists"] is True
    assert "Accepted during dashboard preview test" in log_preview["excerpt"]


def test_dashboard_serves_workspace_json(tmp_path: Path) -> None:
    (tmp_path / "CONTEXT.md").write_text("# Context\n", encoding="utf-8")

    def fake_runner(args: list[str], workspace_root: Path) -> dict:
        if args[0] == "status":
            return {"command": "icm status --json", "stages": [], "next_action": {"type": "run_doctor"}}
        if args[0] == "doctor":
            return {"command": "icm doctor --json", "passed": True, "structure": {"findings": []}, "content": {"findings": []}}
        raise AssertionError(f"Unexpected command: {args}")

    binding = bind_dashboard_server(tmp_path, "127.0.0.1", 0, allow_port_fallback=False, cli_runner=fake_runner)
    thread = threading.Thread(target=binding.server.serve_forever, daemon=True)
    thread.start()
    try:
        with urlopen(f"{binding.url}api/workspace", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    finally:
        binding.server.shutdown()
        binding.server.server_close()
        thread.join(timeout=5)

    assert payload["workspace"] == tmp_path.resolve().as_posix()
    assert payload["status"]["command"] == "icm status --json"


def test_dashboard_source_paths_stay_inside_workspace(tmp_path: Path) -> None:
    source = tmp_path / "stages" / "00_intake" / "CONTEXT.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Intake\n", encoding="utf-8")

    assert resolve_workspace_file(tmp_path.resolve(), "stages/00_intake/CONTEXT.md") == source.resolve()

    try:
        resolve_workspace_file(tmp_path.resolve(), "../outside.md")
    except ValueError as error:
        assert "inside the workspace" in str(error)
    else:
        raise AssertionError("Expected path traversal to be rejected")


def test_dashboard_html_contains_runtime_contract() -> None:
    html = render_dashboard_html()

    assert "ICM Dashboard" in html
    assert "/api/workspace" in html
    assert "CLI Source" in html
    assert "Read-only" in html
    assert "machine passing" in html
    assert "Human acceptance" in html
    assert "copyCommandButton" in html
    assert "commandRow" in html
    assert "renderSourcePreviews" in html
    assert "Source previews" in html
    assert "data-copy" in html
