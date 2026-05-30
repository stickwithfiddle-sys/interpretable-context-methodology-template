# Operating Rules

## ICM Principles

- One stage, one job.
- Plain text is the interface.
- Load context in layers and only for the current stage.
- Every output is an editable review surface.
- Improve reusable source files when repeated output edits reveal a pattern.

## Agent Boundaries

- Use judgment for synthesis, drafting, classification, and review.
- Use local scripts for deterministic validation, file checks, formatting, counting, and repeatable transformations.
- Do not invent missing project facts. Mark them as questions for the next review gate.
- Do not move to a downstream stage until the upstream output has been reviewed or explicitly accepted.

## Handoff Rule

The output of stage `NN` becomes the working input for stage `NN+1`. If a human edits an output file, downstream stages must treat the edited version as authoritative.