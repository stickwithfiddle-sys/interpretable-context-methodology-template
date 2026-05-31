# Scaffold Plan

## Proposed Workspace Tree

```text
project-plan-workspace/
  AGENTS.md
  CONTEXT.md
  _config/
    planning-rules.md
    risk-policy.md
    quality-gates.md
  shared/
    decision-log.md
    backlog.md
  stages/
    00_intake/
      CONTEXT.md
      output/project-brief.md
    01_source_inventory/
      CONTEXT.md
      references/source-types.md
      references/source-inventory-rubric.md
      output/source-inventory.md
    02_milestone_mapping/
      CONTEXT.md
      references/milestone-rules.md
      output/milestone-map.md
    03_project_plan/
      CONTEXT.md
      references/project-plan-rubric.md
      output/project-plan.md
    04_review_pack/
      CONTEXT.md
      references/review-pack-template.md
      output/review-pack.md
    05_validation/
      CONTEXT.md
      references/project-validation-rubric.md
      output/validation-report.md
```

## Stage Responsibilities

| Stage | Responsibility |
| --- | --- |
| `00_intake` | Capture initiative goal, sponsor, audience, target window, and constraints |
| `01_source_inventory` | Classify sponsor notes, roadmap items, requests, risks, and decisions before planning |
| `02_milestone_mapping` | Identify milestones, owners, dependencies, and review gates |
| `03_project_plan` | Produce concrete planned work with owner, status, source, and risk |
| `04_review_pack` | Package risks, tradeoffs, and unresolved questions for approval |
| `05_validation` | Check traceability and go/no-go readiness before starting work |

## Rubric Plan

| Rubric | Required Checks |
| --- | --- |
| `source-inventory-rubric.md` | Required shape: source-inventory |
| `milestone-map-rubric.md` | Required columns: Milestone, Owner, Dependency, Source, Status |
| `project-plan-rubric.md` | Required columns: Work Item, Owner, Source, Risk, Status |
| `project-validation-rubric.md` | Required section: Go/No-Go Recommendation; minimum path count: 5 |

## Source Traceability Rules

- Every source inventory row should cite a file path, issue link, stakeholder note summary, or approved decision.
- Every milestone should cite the source that justifies the work.
- Every planned work item should cite the source that justifies scope, owner, or date.
- Assumptions should be labeled separately from source-backed facts.

## Scaffold Recommendation

Generate the workspace only after the rubric plan is accepted. Keep the first implementation file-first and do not automate project-management tickets until source inventory and project planning have been reviewed on a real initiative.
