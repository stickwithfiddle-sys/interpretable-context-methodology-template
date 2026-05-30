# Content Plan Example

This is a completed example ICM workspace. It shows what the stage outputs look like after a small builder workflow has been run and reviewed.

Read the outputs in order:

1. `stages/00_intake/output/project-brief.md`
2. `stages/01_discovery/output/discovery-report.md`
3. `stages/02_stage_mapping/output/stage-map.md`
4. `stages/03_scaffold/output/scaffold-plan.md`
5. `stages/04_questionnaire/output/setup-questionnaire.md`
6. `stages/05_validation/output/validation-report.md`

## What This Example Builds

The example designs a project-specific ICM workspace for producing a weekly content plan from rough notes, source links, and product priorities.

The important thing to notice is the shape of the handoffs:

- Intake turns a rough idea into an approved brief.
- Discovery finds the workflow shape, risks, and reusable context.
- Stage mapping turns discovery into numbered stages.
- Scaffold turns the stage map into a proposed workspace tree.
- Questionnaire identifies stable setup questions.
- Validation checks whether the proposed workspace is ready to use.

## Validate

From this example folder:

```bash
icm validate --strict
```

Expected output:

```text
OK: workspace passed validation with 0 warning(s)
```

If `icm` is not installed, use:

```bash
python tools/validate_icm_workspace.py . --strict
```

## Review An Output

```bash
icm review stages/01_discovery
```

The discovery report includes a `Source Traceability` section. Its rubric requires citations for the intake brief, discovery question bank, and quality gates.
