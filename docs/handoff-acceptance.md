# Handoff Acceptance

ICM separates machine checks from human acceptance.

- `icm review` means deterministic checks passed or failed.
- `icm accept` means a human reviewed the handoff and approved it.
- `shared/acceptance-log.md` is the plain-file source of truth.

## Accept A Stage

After a stage review passes, accept the handoff:

```bash
icm review stages/00_intake
icm accept stages/00_intake --reviewer Hobo --note "Brief is ready for discovery."
```

`icm accept` appends a row to `shared/acceptance-log.md`:

```markdown
| Date | Stage | Output | Reviewer | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-05-31 | 00_intake | stages/00_intake/output/project-brief.md | Hobo | Accepted | Brief is ready for discovery. |
```

You can edit that file directly. The dashboard and CLI read the file instead of storing hidden state.

## Check Acceptance

```bash
icm status .
icm review stages/00_intake --json
icm dashboard .
```

`icm status` shows accepted output counts. `icm review --json` includes an `acceptance` object. The dashboard shows the difference between `machine passing` and `accepted`.

## Override Carefully

By default, `icm accept` refuses to accept a handoff when review checks fail.

Use this only when a human explicitly accepts the residual risk:

```bash
icm accept stages/00_intake --allow-failing-review --note "Accepted with known gaps."
```

The override still writes to `shared/acceptance-log.md`, so the decision remains visible.
