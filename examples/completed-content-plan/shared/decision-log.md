# Decision Log

Record decisions that should influence future stage runs.

| Date | Decision | Why | Affected Stages | Source Files To Update |
| --- | --- | --- | --- | --- |
| 2026-05-30 | Keep the content workflow to six stages | Six stages give clear review gates without over-fragmenting the work | `02_stage_mapping`, `03_scaffold` | `stages/02_stage_mapping/output/stage-map.md` |
| 2026-05-30 | Require source traceability before final planning | Unsourced claims are the highest-risk failure mode for a public content plan | All downstream stages | `_config/quality-gates.md`, future `references/source-rules.md` |
