# Dashboard Readiness

The dashboard should be a visual layer over the same filesystem workspace. It should not introduce a hidden database, a separate workflow state machine, or a new way to store agent output.

## Readiness Summary

ICM is ready for a dashboard prototype because the UI can answer four questions from local files and CLI checks:

| Question | Source Of Truth |
| --- | --- |
| What stage is active? | `icm status`, `icm next`, and `stages/*/CONTEXT.md` |
| What should the agent read and write? | The current stage contract |
| What needs human review? | Declared output files, `icm review` findings, and `shared/acceptance-log.md` |
| What needs repair before continuing? | `icm doctor` findings and suggested fixes |

The current CLI vocabulary and JSON output are stable enough for a read-only prototype. The first prototype now lives behind `icm dashboard`; a read/write dashboard should wait until the dashboard has proven the review queue and repair UX.

## MVP Views

| View | First Version Behavior | Must Not Hide |
| --- | --- | --- |
| Workspace Overview | List stages, current state, next action, and failed checks | Stage folder paths |
| Stage Detail | Show contract, declared inputs, declared outputs, Verify, and Review Gate | `CONTEXT.md` source |
| Review Queue | Group outputs that exist and have review findings | Output file path and rubric file path |
| Doctor Panel | Show failures, warnings, passes, and suggested fixes | The command that produced the finding |
| Artifact Shapes | Show source-inventory, calendar, and decision-log validity | The markdown table being checked |
| Decision Log | Show accepted, proposed, and superseded decisions | `shared/decision-log.md` |

## Review Queue Rules

A dashboard review queue should be deterministic:

1. Read every numbered stage folder.
2. Read the stage `CONTEXT.md`.
3. Identify declared outputs.
4. Include an output in the queue when the file exists and has content.
5. Attach `icm review` results for that stage.
6. Show a clear state: `not_started`, `needs_input`, `ready_for_review`, `blocked`, or `accepted`.

`accepted` comes from `shared/acceptance-log.md`. It should not be guessed from a passing review alone. A passing review means "machine checks passed"; a human still accepts the handoff.

## Artifact Failure UX

Common artifact-shape failures should become direct repair prompts:

| Failure | UI Repair Prompt |
| --- | --- |
| Source inventory missing columns | Add `Source`, `Type`, `Status`, and `Used For` columns |
| Calendar has fuzzy dates | Use `YYYY-MM-DD` dates for each milestone |
| Decision log missing rationale | Add `Date`, `Decision`, `Status`, and `Rationale` columns |
| Link/path count too low | Cite more upstream files or references |
| Required source missing | Add the required path or filename to the output |

The dashboard should show the exact markdown row or section that needs repair whenever possible.

## Current Data Contract

Use machine-readable command output for dashboard integrations:

```bash
icm status --json
icm review stages/01_discovery --workspace . --json
icm accept stages/01_discovery --workspace . --json
icm doctor . --json
```

Each JSON response includes:

| Field | Purpose |
| --- | --- |
| `workspace` | Absolute or relative workspace path |
| `stage` | Stage name when relevant |
| `state` | Stable machine state |
| `findings` | Fail, warn, and pass messages with source paths |
| `suggested_fix` | Beginner-facing repair text when available |
| `command` | CLI command that produced the result |
| `acceptance` | Human acceptance state read from `shared/acceptance-log.md` |

See [json-output.md](json-output.md) for command examples and response shapes. This keeps the dashboard honest: the UI displays the same facts the CLI knows.

## Prototype Boundary

Start with a local-only dashboard that reads a workspace folder and shells out to the CLI. The current implementation is documented in [dashboard-prototype.md](dashboard-prototype.md).

Do not start with:

- User accounts
- Cloud sync
- Provider configuration
- Multi-user permissions
- A database-backed workflow state
- A separate artifact editor format

## Acceptance Checklist

- A beginner can see the next action without reading every file.
- Every dashboard item links back to the markdown file it came from.
- A failed review shows the rubric or contract that produced the failure.
- The dashboard can be closed and the workspace still works through the CLI.
- The first prototype works against `examples/completed-documentation-refresh` and `examples/completed-project-plan`.
- The dashboard does not mark a handoff accepted without a row in `shared/acceptance-log.md`.
- Review and acceptance actions are copyable terminal commands, not hidden browser state.
