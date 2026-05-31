# Setup Questionnaire

## Required Answers

1. Which initiative is in scope for this planning pass?
2. Which sponsor or decision-maker approves scope, dates, and risk?
3. Which target date or milestone window matters most?
4. Which constraints are hard blockers versus preferences?
5. What evidence is required before a milestone becomes committed?

## Source Inventory Questions

| Question | Why It Matters | Suggested Source |
| --- | --- | --- |
| Which source files or notes should be inventoried first? | Keeps the first run focused | `ROADMAP.md`, `shared/decision-log.md`, sponsor notes |
| Which requests are requirements versus nice-to-haves? | Prevents scope creep | Sponsor brief or stakeholder notes |
| Which risks must block planning approval? | Keeps risk review explicit | `_config/risk-policy.md` |
| Which dates are fixed externally? | Prevents invented commitments | Roadmap, launch window, or dependency notes |

## Rubric Tuning Questions

1. Should milestone tables require `Dependency`, or is `Blocked By` clearer?
2. Should path counts include external links or only repo-local paths?
3. Should unowned milestones fail validation or stay as review warnings?
4. Which placeholder terms should be forbidden beyond `TBD` and `lorem ipsum`?

## Review Preferences

| Preference | Default |
| --- | --- |
| Source citation format | Backticked repo-relative paths |
| Risk labels | Blocker, Watch, Accepted |
| Status labels | Proposed, Accepted, Blocked, Done |
| Review style | Approve, request changes, or block |

## Questionnaire Recommendation

Answer the required questions before creating the project-specific workspace. If scope authority or date confidence is unclear, write a decision-log entry before the first milestone-mapping stage runs.
