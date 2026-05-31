# Dashboard Direction

Last updated: 2026-05-31

The dashboard should not replace the filesystem workspace. It should make the same files easier to inspect, review, and eventually edit.

For a more implementation-oriented checklist, see [dashboard-readiness.md](dashboard-readiness.md). The current read-only prototype is documented in [dashboard-prototype.md](dashboard-prototype.md).

## Readiness Criteria

The read-only prototype is ready because these are true:

- The CLI status model is stable enough to expose visually.
- `icm doctor` explains most beginner problems without needing source-code knowledge.
- At least three example workspaces show different real use cases.
- Review checks can distinguish structure problems from artifact-quality problems.
- The docs site explains the core flow without relying on a live demo.
- The CLI exposes status, review, and doctor findings in a machine-readable form.

## MVP Shape

The first dashboard is local-first and read-only. It shows acceptance from `shared/acceptance-log.md`. A later dashboard can write to the current workspace folder after command-copy and edit boundaries are clear.

| View | Purpose |
| --- | --- |
| Workspace Overview | Show stages, current state, missing outputs, and likely next action |
| Stage Detail | Show the stage contract, declared inputs, output files, and review gate |
| Review Queue | List outputs that are ready for human review |
| Acceptance State | Show machine-passing outputs separately from accepted handoffs |
| Doctor Panel | Run structure and content checks with suggested fixes |
| Artifact Shapes | Show source-inventory, calendar, and decision-log failures with the exact markdown table path |
| Decision Log | Show cross-stage decisions without hiding the underlying markdown |

## Product Rules

- Files remain authoritative.
- No database is required for the first dashboard.
- The UI should never hide where an output lives on disk.
- A user should be able to close the dashboard and keep working with only the CLI.
- Dashboard actions should map to CLI verbs wherever possible.
- Passing machine checks should not automatically mean a handoff is accepted; acceptance comes from `shared/acceptance-log.md`.

## Not Yet

Do not start with authentication, cloud sync, provider configuration, or multi-user collaboration. Those may matter later, but they would make the first useful product harder to finish and harder for beginners to understand.
