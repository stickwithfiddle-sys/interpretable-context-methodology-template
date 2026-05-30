# Setup Questionnaire

## Required Answers

1. Which docs are in scope for this refresh?
2. Which release or product milestone triggered the refresh?
3. Who approves beginner-facing install instructions?
4. Which files are source of truth when README, docs site, and changelog disagree?
5. What evidence is required before a command changes?

## Source Inventory Questions

| Question | Why It Matters | Suggested Source |
| --- | --- | --- |
| Which files should be inventoried first? | Keeps the first run focused | `README.md`, `docs/install.md`, `docs/index.html` |
| Which docs are generated or derived? | Prevents editing generated content manually | `docs/release-process.md` |
| Which release notes prove current behavior? | Grounds updates in shipped changes | `CHANGELOG.md` |
| Which pages are beginner-critical? | Prioritizes first-run success | `docs/first-workspace.md` |

## Rubric Tuning Questions

1. Should source inventory require `Owner`, or is `Reviewer` clearer?
2. Should path counts include external links or only repo-local paths?
3. Should missing screenshots be a validation failure or a warning?
4. Which placeholder terms should be forbidden beyond `TBD` and `lorem ipsum`?

## Review Preferences

| Preference | Default |
| --- | --- |
| Source citation format | Backticked repo-relative paths |
| Gap severity labels | High, Medium, Low |
| Status labels | Proposed, Accepted, Blocked, Done |
| Review style | Approve, request changes, or block |

## Questionnaire Recommendation

Answer the required questions before creating the project-specific workspace. If source-of-truth priority is unclear, write a decision-log entry before the first source inventory stage runs.
