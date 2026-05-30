# Review Rubrics

Review rubrics let a stage define deterministic artifact checks that run during `icm review`.

Use a rubric when an output needs more than "the file exists and has content." A rubric can require specific headings, require important terms, and reject placeholder or forbidden text.

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

## Good Rubric Habits

- Keep rubric items concrete and easy to verify.
- Prefer required headings for artifact structure.
- Prefer required terms for concepts that must be present somewhere in the artifact.
- Use forbidden terms for placeholders, banned claims, or known failure modes.
- Keep subjective quality judgment in the Review Gate until it can be made deterministic.
