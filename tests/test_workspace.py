from pathlib import Path

import icm.workspace as workspace


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPLETED_EXAMPLE = REPO_ROOT / "examples" / "completed-content-plan"
RESEARCH_EXAMPLE = REPO_ROOT / "examples" / "completed-research-brief"
DOCS_EXAMPLE = REPO_ROOT / "examples" / "completed-documentation-refresh"


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


def test_initialize_workspace_preserves_existing_files(tmp_path: Path) -> None:
    target = tmp_path / "existing-project"
    target.mkdir()
    readme_path = target / "README.md"
    readme_path.write_text("# Existing Project\n", encoding="utf-8")

    initialized = workspace.initialize_workspace(target, name="Existing Project")

    assert "README.md" in initialized.skipped_files
    assert "AGENTS.md" in initialized.created_files
    assert readme_path.read_text(encoding="utf-8") == "# Existing Project\n"
    assert (target / "stages" / "00_intake" / "CONTEXT.md").is_file()
    assert (target / "tools" / "validate_icm_workspace.py").is_file()
    assert workspace.validate_workspace(target).passed(strict=True)


def test_doctor_warns_when_existing_root_files_need_icm_guidance(tmp_path: Path) -> None:
    target = tmp_path / "existing-project"
    target.mkdir()
    (target / "AGENTS.md").write_text("# Existing Agent Notes\n", encoding="utf-8")
    (target / "CONTEXT.md").write_text("# Existing Context\n", encoding="utf-8")

    workspace.initialize_workspace(target, name="Existing Project")
    result = workspace.doctor_workspace(target)

    assert any("Layer 0 identity file may not contain ICM guidance" in finding.message for finding in result.warnings)
    assert any("Layer 1 routing file may not include" in finding.message for finding in result.warnings)


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
    assert any("Review rubric loaded" in finding.message for finding in review.passes)
    assert any("Rubric required section present" in finding.message for finding in review.passes)
    assert any("Rubric required source cited" in finding.message for finding in review.passes)


def test_review_fails_when_rubric_required_section_is_missing(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

## Desired Outcome

Demo outcome.

## Audience Or Users

Demo audience.

## Success Criteria

Demo criteria.
""",
        encoding="utf-8",
    )
    rubric_path = target / "stages" / "00_intake" / "references" / "project-brief-rubric.md"
    rubric_path.write_text(
        """# Project Brief Rubric

## Required Sections

- Definitely Missing
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "00_intake")

    assert not review.passed()
    assert any("Rubric required section missing" in finding.message for finding in review.errors)


def test_review_fails_when_rubric_required_source_is_missing(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

## Desired Outcome

Demo outcome.

## Audience Or Users

Demo audience.

## Success Criteria

Demo criteria.
""",
        encoding="utf-8",
    )
    rubric_path = target / "stages" / "00_intake" / "references" / "project-brief-rubric.md"
    rubric_path.write_text(
        """# Project Brief Rubric

## Required Sources

- references/source-note.md
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "00_intake")

    assert not review.passed()
    assert any("Rubric required source missing" in finding.message for finding in review.errors)


def test_review_passes_when_rubric_required_source_is_cited_by_filename(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

Source: source-note.md

## Desired Outcome

Demo outcome.

## Audience Or Users

Demo audience.

## Success Criteria

Demo criteria.
""",
        encoding="utf-8",
    )
    rubric_path = target / "stages" / "00_intake" / "references" / "project-brief-rubric.md"
    rubric_path.write_text(
        """# Project Brief Rubric

## Required Sources

- references/source-note.md
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "00_intake")

    assert review.passed(strict=True)
    assert any("Rubric required source cited" in finding.message for finding in review.passes)


def test_review_fails_when_required_table_columns_are_missing(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

| Source | Status |
| --- | --- |
| `README.md` | Current |

## Desired Outcome

Demo outcome.

## Audience Or Users

Demo audience.

## Success Criteria

Demo criteria.
""",
        encoding="utf-8",
    )
    rubric_path = target / "stages" / "00_intake" / "references" / "project-brief-rubric.md"
    rubric_path.write_text(
        """# Project Brief Rubric

## Required Table Columns

- Source
- Status
- Owner
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "00_intake")

    assert not review.passed()
    assert any("Rubric required table columns missing" in finding.message for finding in review.errors)


def test_review_passes_when_table_columns_and_path_count_match(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

| Source | Status | Owner |
| --- | --- | --- |
| `README.md` | Current | Hobo |
| `docs/install.md` | Needs review | Hobo |
| [Roadmap](../../ROADMAP.md) | Current | Hobo |

## Desired Outcome

Demo outcome.

## Audience Or Users

Demo audience.

## Success Criteria

Demo criteria.
""",
        encoding="utf-8",
    )
    rubric_path = target / "stages" / "00_intake" / "references" / "project-brief-rubric.md"
    rubric_path.write_text(
        """# Project Brief Rubric

## Required Table Columns

- Source
- Status
- Owner

## Required Link Or Path Count

- 3
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "00_intake")

    assert review.passed(strict=True)
    assert any("Rubric required table columns present" in finding.message for finding in review.passes)
    assert any("Rubric link/path reference count met" in finding.message for finding in review.passes)


def test_review_fails_when_path_count_is_too_low(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

Source: `README.md`

## Desired Outcome

Demo outcome.

## Audience Or Users

Demo audience.

## Success Criteria

Demo criteria.
""",
        encoding="utf-8",
    )
    rubric_path = target / "stages" / "00_intake" / "references" / "project-brief-rubric.md"
    rubric_path.write_text(
        """# Project Brief Rubric

## Required Link Or Path Count

- 2
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "00_intake")

    assert not review.passed()
    assert any("Rubric link/path reference count too low" in finding.message for finding in review.errors)


def test_research_example_validates_and_review_rubric_passes() -> None:
    assert workspace.validate_workspace(RESEARCH_EXAMPLE).passed(strict=True)

    review = workspace.review_stage(RESEARCH_EXAMPLE, "stages/01_discovery")

    assert review.passed(strict=True)
    assert any("Review rubric loaded" in finding.message for finding in review.passes)
    assert any("Rubric required source cited" in finding.message for finding in review.passes)


def test_documentation_example_validates_and_review_validators_pass() -> None:
    assert workspace.validate_workspace(DOCS_EXAMPLE).passed(strict=True)

    review = workspace.review_stage(DOCS_EXAMPLE, "stages/01_discovery")

    assert review.passed(strict=True)
    assert any("Rubric required table columns present" in finding.message for finding in review.passes)
    assert any("Rubric link/path reference count met" in finding.message for finding in review.passes)


def test_review_unfinished_intake_fails(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")

    review = workspace.review_stage(target, "00_intake")

    assert not review.passed()
    assert any("Project brief is missing" in finding.message for finding in review.errors)


def test_doctor_flags_empty_intake_and_missing_config_input(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    (target / "_config" / "quality-gates.md").unlink()

    result = workspace.doctor_workspace(target)

    assert not result.passed()
    assert any("Project brief needs required sections" in finding.message for finding in result.warnings)
    assert any("Declared input is missing" in finding.message for finding in result.failures)
