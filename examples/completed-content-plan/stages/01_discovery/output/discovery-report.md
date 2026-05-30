# Discovery Report

## Known Facts

- The target workflow produces a weekly content plan.
- Inputs arrive as rough ideas, source links, notes, and current priorities.
- The user wants review gates before drafting begins.
- Traceability matters because public content should not contain unsourced claims.
- The first implementation should stay model-neutral and file-based.

## Assumptions

- A weekly cadence is frequent enough that repeatability matters.
- One human reviewer is available to approve themes and the final plan.
- Markdown tables are sufficient for early planning artifacts.
- Channel-specific formatting can wait until the core workflow is stable.

## Open Questions

- Which publishing channels are in scope for the first project-specific workspace?
- Should scoring use a numeric rubric or a simple high/medium/low priority label?
- Should final validation check only structure, or also source coverage per content item?

## Users And Reviewers

| Role | Need | Review Concern |
| --- | --- | --- |
| Builder or editor | Turn messy inputs into a usable plan | Too much process for a weekly task |
| Reviewer | Approve topics and priorities quickly | Hidden assumptions or weak sources |
| Reader | Receive useful and accurate content | Unsourced or irrelevant claims |

## Candidate Workflow

1. Capture the planning week, goals, inputs, and constraints.
2. Inventory raw content inputs and normalize them into a consistent table.
3. Select weekly themes and reject low-fit ideas.
4. Assemble a calendar plan with owner, channel, source, and review status.
5. Produce a review pack for human approval.
6. Validate traceability and readiness before drafting.

## Candidate Layer 3 Material

| File | Purpose |
| --- | --- |
| `_config/editorial-rules.md` | Stable tone, claims, and sourcing rules |
| `_config/channel-guide.md` | Channel-specific length and format preferences |
| `shared/decision-log.md` | Decisions that should affect future plans |
| `stages/02_theme_selection/references/theme-rubric.md` | Criteria for choosing weekly themes |
| `stages/05_validation/references/source-checklist.md` | Minimum source and readiness checks |

## Candidate Layer 4 Artifacts

| Artifact | Produced By | Consumed By |
| --- | --- | --- |
| `planning-brief.md` | Intake | Source inventory |
| `source-inventory.md` | Source inventory | Theme selection |
| `theme-selection.md` | Theme selection | Calendar planning |
| `content-calendar.md` | Calendar planning | Review pack |
| `review-pack.md` | Review pack | Validation |
| `validation-report.md` | Validation | Human go/no-go decision |

## Risks

| Risk | Mitigation |
| --- | --- |
| Weak source material slips into the final plan | Require source notes and validation checks |
| Workflow becomes too heavy for weekly use | Keep stages small and artifacts table-driven |
| Review happens too late | Add review gates after theme selection and review pack |
| Editorial preferences stay trapped in chat | Store stable preferences in `_config/editorial-rules.md` |

## Discovery Recommendation

Proceed to stage mapping with a six-stage workflow. Keep the first version markdown-only, with optional scripts added later for date and source coverage checks.
