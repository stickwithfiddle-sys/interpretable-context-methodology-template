# Release-Ready Workspace

Use this checklist when an ICM workspace is about to become something other people rely on: a published package, public repo, client deliverable, internal process, or recurring content workflow.

## 1. Confirm The Installed CLI

```bash
icm --version
python -m pip show icm-workspace-template
```

If the version is stale, upgrade and smoke test:

```bash
python -m pip install --upgrade icm-workspace-template
rm -rf /tmp/icm-upgrade-smoke
icm new /tmp/icm-upgrade-smoke --name "Upgrade Smoke" --with-common-artifacts
icm validate /tmp/icm-upgrade-smoke --strict
```

See [pypi-upgrade.md](pypi-upgrade.md) for pipx and virtual environment variants.

For choosing review checks by workflow type, see [workflow-rubrics.md](workflow-rubrics.md).

## 2. Validate Structure

Run this from the workspace root:

```bash
icm validate . --strict
```

Expected result:

```text
OK: workspace passed validation with 0 warning(s)
```

If the generated workspace must stand alone without the global CLI, also run:

```bash
python tools/validate_icm_workspace.py . --strict
```

## 3. Run Doctor

```bash
icm doctor . --strict
```

Doctor checks structure, empty stage sections, undeclared outputs, missing inputs, broken handoffs, intake readiness, and rubric failures for existing declared outputs.

When source inventory, calendar, or decision-log shape checks fail, starter files can be added with:

```bash
icm init . --with-common-artifacts
```

## 4. Review The Important Stages

Run review checks on the stages that produce release-critical artifacts:

```bash
icm review stages/01_discovery
icm review stages/05_validation
```

For file-specific review:

```bash
icm review stages/05_validation/output/source-inventory.md
icm review stages/05_validation/output/release-calendar.md
icm review stages/05_validation/output/decision-log.md
```

Useful PASS lines include:

```text
PASS Rubric required source cited
PASS Rubric required table columns present
PASS Rubric link/path reference count met
PASS Rubric source-inventory artifact shape valid
PASS Rubric calendar artifact shape valid
PASS Rubric decision-log artifact shape valid
```

## 5. Update Release Notes

Before merging or tagging, update:

- `CHANGELOG.md` for user-facing behavior.
- `README.md` or docs when commands or workflows changed.
- The workspace `shared/decision-log.md` when a durable decision affects future stages.
- Any rubric in `stages/*/references/` when the accepted artifact shape changed.

## 6. Package Or Publish

For this repository, use the full release process:

```bash
python -m pytest
python tools/check_packaged_assets.py
python tools/check_docs_site.py
python tools/check_release_readiness.py
rm -rf dist build *.egg-info
python -m build
python -m twine check dist/*
```

Then follow [release-process.md](release-process.md) and [pypi-readiness.md](pypi-readiness.md).

## Release Gate

Do not ship until:

- Structure validation passes.
- Doctor has no strict failures.
- Critical stage reviews pass.
- Changelog and docs match the behavior.
- The installed package path has been smoke tested.
