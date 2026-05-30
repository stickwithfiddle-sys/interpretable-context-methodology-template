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

## Pre-Merge Checklist

Run:

```bash
python -m icm validate templates/icm-workspace --strict
python -m icm validate examples/completed-content-plan --strict
python -m icm status examples/completed-content-plan
python -m icm next examples/completed-content-plan
python -m icm explain stages/01_discovery --workspace examples/completed-content-plan
python -m icm doctor examples/completed-content-plan --strict
python tools/validate_icm_workspace.py templates/icm-workspace --strict
```

Check:

- The PR checklist is complete.
- `CHANGELOG.md` names the user-facing changes.
- Any new command has help text.
- Any new workflow behavior appears in a doc or example.
- The completed example still validates.

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

## Recommended GitHub Settings

Use these settings once the project has collaborators:

- Protect `main`.
- Require pull requests before merging.
- Require the CI workflow to pass.
- Use squash merges for tidy history, unless preserving commits helps review.
- Delete branches after merge.
- Keep issues and discussions enabled for feedback.
