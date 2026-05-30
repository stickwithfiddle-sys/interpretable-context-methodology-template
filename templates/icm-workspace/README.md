# {{PROJECT_NAME}}

This is an Interpretable Context Methodology workspace created on {{CREATED_DATE}}.

The workspace uses folders, markdown contracts, and local scripts as the agent orchestration layer. Start at `AGENTS.md`, then read `CONTEXT.md`, then run stages in numbered order.

## Run The Builder

1. Fill `stages/00_intake/output/project-brief.md`.
2. Run one stage at a time.
3. Review and edit each stage's `output/` files before continuing.
4. Update `_config/` or stage `references/` when repeated output edits reveal a source-level improvement.

## Validate

```powershell
python tools/validate_icm_workspace.py . --strict
```

## Layer Map

| Layer | Location | Purpose |
| --- | --- | --- |
| 0 | `AGENTS.md` | Agent identity and workspace operating rules |
| 1 | `CONTEXT.md` | Stage routing and shared resources |
| 2 | `stages/*/CONTEXT.md` | Stage-specific contracts |
| 3 | `_config/`, `shared/`, `stages/*/references/` | Stable reference material |
| 4 | `stages/*/output/` | Per-run artifacts and handoffs |