# Discovery Report

## Known Facts

- The target workflow turns a rough initiative into a reviewable project plan.
- Inputs arrive as sponsor notes, roadmap items, constraints, stakeholder requests, and prior decisions.
- Milestone dates are high-risk because vague dates make downstream work look more certain than it is.
- Review gates matter because planning errors are cheapest to fix before contributors commit work.
- Traceability matters because every major milestone should point back to a source, constraint, or approved decision.

## Assumptions

- Markdown tables are enough for source inventory, milestone mapping, and risk review.
- One sponsor can approve scope, owners, and target dates.
- The first workflow should produce a plan and review pack rather than create implementation tickets automatically.
- A lightweight decision log is enough until the project has repeated planning cycles.

## Open Questions

- Which roadmap items are mandatory for the first milestone?
- Should risks block the plan or stay as watch items?
- How much stakeholder detail should be preserved in the public project plan?

## Source Traceability

| Source | Used For |
| --- | --- |
| `../00_intake/output/project-brief.md` | Goal, audience, constraints, and review points |
| `references/discovery-question-bank.md` | Discovery coverage and workflow prompts |
| `../../_config/quality-gates.md` | Review expectations and source-traceability standards |

## Users And Reviewers

| Role | Need | Review Concern |
| --- | --- | --- |
| Project owner | Turn a rough initiative into a concrete plan | Missing constraints or unclear owners |
| Contributor | Understand dates, responsibilities, and dependencies | Ambiguous scope or changing priorities |
| Sponsor | Approve scope and risk before work starts | Unsourced commitments or hidden assumptions |

## Candidate Workflow

1. Capture initiative goal, sponsor, stakeholders, target window, and constraints.
2. Inventory source material and classify constraint, request, risk, and decision inputs.
3. Map milestones, owners, dependencies, and review gates.
4. Create a project plan with source traceability, owner, status, and risk level.
5. Package decisions, tradeoffs, and unresolved questions for approval.
6. Validate that every milestone cites a source, constraint, or accepted decision.

## Candidate Layer 3 Material

| File | Purpose |
| --- | --- |
| `_config/planning-rules.md` | Stable planning standards, status labels, and ownership rules |
| `_config/risk-policy.md` | Rules for blocker, watch, and accepted-risk decisions |
| `shared/decision-log.md` | Accepted planning decisions across project cycles |
| `stages/01_source_inventory/references/source-types.md` | Source classification guidance |
| `stages/05_validation/references/project-validation-rubric.md` | Required checks before approving the plan |

## Candidate Layer 4 Artifacts

| Artifact | Produced By | Consumed By |
| --- | --- | --- |
| `project-brief.md` | Intake | Source inventory |
| `source-inventory.md` | Source inventory | Gap analysis |
| `milestone-map.md` | Milestone mapping | Project plan |
| `project-plan.md` | Project plan | Review pack |
| `review-pack.md` | Review pack | Validation |
| `validation-report.md` | Validation | Human go/no-go decision |

## Risks

| Risk | Mitigation |
| --- | --- |
| Project scope expands after planning starts | Require sponsor review before adding milestones |
| Dates are invented without capacity evidence | Require source or decision citations for target dates |
| Risks stay buried in prose | Use a risk table and decision log before approval |
| Source inventory becomes stale | Treat source inventory as a per-planning-cycle artifact |

## Discovery Recommendation

Proceed to stage mapping with a six-stage project-planning workflow. Keep the first version markdown-only, make source traceability explicit, and use rubric checks for required table columns, cited path counts, calendars, and decision logs.
