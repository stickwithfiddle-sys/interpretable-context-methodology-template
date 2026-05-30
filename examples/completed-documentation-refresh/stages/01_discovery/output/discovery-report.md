# Discovery Report

## Known Facts

- The target workflow refreshes documentation after product changes.
- Inputs arrive as markdown docs, release notes, roadmap items, support questions, and package metadata.
- Install instructions are high-risk because stale commands block beginners immediately.
- Review gates matter because documentation edits can accidentally overstate product readiness.
- Traceability matters because every proposed change should point back to a source file, release note, or approved decision.

## Assumptions

- Markdown tables are enough for source inventory and gap analysis.
- One maintainer can review source classifications and update priorities.
- The first workflow should plan doc edits rather than rewriting files automatically.
- Screenshots can be refreshed later if command text has already been verified.

## Open Questions

- Which documentation page should be the canonical first-run guide?
- Should release notes be treated as higher authority than the roadmap?
- How much historical context should stay visible after a workflow becomes simpler?

## Source Traceability

| Source | Used For |
| --- | --- |
| `../00_intake/output/project-brief.md` | Goal, audience, constraints, and review points |
| `references/discovery-question-bank.md` | Discovery coverage and workflow prompts |
| `../../_config/quality-gates.md` | Review expectations and source-traceability standards |

## Users And Reviewers

| Role | Need | Review Concern |
| --- | --- | --- |
| Maintainer | Find stale docs quickly | Missing source files or too many manual checks |
| Beginner | Install and run ICM without guessing | Outdated commands or jargon-heavy explanation |
| Product reviewer | Confirm docs match release state | Unsourced claims or hidden assumptions |

## Candidate Workflow

1. Capture docs goal, audience, release context, and constraints.
2. Inventory source docs and classify source-of-truth status.
3. Compare current docs against source material and identify gaps.
4. Create an update plan with owner, status, and source traceability.
5. Package risky decisions and unresolved questions for review.
6. Validate that every planned change cites a source path or approved decision.

## Candidate Layer 3 Material

| File | Purpose |
| --- | --- |
| `_config/docs-style-guide.md` | Stable style, tone, and beginner-language rules |
| `_config/source-priority.md` | Rules for choosing source of truth when docs disagree |
| `shared/decision-log.md` | Accepted documentation decisions across releases |
| `stages/01_source_inventory/references/source-types.md` | Source classification guidance |
| `stages/05_validation/references/docs-validation-rubric.md` | Required checks before publishing docs |

## Candidate Layer 4 Artifacts

| Artifact | Produced By | Consumed By |
| --- | --- | --- |
| `docs-refresh-brief.md` | Intake | Source inventory |
| `source-inventory.md` | Source inventory | Gap analysis |
| `gap-analysis.md` | Gap analysis | Update plan |
| `docs-update-plan.md` | Update plan | Review pack |
| `review-pack.md` | Review pack | Validation |
| `validation-report.md` | Validation | Human go/no-go decision |

## Risks

| Risk | Mitigation |
| --- | --- |
| Install docs drift from the package release | Require package metadata and README citations |
| A rewrite hides unresolved product decisions | Keep open decisions in the review pack |
| Beginner docs become too abstract | Keep the first path command-driven |
| Source inventory becomes stale | Treat source inventory as a per-release artifact |

## Discovery Recommendation

Proceed to stage mapping with a six-stage documentation refresh workflow. Keep the first version markdown-only, make source traceability explicit, and use rubric checks for required table columns and cited path counts.
