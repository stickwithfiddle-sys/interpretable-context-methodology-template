from pathlib import Path

import icm.workspace as workspace


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPLETED_EXAMPLE = REPO_ROOT / "examples" / "completed-content-plan"
RESEARCH_EXAMPLE = REPO_ROOT / "examples" / "completed-research-brief"
DOCS_EXAMPLE = REPO_ROOT / "examples" / "completed-documentation-refresh"
PROJECT_EXAMPLE = REPO_ROOT / "examples" / "completed-project-plan"


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
    assert (target / "shared" / "acceptance-log.md").is_file()
    assert (target / "stages" / "01_discovery" / "output" / ".gitkeep").is_file()
    assert (target / "tools" / "validate_icm_workspace.py").is_file()
    assert workspace.validate_workspace(target).passed(strict=True)


def test_create_workspace_can_scaffold_common_artifacts(tmp_path: Path) -> None:
    target = tmp_path / "demo"

    created = workspace.create_workspace(target, name="Demo Project", include_common_artifacts=True)

    assert "shared/source-inventory.md" in created.created_common_artifacts
    assert "shared/release-calendar.md" in created.created_common_artifacts
    assert "shared/decision-log.md" in created.skipped_common_artifacts
    assert "| Source | Type | Status | Used For |" in (target / "shared" / "source-inventory.md").read_text(
        encoding="utf-8"
    )
    assert "| Date | Milestone | Owner | Status |" in (target / "shared" / "release-calendar.md").read_text(
        encoding="utf-8"
    )
    assert "| Date | Decision | Status | Rationale |" in (target / "shared" / "decision-log.md").read_text(
        encoding="utf-8"
    )
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


def test_initialize_workspace_can_scaffold_common_artifacts(tmp_path: Path) -> None:
    target = tmp_path / "existing-project"
    target.mkdir()

    initialized = workspace.initialize_workspace(target, name="Existing Project", include_common_artifacts=True)

    assert "shared/source-inventory.md" in initialized.created_files
    assert "shared/release-calendar.md" in initialized.created_files
    assert "shared/source-inventory.md" in initialized.created_common_artifacts
    assert "shared/release-calendar.md" in initialized.created_common_artifacts
    assert "shared/decision-log.md" in initialized.skipped_common_artifacts
    assert (target / "shared" / "source-inventory.md").is_file()
    assert (target / "shared" / "release-calendar.md").is_file()
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


def test_acceptance_log_marks_stage_outputs_accepted(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

## Desired Outcome

Create a small playtest workspace.

## Audience Or Users

The maintainer.

## Success Criteria

The first handoff is reviewable and accepted.
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "stages/00_intake")
    assert review.passed(strict=True)
    statuses = workspace.workspace_statuses(target)
    assert statuses[0].state == "ready_for_review"
    assert statuses[0].pending_acceptance_outputs == ("project-brief.md",)

    result = workspace.accept_reviewed_handoff(
        target,
        "stages/00_intake",
        reviewer="Hobo",
        note="Brief is ready for discovery.",
    )

    assert result.accepted_entries[0].output == "stages/00_intake/output/project-brief.md"
    assert workspace.acceptance_entry_for_output(target, brief_path).reviewer == "Hobo"
    statuses = workspace.workspace_statuses(target)
    assert statuses[0].state == "accepted"
    assert statuses[0].accepted_outputs == ("project-brief.md",)
    assert workspace.next_stage(statuses) == statuses[1]


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


def test_review_passes_required_source_inventory_shape(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

| Source | Type | Status | Used For |
| --- | --- | --- | --- |
| `README.md` | Guide | Current | Beginner entry point |
| `docs/install.md` | Install doc | Current | Install commands |

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

## Required Artifact Shapes

- source-inventory
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "00_intake")

    assert review.passed(strict=True)
    assert any("Rubric source-inventory artifact shape valid" in finding.message for finding in review.passes)


def test_review_passes_required_calendar_shape(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

| Date | Milestone | Owner | Status |
| --- | --- | --- | --- |
| 2026-06-01 | Draft docs update | Hobo | Planned |
| 2026-06-03 | Review install path | Hobo | Planned |

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

## Required Artifact Shapes

- calendar
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "00_intake")

    assert review.passed(strict=True)
    assert any("Rubric calendar artifact shape valid" in finding.message for finding in review.passes)


