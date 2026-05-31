from pathlib import Path

import icm


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"


def test_first_10_minutes_guide_has_current_beginner_commands() -> None:
    text = (DOCS / "first-10-minutes.md").read_text(encoding="utf-8")

    assert f"icm {icm.__version__}" in text
    assert "python -m pip install icm-workspace-template" in text
    assert 'icm new my-first-icm-workspace --name "My First ICM Workspace" --with-common-artifacts' in text
    assert "icm doctor ." in text
    assert "icm validate . --strict" in text


def test_dashboard_readiness_names_cli_json_contract() -> None:
    text = (DOCS / "dashboard-readiness.md").read_text(encoding="utf-8")

    assert "icm status --json" in text
    assert "icm review stages/01_discovery --workspace . --json" in text
    assert "icm doctor . --json" in text
    assert "[json-output.md](json-output.md)" in text
    assert "[dashboard-prototype.md](dashboard-prototype.md)" in text
    assert "human still accepts the handoff" in text


def test_json_output_doc_names_dashboard_contract() -> None:
    text = (DOCS / "json-output.md").read_text(encoding="utf-8")

    assert "icm status examples/completed-content-plan --json" in text
    assert "icm review stages/01_discovery --workspace examples/completed-content-plan --json" in text
    assert "icm doctor examples/completed-content-plan --json" in text
    assert '"next_action"' in text
    assert '"suggested_fix": null' in text


def test_docs_homepage_links_walkthrough_and_dashboard_readiness() -> None:
    text = (DOCS / "index.html").read_text(encoding="utf-8")

    assert "assets/walkthrough-10-minute.svg" in text
    assert "assets/screenshot-dashboard.svg" in text
    assert "first-10-minutes.html" in text
    assert "json-output.html" in text
    assert "dashboard-prototype.html" in text
    assert "dashboard-readiness.html" in text


def test_dashboard_prototype_doc_names_read_only_contract() -> None:
    text = (DOCS / "dashboard-prototype.md").read_text(encoding="utf-8")

    assert "icm dashboard examples/completed-project-plan" in text
    assert "icm status . --json" in text
    assert "icm review stages/01_discovery --workspace . --json" in text
    assert "icm doctor . --json" in text
    assert "does not write workflow state" in text
