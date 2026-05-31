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
    assert 'icm accept stages/00_intake --reviewer "Hobo"' in text
    assert "icm validate . --strict" in text


def test_dashboard_readiness_names_cli_json_contract() -> None:
    text = (DOCS / "dashboard-readiness.md").read_text(encoding="utf-8")

    assert "icm status --json" in text
    assert "icm review stages/01_discovery --workspace . --json" in text
    assert "icm accept stages/01_discovery --workspace . --json" in text
    assert "icm doctor . --json" in text
    assert "[json-output.md](json-output.md)" in text
    assert "[dashboard-prototype.md](dashboard-prototype.md)" in text
    assert "human still accepts the handoff" in text


def test_json_output_doc_names_dashboard_contract() -> None:
    text = (DOCS / "json-output.md").read_text(encoding="utf-8")

    assert "icm status examples/completed-content-plan --json" in text
    assert "icm review stages/01_discovery --workspace examples/completed-content-plan --json" in text
    assert "icm accept stages/01_discovery --workspace examples/completed-content-plan --json" in text
    assert "icm doctor examples/completed-content-plan --json" in text
    assert '"next_action"' in text
    assert '"suggested_fix": null' in text
    assert '"acceptance"' in text


def test_docs_homepage_links_walkthrough_and_dashboard_readiness() -> None:
    text = (DOCS / "index.html").read_text(encoding="utf-8")

    assert "assets/walkthrough-10-minute.svg" in text
    assert "assets/screenshot-dashboard.svg" in text
    assert "first-10-minutes.html" in text
    assert "json-output.html" in text
    assert "e2e-playtest.html" in text
    assert "handoff-acceptance.html" in text
    assert "dashboard-prototype.html" in text
    assert "dashboard-readiness.html" in text


def test_dashboard_prototype_doc_names_read_only_contract() -> None:
    text = (DOCS / "dashboard-prototype.md").read_text(encoding="utf-8")

    assert "icm dashboard examples/completed-project-plan" in text
    assert "icm status . --json" in text
    assert "icm review stages/01_discovery --workspace . --json" in text
    assert "icm accept stages/01_discovery --workspace . --json" in text
    assert "icm doctor . --json" in text
    assert "does not write workflow state" in text
    assert "Copy buttons" in text


def test_handoff_acceptance_doc_names_plain_file_source_of_truth() -> None:
    text = (DOCS / "handoff-acceptance.md").read_text(encoding="utf-8")

    assert "shared/acceptance-log.md" in text
    assert "icm accept stages/00_intake" in text
    assert "machine checks" in text


def test_e2e_playtest_includes_complete_idea_and_acceptance_loop() -> None:
    text = (DOCS / "e2e-playtest.md").read_text(encoding="utf-8")

    assert "Meeting Notes To Action Plan" in text
    assert "icm new ~/icm-meeting-notes-playtest" in text
    assert "icm accept stages/00_intake" in text
    assert "shared/acceptance-log.md" in text
