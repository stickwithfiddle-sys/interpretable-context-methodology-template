# Stage Map

## Proposed Stages

| Stage | Purpose | Inputs | Output | Review Gate | Validation |
| --- | --- | --- | --- | --- | --- |
| `00_intake` | Capture initiative goal, sponsor, audience, and constraints | Project profile, prior decisions | `project-brief.md` | Confirm scope and authority | Brief names desired outcome, users, success criteria, and natural review points |
| `01_source_inventory` | Inventory source material and classify constraints, requests, risks, and decisions | Intake, source rules | `source-inventory.md` | Confirm important sources are not missing | Each source has path, type, status, and use |
| `02_milestone_mapping` | Turn sources into milestones, owners, dependencies, and review gates | Source inventory, planning rules | `milestone-map.md` | Confirm sequence and dependencies | Each milestone has owner, status, and source reference |
| `03_project_plan` | Turn milestones into an executable plan | Milestone map, risk policy | `project-plan.md` | Approve scope before work starts | Every action has owner, status, source, and risk level |
| `04_review_pack` | Summarize decisions, risks, tradeoffs, and open questions | Project plan, decision log | `review-pack.md` | Approve, request changes, or block start | Pack separates accepted decisions from unresolved questions |
| `05_validation` | Check traceability and readiness before starting work | Review pack, validation rubric | `validation-report.md` | Go/no-go decision | Every milestone traces to source, decision, or assumption |

## Handoff Chain

```text
project-brief.md
  -> source-inventory.md
  -> milestone-map.md
  -> project-plan.md
  -> review-pack.md
  -> validation-report.md
```

## Stable Reference Material

| File | Used By |
| --- | --- |
| `_config/planning-rules.md` | Milestone mapping, project plan, review pack |
| `_config/risk-policy.md` | Project plan, validation |
| `shared/decision-log.md` | All downstream stages |
| `stages/01_source_inventory/references/source-types.md` | Source inventory |
| `stages/05_validation/references/project-validation-rubric.md` | Validation |

## Review Strategy

- Source inventory catches missing constraints before planning work.
- Milestone mapping prevents implementation work from starting before dependencies are visible.
- Project plan review keeps ownership, dates, and risks inspectable.
- Validation checks table shape, source references, calendar dates, and open decisions before work starts.

## Stage Mapping Recommendation

Approve this six-stage map for scaffold planning. Keep validators deterministic first: required columns, required source paths, minimum cited path counts, ISO calendar dates, and decision-log shape.
