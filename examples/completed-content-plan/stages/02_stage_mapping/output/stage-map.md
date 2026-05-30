# Stage Map

## Proposed Project-Specific Workflow

| Stage | Purpose | Primary Inputs | Main Output | Review Gate | Verify |
| --- | --- | --- | --- | --- | --- |
| `00_intake` | Capture weekly goal, channels, constraints, and raw input locations | Project profile, prior decisions | `planning-brief.md` | Confirm week, audience, channels, and constraints | Brief names goal, audience, inputs, and open questions |
| `01_source_inventory` | Normalize rough ideas and links into a source inventory | Planning brief, source rules | `source-inventory.md` | Confirm no important source is missing | Every source has type, note, and status |
| `02_theme_selection` | Choose weekly themes and reject low-fit ideas | Source inventory, theme rubric | `theme-selection.md` | Approve selected themes before calendar planning | Each selected theme has rationale and supporting inputs |
| `03_calendar_plan` | Turn approved themes into dated content items | Theme selection, channel guide | `content-calendar.md` | Confirm dates, channels, and owners | Every item has channel, date, source, owner, and status |
| `04_review_pack` | Package the plan for human approval | Content calendar, editorial rules | `review-pack.md` | Approve, request changes, or block drafting | Pack lists decisions, risks, and open questions |
| `05_validation` | Check readiness and traceability before drafting | Review pack, source checklist | `validation-report.md` | Go/no-go decision | Every planned item traces to a source or approved decision |

## Handoff Pattern

```text
planning-brief.md
  -> source-inventory.md
  -> theme-selection.md
  -> content-calendar.md
  -> review-pack.md
  -> validation-report.md
```

## Layer 3 Files To Seed

| File | Used By |
| --- | --- |
| `_config/editorial-rules.md` | Theme selection, review pack, validation |
| `_config/channel-guide.md` | Calendar planning |
| `shared/decision-log.md` | All stages |
| `stages/02_theme_selection/references/theme-rubric.md` | Theme selection |
| `stages/05_validation/references/source-checklist.md` | Validation |

## Review Gate Rationale

- Theme selection is the cheapest place to correct direction.
- Review pack is the cheapest place to correct the calendar before drafting.
- Validation prevents weakly sourced items from moving into production.

## Recommendation

Approve this map for scaffold planning. Do not add channel-specific drafting stages until the planning workflow has been used at least once.
