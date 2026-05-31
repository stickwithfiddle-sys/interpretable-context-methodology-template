# JSON Output

Use JSON output when another tool needs to read ICM workspace state without scraping terminal text.

The human CLI output remains the default. Add `--json` when building dashboard, TUI, editor, or automation integrations.

## Commands

```bash
icm status examples/completed-content-plan --json
icm review stages/01_discovery --workspace examples/completed-content-plan --json
icm accept stages/01_discovery --workspace examples/completed-content-plan --json
icm doctor examples/completed-content-plan --json
```

## Shared Fields

Each JSON response includes:

| Field | Meaning |
| --- | --- |
| `command` | The CLI command shape that produced the response |
| `workspace` | Absolute workspace path |
| `passed` | Whether the command checks passed |

Paths inside stage lists are workspace-relative so a UI can link back to the source file without hiding the filesystem.

## Status Shape

`icm status --json` returns stage state and the likely next action:

```json
{
  "command": "icm status /path/to/workspace --json",
  "workspace": "/path/to/workspace",
  "passed": true,
  "next_action": {
    "type": "review_or_accept_handoff",
    "message": "Review and accept the declared outputs in stages/01_discovery."
  },
  "stages": [
    {
      "name": "01_discovery",
      "path": "stages/01_discovery",
      "state": "ready_for_review",
      "note": "Declared outputs are present; review before continuing.",
      "declared_outputs": ["discovery-report.md"],
      "existing_outputs": ["discovery-report.md"],
      "missing_outputs": [],
      "accepted_outputs": [],
      "pending_acceptance_outputs": ["discovery-report.md"],
      "acceptance": {
        "accepted": false,
        "accepted_outputs": [],
        "pending_outputs": ["discovery-report.md"],
        "log_path": "shared/acceptance-log.md"
      }
    }
  ]
}
```

Common `next_action.type` values:

| Type | Meaning |
| --- | --- |
| `run_doctor` | No stages were found |
| `fill_intake` | The intake brief needs content |
| `review_or_accept_handoff` | Declared outputs exist but need human acceptance |
| `run_or_repair_stage` | A stage is missing contract or output work |
| `review_or_restart` | Declared outputs are accepted or no next stage is blocked |

## Review Shape

`icm review --json` returns the same findings as the text output, plus summary counts and repair suggestions for failures or warnings:

```json
{
  "command": "icm review stages/01_discovery --workspace /path/to/workspace --json",
  "workspace": "/path/to/workspace",
  "target": "stages/01_discovery",
  "stage": "01_discovery",
  "stage_path": "stages/01_discovery",
  "output_path": null,
  "passed": true,
  "summary": {
    "fail": 0,
    "warn": 0,
    "pass": 33
  },
  "findings": [
    {
      "level": "PASS",
      "message": "Contract has required heading: Inputs",
      "suggested_fix": null
    }
  ],
  "acceptance": {
    "accepted": false,
    "log_path": "shared/acceptance-log.md",
    "outputs": [
      {
        "path": "stages/01_discovery/output/discovery-report.md",
        "accepted": false,
        "status": "Pending",
        "date": null,
        "reviewer": null,
        "notes": null
      }
    ]
  },
  "next_actions": []
}
```

## Accept Shape

`icm accept --json` appends to `shared/acceptance-log.md` and returns the rows it recorded:

```json
{
  "command": "icm accept stages/01_discovery --workspace /path/to/workspace --json",
  "workspace": "/path/to/workspace",
  "target": "stages/01_discovery",
  "accepted": true,
  "log_path": "shared/acceptance-log.md",
  "entries": [
    {
      "date": "2026-05-31",
      "stage": "01_discovery",
      "output": "stages/01_discovery/output/discovery-report.md",
      "reviewer": "Hobo",
      "status": "Accepted",
      "notes": "Approved for stage mapping."
    }
  ]
}
```

## Doctor Shape

`icm doctor --json` combines structure validation, content checks, stage states, and the next action:

```json
{
  "command": "icm doctor /path/to/workspace --json",
  "workspace": "/path/to/workspace",
  "passed": true,
  "structure": {
    "passed": true,
    "strict_passed": true,
    "errors": [],
    "warnings": [],
    "findings": []
  },
  "content": {
    "passed": true,
    "strict_passed": true,
    "findings": []
  },
  "stages": [
    {
      "name": "01_discovery",
      "path": "stages/01_discovery",
      "state": "ready_for_review",
      "accepted_outputs": [],
      "pending_acceptance_outputs": ["discovery-report.md"]
    }
  ],
  "next_action": {
    "type": "review_or_accept_handoff",
    "message": "Review and accept the declared outputs in stages/01_discovery."
  }
}
```

## Integration Rules

- Treat markdown files as authoritative.
- Use JSON for reading state, not for storing separate workflow state.
- Treat `passed: true` as "machine checks passed," not as human acceptance.
- Treat `shared/acceptance-log.md` as the source of truth for human acceptance.
- Use `next_action` for guidance, but let the user choose when to proceed.
- Show `suggested_fix` only for findings where it is not null.
