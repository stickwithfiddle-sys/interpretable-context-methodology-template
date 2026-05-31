# Review Rubrics

Review rubrics let a stage define deterministic artifact checks that run during `icm review`.

Use a rubric when an output needs more than "the file exists and has content." A rubric can require specific headings, important terms, source citations, table columns, link/path counts, common artifact shapes, and reject placeholder or forbidden text.

If you are choosing checks for a specific workflow type, start with [workflow-rubrics.md](workflow-rubrics.md).

## Where Rubrics Live

Place a rubric in a stage `references/` folder:

```text
stages/01_discovery/references/review-rubric.md
stages/01_discovery/references/discovery-report-rubric.md
```

`review-rubric.md` applies to every declared output in that stage.

`<output-stem>-rubric.md` applies to one output. For `discovery-report.md`, use `discovery-report-rubric.md`.

## Rubric Format

```markdown
# Discovery Report Review Rubric

## Required Sections

- Known Facts
- Assumptions
- Open Questions
- Risks

## Required Terms

- traceability
- source quality

## Required Sources

- ../00_intake/output/project-brief.md
- references/discovery-question-bank.md
- ../../_config/quality-gates.md

## Required Table Columns

- Source
- Used For

## Required Link Or Path Count

- 3

## Required Artifact Shapes

- source-inventory

## Forbidden Terms

- TBD
- lorem ipsum
```

## Review Behavior

When an output exists, `icm review` loads matching rubrics and adds PASS or FAIL findings:

```bash
icm review stages/01_discovery
icm review stages/01_discovery/output/discovery-report.md
```

`icm doctor` also reports rubric failures for existing declared outputs, so shape problems can appear in the general health check before release.

Required sections match markdown headings at any level. Required and forbidden terms are matched case-insensitively against the output text.

Required sources are matched against the output text by path or filename. For example, `../00_intake/output/project-brief.md` passes when the output cites either that path or `project-brief.md`.

Use `## Required Source References` if your team prefers a more explicit heading name; it behaves the same as `## Required Sources`.

Required table columns look for one markdown table whose header row contains every listed column. Column matching ignores case and punctuation, so `Used for` and `Used For` behave the same.

Required link/path count checks the number of distinct markdown links and inline-code file or URL references in the output. Use `## Minimum Link Or Path Count` or `## Required Path Count` if either phrase fits your team better.

Required artifact shapes check common markdown artifact formats. Use `## Required Artifact Shapes` with one or more of:

| Shape | Required Pattern |
| --- | --- |
| `source-inventory` | A markdown table with Source, Type, Status, and Used For columns, plus at least one source path, URL, or link |
| `calendar` | A markdown table with Date, Event or Milestone, Owner, and Status columns; dates must use `YYYY-MM-DD` |
| `decision-log` | A markdown table with Date, Decision, Status, and Rationale or Reason columns; dates must use `YYYY-MM-DD` |

Use `## Required Artifact Validators` or `## Required Artifact Types` if either heading fits your team better; they behave the same as `## Required Artifact Shapes`.

To add starter files for these common shapes to a workspace, run:

```bash
icm init . --with-common-artifacts
```

That creates `shared/source-inventory.md` and `shared/release-calendar.md` when missing, and keeps the shared decision log in the validator-friendly table shape.

Example PASS lines:

```text
PASS Rubric required table columns present in discovery-report.md: Source, Used For
PASS Rubric link/path reference count met in discovery-report.md: 14/3
PASS Rubric source-inventory artifact shape valid in source-inventory.md
PASS Rubric calendar artifact shape valid in release-calendar.md
PASS Rubric decision-log artifact shape valid in decision-log.md
```

## Source Traceability Pattern

A simple source traceability section is usually enough:

```markdown
## Source Traceability

| Source | Used For |
| --- | --- |
| `../00_intake/output/project-brief.md` | Project goals, users, and constraints |
| `references/discovery-question-bank.md` | Discovery coverage |
```

This keeps the review deterministic while still leaving the human reviewer room to judge whether the use of each source is reasonable.

When the traceability table is part of the contract, add both checks to the rubric:

```markdown
## Required Table Columns

- Source
- Used For

## Required Link Or Path Count

- 3
```

## Common Artifact Shape Examples

Source inventory:

```markdown
| Source | Type | Status | Used For |
| --- | --- | --- | --- |
| `README.md` | Beginner entry point | Current | First-run instructions |
| `docs/install.md` | Install guide | Current | PyPI commands |
```

Calendar:

```markdown
| Date | Milestone | Owner | Status |
| --- | --- | --- | --- |
| 2026-06-01 | Review upgrade docs | Hobo | Planned |
```

Decision log:

```markdown
| Date | Decision | Status | Rationale |
| --- | --- | --- | --- |
| 2026-06-01 | Keep CLI-first release path | Accepted | Beginners need a trustworthy install path |
```

## Good Rubric Habits

- Keep rubric items concrete and easy to verify.
- Prefer required headings for artifact structure.
- Prefer required terms for concepts that must be present somewhere in the artifact.
- Use required sources when an artifact should cite the inputs, references, or prior decisions it relied on.
- Use required table columns when a human reviewer expects a consistent artifact shape.
- Use link/path counts as a lightweight guardrail for inventories, traceability tables, or research notes.
- Use required artifact shapes for source inventories, calendars, and decision logs that should stay machine-checkable.
- Use forbidden terms for placeholders, banned claims, or known failure modes.
- Keep subjective quality judgment in the Review Gate until it can be made deterministic.
