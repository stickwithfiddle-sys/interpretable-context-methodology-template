# Stage 04: Questionnaire

## Purpose

Create the setup questionnaire and reference-material prompts needed to configure the project-specific workspace once, then reuse it across runs.

## Inputs

| Layer | Path | Use |
| --- | --- | --- |
| Layer 3 | `../../_config/project-profile.md` | Known project identity and constraints |
| Layer 3 | `../../_config/style-guide.md` | Default output style |
| Layer 3 | `references/questionnaire-patterns.md` | Setup question patterns |
| Layer 4 | `../03_scaffold/output/scaffold-plan.md` | Approved scaffold plan |

## Process

1. Identify what stable knowledge each stage needs before normal runs begin.
2. Write setup questions that collect that knowledge from a human.
3. Map each answer to the `_config/`, `shared/`, or stage `references/` file it should populate.
4. Separate must-answer setup questions from optional refinements.

## Outputs

| File | Location | Purpose |
| --- | --- | --- |
| `setup-questionnaire.md` | `output/` | Setup questions and target reference files |

## Review Gate

Before continuing, a human should confirm the questionnaire collects enough stable context without becoming burdensome.

## Verify

- Confirm `output/setup-questionnaire.md` exists.
- Confirm each question maps to a target reference file.
- Confirm questions distinguish stable factory configuration from per-run working inputs.