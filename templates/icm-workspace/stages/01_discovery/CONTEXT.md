# Stage 01: Discovery

## Purpose

Analyze the project brief to identify the project domain, users, deliverables, risks, and repeatable workflow shape.

## Inputs

| Layer | Path | Use |
| --- | --- | --- |
| Layer 3 | `../../_config/operating-rules.md` | ICM operating principles |
| Layer 3 | `../../_config/quality-gates.md` | Output quality standards |
| Layer 3 | `references/discovery-question-bank.md` | Discovery prompts |
| Layer 4 | `../00_intake/output/project-brief.md` | Approved project brief |

## Process

1. Extract known facts, assumptions, constraints, and unresolved questions.
2. Identify repeated work that should become stages.
3. Identify stable reference material the project will need.
4. Identify working artifacts that will change each run.
5. Name risks that require review gates or deterministic checks.

## Outputs

| File | Location | Purpose |
| --- | --- | --- |
| `discovery-report.md` | `output/` | Domain and workflow analysis for stage mapping |

## Review Gate

Before continuing, a human should confirm the discovered workflow matches the real project and that no critical stakeholder or constraint is missing.

## Verify

- Confirm `output/discovery-report.md` exists.
- Confirm the report separates facts, assumptions, open questions, and risks.
- Confirm it identifies candidate Layer 3 reference material and Layer 4 working artifacts.