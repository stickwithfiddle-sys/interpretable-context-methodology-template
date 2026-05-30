# Stage Map

## Proposed Stages

| Stage | Purpose | Inputs | Output | Review Gate | Validation |
| --- | --- | --- | --- | --- | --- |
| `00_intake` | Capture docs goal, audience, release context, and constraints | Project profile, prior decisions | `docs-refresh-brief.md` | Confirm scope and audience | Brief names desired outcome, users, success criteria, and natural review points |
| `01_source_inventory` | Inventory source docs and classify source-of-truth status | Intake, source rules | `source-inventory.md` | Confirm important docs are not missing | Each source has path, type, status, owner, and use decision |
| `02_gap_analysis` | Compare current docs with release/source material | Source inventory, release notes | `gap-analysis.md` | Confirm gaps are real and prioritized | Every gap cites at least one source path |
| `03_update_plan` | Turn gaps into concrete documentation actions | Gap analysis, style guide | `docs-update-plan.md` | Approve edits before writing | Every action has owner, status, source, and risk level |
| `04_review_pack` | Summarize decisions, risks, and open questions | Update plan, decision log | `review-pack.md` | Approve, request changes, or block release | Pack separates accepted decisions from unresolved questions |
| `05_validation` | Check traceability and readiness before publishing | Review pack, validation rubric | `validation-report.md` | Go/no-go decision | Every planned change traces to source, decision, or assumption |

## Handoff Chain

```text
docs-refresh-brief.md
  -> source-inventory.md
  -> gap-analysis.md
  -> docs-update-plan.md
  -> review-pack.md
  -> validation-report.md
```

## Stable Reference Material

| File | Used By |
| --- | --- |
| `_config/docs-style-guide.md` | Gap analysis, update plan, review pack |
| `_config/source-priority.md` | Source inventory, validation |
| `shared/decision-log.md` | All downstream stages |
| `stages/01_source_inventory/references/source-types.md` | Source inventory |
| `stages/05_validation/references/docs-validation-rubric.md` | Validation |

## Review Strategy

- Source inventory catches missing docs before planning work.
- Gap analysis prevents rewrite work from starting before source disagreements are visible.
- Update plan review keeps final edits scoped and traceable.
- Validation checks table shape, source references, and open decisions before publishing.

## Stage Mapping Recommendation

Approve this six-stage map for scaffold planning. Keep validators deterministic first: required columns, required source paths, and minimum cited path counts.
