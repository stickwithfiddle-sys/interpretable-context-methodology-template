# Scaffold Plan

## Proposed Workspace Tree

```text
research-brief-workspace/
  AGENTS.md
  CONTEXT.md
  _config/
    evidence-rules.md
    brief-style.md
    project-profile.md
  shared/
    decision-log.md
    glossary.md
  stages/
    00_intake/
      CONTEXT.md
      output/research-brief-intake.md
    01_source_triage/
      CONTEXT.md
      references/source-types.md
      output/source-triage.md
    02_synthesis/
      CONTEXT.md
      references/synthesis-patterns.md
      output/synthesis-notes.md
    03_brief_draft/
      CONTEXT.md
      references/brief-outline.md
      output/research-brief.md
    04_validation/
      CONTEXT.md
      references/traceability-checklist.md
      output/validation-report.md
```

## Stage Contract Notes

| Stage | Contract Focus |
| --- | --- |
| `00_intake` | Keep the research question, audience, and decision deadline explicit |
| `01_source_triage` | Classify sources before synthesis begins |
| `02_synthesis` | Separate facts, interpretations, contradictions, and gaps |
| `03_brief_draft` | Make recommendation, evidence, confidence, and risks visible |
| `04_validation` | Check traceability and readiness before acceptance |

## Review Rubrics To Seed

| Rubric | Purpose |
| --- | --- |
| `stages/01_source_triage/references/source-triage-rubric.md` | Confirm source classification quality |
| `stages/03_brief_draft/references/research-brief-rubric.md` | Confirm the brief contains recommendation, evidence, confidence, and risks |
| `stages/04_validation/references/validation-report-rubric.md` | Confirm traceability and go/no-go criteria |

## Deterministic Checks

- Validate workspace structure with `icm validate --strict`.
- Review stage outputs with `icm review`.
- Use rubrics for required headings, required terms, and forbidden placeholder text.

## Recommendation

Create the project-specific workspace from this scaffold, then dry-run it once with a small research question before adopting it for larger decisions.
