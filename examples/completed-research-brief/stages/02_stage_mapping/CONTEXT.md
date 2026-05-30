# Stage 02: Stage Mapping

## Purpose

Turn the discovery report into a numbered workflow with clear stage responsibilities, handoffs, review gates, and validation checks.

## Inputs

| Layer | Path | Use |
| --- | --- | --- |
| Layer 3 | `../../_config/operating-rules.md` | ICM design rules |
| Layer 3 | `../../_config/quality-gates.md` | Review standards |
| Layer 3 | `references/stage-patterns.md` | Common stage shapes |
| Layer 4 | `../01_discovery/output/discovery-report.md` | Approved discovery analysis |

## Process

1. Propose the smallest useful sequence of stages.
2. Give each stage one job and one primary output.
3. Define the Layer 4 handoff from each stage to the next.
4. Mark review gates where human correction is cheapest.
5. Identify deterministic checks for each stage.

## Outputs

| File | Location | Purpose |
| --- | --- | --- |
| `stage-map.md` | `output/` | Numbered stage plan for scaffolding |

## Review Gate

Before continuing, a human should confirm the stage sequence reflects the real workflow and that no stage combines unrelated jobs.

## Verify

- Confirm `output/stage-map.md` exists.
- Confirm every stage has a purpose, inputs, outputs, review gate, and verify check.
- Confirm stage names use numbered order and clear slugs.