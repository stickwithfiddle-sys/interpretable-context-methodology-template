# Review Rubrics

Review rubrics let a stage define deterministic artifact checks that run during `icm review`.

Use a rubric when an output needs more than "the file exists and has content." A rubric can require specific headings, important terms, source citations, table columns, link/path counts, and reject placeholder or forbidden text.

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

Required sections match markdown headings at any level. Required and forbidden terms are matched case-insensitively against the output text.

Required sources are matched against the output text by path or filename. For example, `../00_intake/output/project-brief.md` passes when the output cites either that path or `project-brief.md`.

Use `## Required Source References` if your team prefers a more explicit heading name; it behaves the same as `## Required Sources`.

Required table columns look for one markdown table whose header row contains every listed column. Column matching ignores case and punctuation, so `Used for` and `Used For` behave the same.

Required link/path count checks the number of distinct markdown links and inline-code file or URL references in the output. Use `## Minimum Link Or Path Count` or `## Required Path Count` if either phrase fits your team better.

Example PASS lines:

```text
PASS Rubric required table columns present in discovery-report.md: Source, Used For
PASS Rubric link/path reference count met in discovery-report.md: 14/3
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

## Good Rubric Habits

- Keep rubric items concrete and easy to verify.
- Prefer required headings for artifact structure.
- Prefer required terms for concepts that must be present somewhere in the artifact.
- Use required sources when an artifact should cite the inputs, references, or prior decisions it relied on.
- Use required table columns when a human reviewer expects a consistent artifact shape.
- Use link/path counts as a lightweight guardrail for inventories, traceability tables, or research notes.
- Use forbidden terms for placeholders, banned claims, or known failure modes.
- Keep subjective quality judgment in the Review Gate until it can be made deterministic.
