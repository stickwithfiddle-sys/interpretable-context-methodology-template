# Scaffold Plan

## Proposed Workspace Tree

```text
docs-refresh-workspace/
  AGENTS.md
  CONTEXT.md
  _config/
    docs-style-guide.md
    source-priority.md
    quality-gates.md
  shared/
    decision-log.md
    backlog.md
  stages/
    00_intake/
      CONTEXT.md
      output/docs-refresh-brief.md
    01_source_inventory/
      CONTEXT.md
      references/source-types.md
      references/source-inventory-rubric.md
      output/source-inventory.md
    02_gap_analysis/
      CONTEXT.md
      references/gap-severity.md
      output/gap-analysis.md
    03_update_plan/
      CONTEXT.md
      references/update-plan-rubric.md
      output/docs-update-plan.md
    04_review_pack/
      CONTEXT.md
      references/review-pack-template.md
      output/review-pack.md
    05_validation/
      CONTEXT.md
      references/docs-validation-rubric.md
      output/validation-report.md
```

## Stage Responsibilities

| Stage | Responsibility |
| --- | --- |
| `00_intake` | Capture docs goal, audience, release context, and constraints |
| `01_source_inventory` | Classify docs, release notes, pages, and support inputs before analysis |
| `02_gap_analysis` | Identify stale commands, missing explanations, and source disagreements |
| `03_update_plan` | Produce concrete doc edits with owner, status, and cited source |
| `04_review_pack` | Package risks, tradeoffs, and unresolved questions for approval |
| `05_validation` | Check traceability and go/no-go readiness before publishing |

## Rubric Plan

| Rubric | Required Checks |
| --- | --- |
| `source-inventory-rubric.md` | Required columns: Source, Type, Status, Owner, Decision |
| `gap-analysis-rubric.md` | Required columns: Gap, Source, Severity, Proposed Fix |
| `update-plan-rubric.md` | Required columns: File, Change, Source, Owner, Status |
| `docs-validation-rubric.md` | Required section: Go/No-Go Recommendation; minimum path count: 5 |

## Source Traceability Rules

- Every source inventory row should cite a file path, issue link, release note, or approved decision.
- Every gap should cite the source that proves the gap exists.
- Every planned change should cite the file it affects and the source that justifies the change.
- Assumptions should be labeled separately from source-backed facts.

## Scaffold Recommendation

Generate the workspace only after the rubric plan is accepted. Keep the first implementation file-first and do not automate edits until source inventory and update planning have been reviewed on a real documentation pass.
