# Stage 05: Validation

## Purpose

Validate the proposed project-specific ICM workspace before it is used for real work.

## Inputs

| Layer | Path | Use |
| --- | --- | --- |
| Layer 3 | `../../_config/quality-gates.md` | Validation standards |
| Layer 3 | `references/validation-checklist.md` | Dry-run checklist |
| Layer 4 | `../02_stage_mapping/output/stage-map.md` | Approved stage map |
| Layer 4 | `../03_scaffold/output/scaffold-plan.md` | Approved scaffold plan |
| Layer 4 | `../04_questionnaire/output/setup-questionnaire.md` | Approved setup questionnaire |

## Process

1. Check whether the scaffold plan satisfies the stage map.
2. Check whether the questionnaire collects the Layer 3 material each stage requires.
3. Identify missing contracts, vague handoffs, overloaded stages, and absent validation checks.
4. Produce a clear go/no-go recommendation.
5. If files have been generated, run `python tools/validate_icm_workspace.py . --strict` from that workspace root.

## Outputs

| File | Location | Purpose |
| --- | --- | --- |
| `validation-report.md` | `output/` | Readiness report and fix list |

## Review Gate

Before using the generated project workspace, a human should resolve blocker findings or explicitly accept the residual risk.

## Verify

- Confirm `output/validation-report.md` exists.
- Confirm each finding names the source file or stage it affects.
- Confirm the report includes a go/no-go recommendation.