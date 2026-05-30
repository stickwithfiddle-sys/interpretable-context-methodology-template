# Stage 03: Scaffold

## Purpose

Convert the approved stage map into a concrete project workspace structure and draft stage contracts.

## Inputs

| Layer | Path | Use |
| --- | --- | --- |
| Layer 3 | `../../_templates/stage-context.md` | Canonical stage contract template |
| Layer 3 | `../../_templates/project-readme.md` | Project README shape |
| Layer 3 | `references/scaffold-rules.md` | Folder and naming rules |
| Layer 4 | `../02_stage_mapping/output/stage-map.md` | Approved stage map |

## Process

1. Translate each mapped stage into a folder name, contract, references folder, and output folder.
2. Define root files required for the project-specific workspace.
3. Name shared Layer 3 files that should exist at setup.
4. Identify local scripts that would make validation deterministic.
5. Keep the scaffold plan reviewable before any files are generated.

## Outputs

| File | Location | Purpose |
| --- | --- | --- |
| `scaffold-plan.md` | `output/` | Proposed folder tree, files, and contracts |

## Review Gate

Before continuing, a human should approve the proposed tree and confirm it is small enough to maintain.

## Verify

- Confirm `output/scaffold-plan.md` exists.
- Confirm every proposed stage has `CONTEXT.md`, `references/`, and `output/`.
- Confirm the scaffold avoids project-specific vendor lock-in unless explicitly required.