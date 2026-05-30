from pathlib import Path

import icm.workspace as workspace


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPLETED_EXAMPLE = REPO_ROOT / "examples" / "completed-content-plan"


def test_slugify_normalizes_names() -> None:
    assert workspace.slugify("My First ICM Workspace!") == "my-first-icm-workspace"
    assert workspace.slugify("___") == "icm-project"


def test_create_workspace_from_source_template_preserves_beginner_assets(tmp_path: Path) -> None:
    target = tmp_path / "demo"

    created = workspace.create_workspace(target, name="Demo Project")

    assert created.target == target.resolve()
    assert created.project_name == "Demo Project"
    assert (target / "AGENTS.md").is_file()
    assert (target / ".gitignore").is_file()
    assert (target / ".github" / "prompts" / "run-icm-stage.prompt.md").is_file()
    assert (target / "stages" / "01_discovery" / "output" / ".gitkeep").is_file()
    assert (target / "tools" / "validate_icm_workspace.py").is_file()
    assert workspace.validate_workspace(target).passed(strict=True)


def test_create_workspace_from_packaged_resources_preserves_beginner_assets(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(workspace, "TEMPLATE_ROOT", tmp_path / "missing-template")
    monkeypatch.setattr(workspace, "LEGACY_VALIDATOR", tmp_path / "missing-validator.py")
    target = tmp_path / "packaged-demo"

    workspace.create_workspace(target, name="Packaged Demo")

    assert (target / ".gitignore").is_file()
    assert (target / ".github" / "prompts" / "review-icm-output.prompt.md").is_file()
    assert (target / "stages" / "05_validation" / "output" / ".gitkeep").is_file()
    assert (target / "tools" / "validate_icm_workspace.py").is_file()
    assert workspace.validate_workspace(target).passed(strict=True)


def test_new_workspace_status_starts_at_intake(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")

    statuses = workspace.workspace_statuses(target)

    assert statuses[0].name == "00_intake"
    assert statuses[0].state == "needs_input"
    assert workspace.next_stage(statuses) == statuses[0]


def test_review_completed_example_passes() -> None:
    review = workspace.review_stage(COMPLETED_EXAMPLE, "stages/01_discovery")

    assert review.passed(strict=True)
    assert not review.errors
    assert any("Declared output has content" in finding.message for finding in review.passes)


def test_review_unfinished_intake_fails(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")

    review = workspace.review_stage(target, "00_intake")

    assert not review.passed()
    assert any("Project brief is missing" in finding.message for finding in review.errors)
