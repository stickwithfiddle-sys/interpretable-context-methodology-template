# Stage NN: Stage Name

## Purpose

State the one job this stage performs.

## Inputs

| Layer | Path | Use |
| --- | --- | --- |
| Layer 3 | `../../_config/operating-rules.md` | Stable workspace rules |
| Layer 3 | `references/example.md` | Stage-specific guidance |
| Layer 4 | `../PREVIOUS_STAGE/output/example.md` | Working input from the previous stage |

## Process

1. Read the declared inputs.
2. Transform the Layer 4 artifact according to the Layer 3 references.
3. Keep open questions visible.

## Outputs

| File | Location | Purpose |
| --- | --- | --- |
| `example-output.md` | `output/` | Handoff artifact for the next stage |

## Review Gate

Before continuing, a human should check:

- The output matches the stage purpose.
- The next stage can consume it without guessing.
- Any assumptions or unresolved questions are visible.

## Verify

- Confirm every declared output exists.
- Confirm the output does not contradict upstream decisions.
- Run local scripts if the stage contract names any.