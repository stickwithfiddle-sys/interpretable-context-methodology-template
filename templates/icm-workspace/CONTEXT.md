# {{PROJECT_NAME}} Workspace Context

This file is Layer 1 routing for the workspace. Use it to decide which stage to run and which shared resources are available.

## Workspace Purpose

Use this workspace to design a project-specific ICM workflow for {{PROJECT_NAME}}. The final output should be a validated stage map, setup questionnaire, and scaffold plan that can be turned into a project workspace.

## Stage Index

| Stage | Use When | Primary Output |
| --- | --- | --- |
| `stages/00_intake` | The project idea or constraints are still rough | `output/project-brief.md` |
| `stages/01_discovery` | You need domain, audience, deliverable, risk, and workflow analysis | `output/discovery-report.md` |
| `stages/02_stage_mapping` | You need numbered stages, handoffs, and review gates | `output/stage-map.md` |
| `stages/03_scaffold` | You need the proposed project folder tree and stage contracts | `output/scaffold-plan.md` |
| `stages/04_questionnaire` | You need setup questions for stable project reference material | `output/setup-questionnaire.md` |
| `stages/05_validation` | You need to check the proposed workflow before using it | `output/validation-report.md` |

## Shared Resources

- `_config/project-profile.md`: stable project identity and constraints.
- `_config/operating-rules.md`: ICM principles for this workspace.
- `_config/quality-gates.md`: quality standards for stage outputs.
- `_templates/stage-context.md`: reusable stage contract template.
- `shared/decision-log.md`: cross-stage decisions that should persist.
- `shared/backlog.md`: deferred improvements and unresolved questions.

## Stage Execution Protocol

1. Open the stage `CONTEXT.md`.
2. Load only the files listed under Inputs.
3. Follow the Process section.
4. Write exactly the named Outputs.
5. Run the Verify checks.
6. Stop at the Review Gate before moving to the next stage.

## Local Checks

Run the validator from the workspace root:

```powershell
python tools/validate_icm_workspace.py . --strict
```