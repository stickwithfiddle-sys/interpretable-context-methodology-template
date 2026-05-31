# JSON Output

Use JSON output when another tool needs to read ICM workspace state without scraping terminal text.

The human CLI output remains the default. Add `--json` when building dashboard, TUI, editor, or automation integrations.

## Commands

```bash
icm status examples/completed-content-plan --json
icm review stages/01_discovery --workspace examples/completed-content-plan --json
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
    "type": "review_or_restart",
    "message": "All declared outputs are present. Review the latest output or start a new run."
  },
  "stages": [
    {
      "name": "01_discovery",
      "path": "stages/01_discovery",
      "state": "ready_for_review",
      "note": "Declared outputs are present; review before continuing.",
      "declared_outputs": ["discovery-report.md"],
      "existing_outputs": ["discovery-report.md"],
      "missing_outputs": []
    }
  ]
}
```

Common `next_action.type` values:

| Type | Meaning |
| --- | --- |
| `run_doctor` | No stages were found |
| `fill_intake` | The intake brief needs content |
| `run_or_repair_stage` | A stage is missing contract or output work |
| `review_or_restart` | Declared outputs are present |

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
  "next_actions": []
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
      "state": "ready_for_review"
    }
  ],
  "next_action": {
    "type": "review_or_restart",
    "message": "All declared outputs are present. Review the latest output or start a new run."
  }
}
```

## Integration Rules

- Treat markdown files as authoritative.
- Use JSON for reading state, not for storing separate workflow state.
- Treat `passed: true` as "machine checks passed," not as human acceptance.
- Use `next_action` for guidance, but let the user choose when to proceed.
- Show `suggested_fix` only for findings where it is not null.
