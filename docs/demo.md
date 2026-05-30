# Demo Walkthrough

This walkthrough gives a beginner two fast wins:

1. Install the CLI and create a clean workspace.
2. Inspect a completed example and see deterministic review checks pass.

## First Install

Use a virtual environment so the demo stays isolated:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install icm-workspace-template
icm --version
icm new my-first-icm-workspace --name "My First ICM Workspace"
icm doctor my-first-icm-workspace
```

The first `doctor` run should explain that the intake brief needs content before downstream stages run. That is expected. ICM is checking that the workspace is usable and telling you what to fill in first.

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

Those lines come from:

```text
examples/completed-documentation-refresh/stages/01_discovery/references/discovery-report-rubric.md
```

The rubric requires the discovery report to include a traceability table with `Source` and `Used For` columns, plus at least three link or path references.

## What To Read Next

- [First workspace tutorial](first-workspace.md)
- [Review rubrics](review-rubrics.md)
- [Source traceability](source-traceability.md)
- [Documentation-refresh example](https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/tree/main/examples/completed-documentation-refresh)
