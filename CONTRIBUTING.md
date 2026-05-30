# Contributing

Thanks for helping improve the ICM reusable template.

The project should stay beginner-friendly, inspectable, and file-first. If a change makes the workflow more powerful but harder to understand, document the tradeoff clearly.

## Branch Workflow

1. Start from an up-to-date `main`.
2. Create a short feature branch:

```bash
git checkout main
git pull
git checkout -b feature/short-description
```

3. Make the change.
4. Run the local checks.
5. Update docs, examples, and `CHANGELOG.md` when behavior changes.
6. Open a pull request using the checklist.
7. Merge only after checks pass and the PR has been reviewed.

Use branch names like:

- `feature/icm-status`
- `fix/validator-missing-output`
- `docs/first-run-guide`
- `release/v0.3.1`

## Local Checks

Set up the editable CLI in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run these before opening or merging a pull request:

```bash
python -m pytest
python tools/check_packaged_assets.py
python tools/check_docs_site.py
python tools/check_release_readiness.py
python -m icm validate templates/icm-workspace --strict
python -m icm validate examples/completed-content-plan --strict
python -m icm validate examples/completed-research-brief --strict
python -m icm validate examples/completed-documentation-refresh --strict
python -m icm init /tmp/icm-existing-smoke --name "Existing Smoke" --with-common-artifacts
python -m icm status examples/completed-content-plan
python -m icm next examples/completed-content-plan
python -m icm explain stages/01_discovery --workspace examples/completed-content-plan
python -m icm review stages/01_discovery --workspace examples/completed-content-plan
python -m icm review stages/01_discovery --workspace examples/completed-research-brief
python -m icm review stages/01_discovery --workspace examples/completed-documentation-refresh
python -m icm review stages/05_validation --workspace examples/completed-documentation-refresh
python -m icm doctor examples/completed-content-plan --strict
python -m icm doctor examples/completed-research-brief --strict
python -m icm doctor examples/completed-documentation-refresh --strict
```

Also run the legacy validators so generated workspaces remain self-contained:

```bash
python tools/validate_icm_workspace.py templates/icm-workspace --strict
python examples/completed-content-plan/tools/validate_icm_workspace.py examples/completed-content-plan --strict
python examples/completed-research-brief/tools/validate_icm_workspace.py examples/completed-research-brief --strict
python examples/completed-documentation-refresh/tools/validate_icm_workspace.py examples/completed-documentation-refresh --strict
```

When packaging changes, also run:

```bash
rm -rf dist build *.egg-info
python -m build
python -m twine check dist/*
```

## Change Checklist

- The README still tells a beginner what to do first.
- New behavior has a CLI command, doc note, or example.
- New files are plain text unless there is a strong reason otherwise.
- Stage contracts still use Inputs, Process, Outputs, Review Gate, and Verify.
- Repeated advice belongs in `_config/`, `shared/`, or `references/`, not only in prose.
- `CHANGELOG.md` has an entry under `Unreleased` or the release version.
- Version numbers are updated when preparing a release.
- Package-embedded assets match `templates/icm-workspace`.
- Release metadata passes `python tools/check_release_readiness.py`.
- Tests pass locally with `python -m pytest`.
- The docs homepage passes `python tools/check_docs_site.py` when visual docs change.
- Release-impacting changes are checked against `docs/release-ready-workspace.md`.

When changing `templates/icm-workspace`, mirror it into `icm/templates/icm-workspace` and run:

```bash
python tools/check_packaged_assets.py
```

## Versioning

The version appears in:

- `icm/__init__.py`
- `pyproject.toml`
- `CHANGELOG.md`

For releases, tag the merge commit:

```bash
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin vX.Y.Z
```

See [docs/release-process.md](docs/release-process.md) for the full release checklist.
