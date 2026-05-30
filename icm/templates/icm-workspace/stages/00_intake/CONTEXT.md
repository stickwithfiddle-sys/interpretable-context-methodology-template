# Stage 00: Intake

## Purpose

Convert a rough project idea into a concise project brief that downstream stages can use without guessing.

## Inputs

| Layer | Path | Use |
| --- | --- | --- |
| Layer 3 | `../../_config/project-profile.md` | Stable project identity and constraints |
| Layer 3 | `../../_templates/run-brief.md` | Brief structure |
| Layer 3 | `references/intake-checklist.md` | Completeness checklist |
| Layer 4 | `output/project-brief.md` | Existing draft brief, if any |

## Process

1. Read the existing draft brief if present.
2. Fill gaps using the checklist and project profile.
3. Separate facts from assumptions and open questions.
4. Keep the brief short enough for the next stage to use directly.

## Outputs

| File | Location | Purpose |
| --- | --- | --- |
| `project-brief.md` | `output/` | Authoritative project brief for discovery |

## Review Gate

Before continuing, a human should confirm the goal, constraints, audience, and open questions are accurate.

## Verify

- Confirm `output/project-brief.md` exists.
- Confirm the brief names at least one desired outcome, one user or reviewer, and one success criterion.
- Confirm unknowns are listed under Open Questions rather than hidden as assumptions.