# Scaffold Plan

## Proposed Workspace Tree

```text
content-planning-workspace/
  AGENTS.md
  CONTEXT.md
  README.md
  _config/
    project-profile.md
    editorial-rules.md
    channel-guide.md
    quality-gates.md
  shared/
    decision-log.md
    glossary.md
    backlog.md
  stages/
    00_intake/
      CONTEXT.md
      references/intake-checklist.md
      output/planning-brief.md
    01_source_inventory/
      CONTEXT.md
      references/source-rules.md
      output/source-inventory.md
    02_theme_selection/
      CONTEXT.md
      references/theme-rubric.md
      output/theme-selection.md
    03_calendar_plan/
      CONTEXT.md
      references/calendar-rules.md
      output/content-calendar.md
    04_review_pack/
      CONTEXT.md
      references/review-pack-template.md
      output/review-pack.md
    05_validation/
      CONTEXT.md
      references/source-checklist.md
      output/validation-report.md
  tools/
    validate_icm_workspace.py
```

## Stage Contract Summary

| Stage | Contract Notes |
| --- | --- |
| `00_intake` | Convert the weekly planning request into `planning-brief.md`. Keep open questions visible. |
| `01_source_inventory` | Normalize raw ideas and links. Mark source quality and missing context. |
| `02_theme_selection` | Choose themes using the rubric. Reject or defer low-fit ideas. |
| `03_calendar_plan` | Assign dates, channels, owners, and source links. |
| `04_review_pack` | Summarize the plan for approval and list risks. |
| `05_validation` | Check traceability, required fields, and go/no-go readiness. |

## Stable Reference Files

| File | Initial Contents |
| --- | --- |
| `_config/editorial-rules.md` | Tone, sourcing expectations, claim policy, and reviewer preferences |
| `_config/channel-guide.md` | Channel names, length targets, cadence, and formatting constraints |
| `_config/quality-gates.md` | Required review checks for each artifact |
| `shared/decision-log.md` | Cross-week decisions that should persist |

## Deterministic Checks To Add Later

- Check that every content calendar row has a date, channel, owner, and source.
- Check that every planned item has status `approved`, `needs-change`, or `blocked`.
- Check that no final plan item has source status `missing`.

## Scaffold Recommendation

Approve this scaffold for a first project-specific workspace. Keep validation script additions as a follow-up after the content calendar table format is tested once.
