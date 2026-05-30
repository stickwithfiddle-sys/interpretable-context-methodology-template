# Release Process

Use this checklist when turning repo changes into a visible version.

## Version Rules

The project uses Semantic Versioning while pre-1.0:

- `0.MINOR.0` for meaningful feature additions or workflow changes.
- `0.MINOR.PATCH` for fixes, small docs improvements, and compatibility updates.
- Call out breaking changes in the changelog even before `1.0.0`.

## Required Files To Update

- `icm/__init__.py`
- `pyproject.toml`
- `CHANGELOG.md`
- README or docs when user-facing behavior changes
- Tests or examples when behavior needs coverage

## Pre-Merge Checklist

Run:

```bash
python -m pytest
python tools/check_packaged_assets.py
python tools/check_docs_site.py
python tools/check_release_readiness.py
python -m icm validate templates/icm-workspace --strict
python -m icm validate examples/completed-content-plan --strict
python -m icm validate examples/completed-research-brief --strict
rm -rf /tmp/icm-existing-smoke
mkdir -p /tmp/icm-existing-smoke
printf '# Existing\n' > /tmp/icm-existing-smoke/README.md
python -m icm init /tmp/icm-existing-smoke --name "Existing Smoke"
python -m icm validate /tmp/icm-existing-smoke --strict
python -m icm status examples/completed-content-plan
python -m icm next examples/completed-content-plan
python -m icm explain stages/01_discovery --workspace examples/completed-content-plan
python -m icm review stages/01_discovery --workspace examples/completed-content-plan
python -m icm review stages/01_discovery --workspace examples/completed-research-brief
python -m icm doctor examples/completed-content-plan --strict
python -m icm doctor examples/completed-research-brief --strict
python tools/validate_icm_workspace.py templates/icm-workspace --strict
python examples/completed-content-plan/tools/validate_icm_workspace.py examples/completed-content-plan --strict
python examples/completed-research-brief/tools/validate_icm_workspace.py examples/completed-research-brief --strict
rm -rf dist build *.egg-info
python -m build
python -m twine check dist/*
```

Check:

- The PR checklist is complete.
- `CHANGELOG.md` names the user-facing changes.
- Any new command has help text.
- Any new workflow behavior appears in a doc or example.
- The completed example still validates.
- Pytest covers the expected CLI and workspace behavior.
- The docs homepage still references existing local assets.
- The source distribution and wheel build cleanly.
- `twine check dist/*` passes before publishing.
- The wheel installs and `icm new` works outside the source checkout.

## Installed Package Smoke Test

```bash
rm -rf .tmp/wheelhouse .tmp/install-venv
python -m build --outdir .tmp/wheelhouse
python -m venv .tmp/install-venv
.tmp/install-venv/bin/python -m pip install .tmp/wheelhouse/*.whl
rm -rf /tmp/icm-install-smoke
cd /tmp
/path/to/repo/.tmp/install-venv/bin/icm new /tmp/icm-install-smoke --name "Install Smoke"
/path/to/repo/.tmp/install-venv/bin/icm init /tmp/icm-install-smoke --name "Install Smoke"
/path/to/repo/.tmp/install-venv/bin/icm validate /tmp/icm-install-smoke --strict
python /tmp/icm-install-smoke/tools/validate_icm_workspace.py /tmp/icm-install-smoke --strict
```

## Release Checklist

1. Move changelog notes from `Unreleased` into the release version.
2. Confirm version numbers match.
3. Commit the release changes.
4. Tag the release:

```bash
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin main
git push origin vX.Y.Z
```

5. Create a GitHub release from the tag.
6. Paste the changelog section into the release notes.
7. After release, add a fresh `Unreleased` section if needed.

## PyPI Publishing Checklist

Use this only after a tagged GitHub release exists and the PyPI Trusted Publisher is configured.

1. Confirm the PyPI or TestPyPI publisher matches:

```text
Owner: stickwithfiddle-sys
Repository: interpretable-context-methodology-template
Workflow: publish.yml
Environment: testpypi or pypi
```

2. In GitHub Actions, run `Publish Python Package` from the release tag.
3. Choose `testpypi` first.
4. Install from TestPyPI into a clean environment and run `icm new`.
5. Run `Publish Python Package` again from the same tag and choose `pypi`.
6. After PyPI is live, update README and docs/install.md to lead with `pip install icm-workspace-template`.

## Recommended GitHub Settings

Use these settings once the project has collaborators:

- Protect `main`.
- Require pull requests before merging.
- Require the CI workflow to pass.
- Require code owner review for pull requests when collaborators are added.
- Use squash merges for tidy history, unless preserving commits helps review.
- Delete branches after merge.
- Keep issues and discussions enabled for feedback.
- Use GitHub Pages from the `main` branch `/docs` folder for the visual docs site.