def test_review_passes_required_decision_log_shape(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

| Date | Decision | Status | Rationale |
| --- | --- | --- | --- |
| 2026-06-01 | Keep CLI-first release path | Accepted | Beginners need install trust before dashboard work |

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

## Required Artifact Shapes

- decision-log
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "00_intake")

    assert review.passed(strict=True)
    assert any("Rubric decision-log artifact shape valid" in finding.message for finding in review.passes)


def test_review_fails_when_calendar_shape_has_bad_date(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

| Date | Event | Owner | Status |
| --- | --- | --- | --- |
| Soon | Draft docs update | Hobo | Planned |

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

## Required Artifact Shapes

- calendar
""",
        encoding="utf-8",
    )

    review = workspace.review_stage(target, "00_intake")

    assert not review.passed()
    assert any("Rubric calendar artifact shape invalid" in finding.message for finding in review.errors)


def test_doctor_reports_rubric_shape_failures_with_fix(tmp_path: Path) -> None:
    target = tmp_path / "demo"
    workspace.create_workspace(target, name="Demo")
    brief_path = target / "stages" / "00_intake" / "output" / "project-brief.md"
    brief_path.write_text(
        """# Project Brief

| Date | Event | Owner | Status |
| --- | --- | --- | --- |
| Soon | Draft docs update | Hobo | Planned |

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

## Required Artifact Shapes

- calendar
""",
        encoding="utf-8",
    )

    doctor = workspace.doctor_workspace(target)

    assert not doctor.passed()
    failure = next(finding for finding in doctor.failures if "Rubric calendar artifact shape invalid" in finding.message)
    assert "YYYY-MM-DD" in workspace.suggest_fix(failure.message)
    assert "--with-common-artifacts" in workspace.suggest_fix(failure.message)


def test_research_example_validates_and_review_rubric_passes() -> None:
    assert workspace.validate_workspace(RESEARCH_EXAMPLE).passed(strict=True)

    review = workspace.review_stage(RESEARCH_EXAMPLE, "stages/01_discovery")

    assert review.passed(strict=True)
    assert any("Review rubric loaded" in finding.message for finding in review.passes)
    assert any("Rubric required source cited" in finding.message for finding in review.passes)


def test_documentation_example_validates_and_review_validators_pass() -> None:
    assert workspace.validate_workspace(DOCS_EXAMPLE).passed(strict=True)

    discovery_review = workspace.review_stage(DOCS_EXAMPLE, "stages/01_discovery")
    validation_review = workspace.review_stage(DOCS_EXAMPLE, "stages/05_validation")

    assert discovery_review.passed(strict=True)
    assert validation_review.passed(strict=True)
    assert any("Rubric required table columns present" in finding.message for finding in discovery_review.passes)
    assert any("Rubric link/path reference count met" in finding.message for finding in discovery_review.passes)
    assert any("Rubric source-inventory artifact shape valid" in finding.message for finding in validation_review.passes)
    assert any("Rubric calendar artifact shape valid" in finding.message for finding in validation_review.passes)
    assert any("Rubric decision-log artifact shape valid" in finding.message for finding in validation_review.passes)


def test_project_plan_example_validates_and_review_validators_pass() -> None:
    assert workspace.validate_workspace(PROJECT_EXAMPLE).passed(strict=True)

    discovery_review = workspace.review_stage(PROJECT_EXAMPLE, "stages/01_discovery")
    validation_review = workspace.review_stage(PROJECT_EXAMPLE, "stages/05_validation")

    assert discovery_review.passed(strict=True)
    assert validation_review.passed(strict=True)
    assert any("Rubric required table columns present" in finding.message for finding in discovery_review.passes)
    assert any("Rubric link/path reference count met" in finding.message for finding in discovery_review.passes)
    assert any("Rubric source-inventory artifact shape valid" in finding.message for finding in validation_review.passes)
    assert any("Rubric calendar artifact shape valid" in finding.message for finding in validation_review.passes)
    assert any("Rubric decision-log artifact shape valid" in finding.message for finding in validation_review.passes)


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
