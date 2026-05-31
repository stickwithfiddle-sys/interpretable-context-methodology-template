# Demo Walkthrough

This walkthrough gives a beginner two fast wins:

1. Install the CLI and create a clean workspace.
2. Inspect a completed example and see deterministic review checks pass.

For the fastest install-to-review path, start with [first-10-minutes.md](first-10-minutes.md). This page is the longer copy-paste demo.

## First Install

Use a virtual environment so the demo stays isolated:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install icm-workspace-template
icm --version
icm new my-first-icm-workspace --name "My First ICM Workspace" --with-common-artifacts
icm doctor my-first-icm-workspace
```

The first `doctor` run should explain that the intake brief needs content before downstream stages run. That is expected. ICM is checking that the workspace is usable and telling you what to fill in first.

The `--with-common-artifacts` flag adds starter files for `shared/source-inventory.md`, `shared/release-calendar.md`, and the shared decision log. They are optional, but they make the common artifact-shape validators easier to try.

## Completed Review Demo

The completed examples live in the GitHub repository. Clone the repo when you want to inspect a full run:

```bash
git clone https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template.git
cd interpretable-context-methodology-template
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
icm review stages/01_discovery --workspace examples/completed-documentation-refresh
```

Expected result:

```text
Summary: 0 fail, 0 warn, 35 pass
```

Look for these checks in the output:

```text
PASS Rubric required table columns present in discovery-report.md: Source, Used For
PASS Rubric link/path reference count met in discovery-report.md: 14/3
```

Then review the validation stage to see common artifact-shape checks:

```bash
icm review stages/05_validation --workspace examples/completed-documentation-refresh
```

Look for:

```text
PASS Rubric source-inventory artifact shape valid in source-inventory.md
PASS Rubric calendar artifact shape valid in release-calendar.md
PASS Rubric decision-log artifact shape valid in decision-log.md
```

For a project-planning version of the same pattern, run:

```bash
icm review stages/05_validation --workspace examples/completed-project-plan
```

Look for:

```text
PASS Rubric source-inventory artifact shape valid in source-inventory.md
PASS Rubric calendar artifact shape valid in project-calendar.md
PASS Rubric decision-log artifact shape valid in decision-log.md
```

Those lines come from:

```text
examples/completed-documentation-refresh/stages/01_discovery/references/discovery-report-rubric.md
examples/completed-documentation-refresh/stages/05_validation/references/source-inventory-rubric.md
examples/completed-documentation-refresh/stages/05_validation/references/release-calendar-rubric.md
examples/completed-documentation-refresh/stages/05_validation/references/decision-log-rubric.md
```

The rubric requires the discovery report to include a traceability table with `Source` and `Used For` columns, plus at least three link or path references.

## What To Read Next

- [First workspace tutorial](first-workspace.md)
- [First 10 minutes](first-10-minutes.md)
- [Review rubrics](review-rubrics.md)
- [Workflow rubric guide](workflow-rubrics.md)
- [JSON output](json-output.md)
- [Dashboard prototype](dashboard-prototype.md)
- [Source traceability](source-traceability.md)
- [Release-ready workspace](release-ready-workspace.md)
- [Documentation-refresh example](https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/tree/main/examples/completed-documentation-refresh)
- [Project-plan example](https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/tree/main/examples/completed-project-plan)
