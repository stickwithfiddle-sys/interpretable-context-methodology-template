# Research Brief Example Agent Guide

You are operating inside an Interpretable Context Methodology workspace. The folder structure is the workflow architecture.

## Context Loading Order

1. Read this file for Layer 0 workspace identity.
2. Read `CONTEXT.md` for Layer 1 routing.
3. Read the selected stage's `CONTEXT.md` for Layer 2 instructions.
4. Load only the Layer 3 reference files listed in that stage's Inputs section.
5. Load only the Layer 4 working artifacts listed in that stage's Inputs section.

Do not load the whole workspace by default. Stage contracts decide what context matters.

## Operating Rules

- Treat each numbered folder under `stages/` as a single workflow stage.
- Write stage outputs only to that stage's `output/` folder unless the stage contract says otherwise.
- Keep stable preferences, standards, and domain rules in `_config/`, `shared/`, or stage `references/` files.
- Keep per-run artifacts in stage `output/` folders.
- Stop at review gates and clearly name what the human should inspect before continuing.
- Use scripts for deterministic mechanical work when possible.
- If the same output correction appears repeatedly, update the relevant source file instead of patching only the current output.

## Editing Source Before Output

Output edits are allowed and expected. Source edits are better when an issue should be fixed for future runs. Prefer updating these files when a repeated pattern appears:

- Stage behavior: `stages/NN_slug/CONTEXT.md`
- Stable project rules: `_config/*.md`
- Stage-specific examples or rubrics: `stages/NN_slug/references/*.md`
- Cross-stage vocabulary or decisions: `shared/*.md`