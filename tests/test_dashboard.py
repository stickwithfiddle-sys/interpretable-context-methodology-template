import json
import threading
from pathlib import Path
from urllib.request import urlopen

from icm.dashboard import bind_dashboard_server, collect_dashboard_payload, render_dashboard_html, resolve_workspace_file


def test_dashboard_payload_uses_cli_json_contract(tmp_path: Path) -> None:
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
                "summary": {"fail": 0, "warn": 0, "pass": 3},
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
                "findings": [],
            }
        raise AssertionError(f"Unexpected command: {args}")

    payload = collect_dashboard_payload(tmp_path, cli_runner=fake_runner)

    assert payload["read_only"] is True
    assert payload["summary"]["stages"] == 2
    assert payload["summary"]["accepted_stages"] == 1
    assert payload["summary"]["ready_for_review"] == 0
    assert payload["summary"]["review_failures"] == 0
    assert [call[0] for call in calls] == ["status", "doctor", "review"]
    assert calls[2][1] == "stages/00_intake"
    assert payload["reviews"][0]["stage"] == "00_intake"


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
