# PyPI Publishing

This project is published on PyPI as [`icm-workspace-template`](https://pypi.org/project/icm-workspace-template/).

The recommended path is PyPI Trusted Publishing, which uses GitHub Actions OpenID Connect instead of a long-lived PyPI API token. See the official PyPI docs for [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) and [publishing with a Trusted Publisher](https://docs.pypi.org/trusted-publishers/using-a-publisher/).

## Package Identity

Current package metadata:

- Distribution name: `icm-workspace-template`
- CLI command: `icm`
- Python: `>=3.10`
- License: MIT
- Maintainer credit: Hobo
- Original method credit: see `NOTICE`

Before any future publish, confirm the README renders cleanly and the release version has not already been uploaded.

## Local Package Checks

Run these before publishing:

```bash
python -m pytest
python tools/check_packaged_assets.py
python tools/check_docs_site.py
python tools/check_release_readiness.py
rm -rf dist build *.egg-info
python -m build
python -m twine check dist/*
```

Then install the wheel into a clean environment:

```bash
python -m venv .tmp/install-venv
.tmp/install-venv/bin/python -m pip install dist/*.whl
.tmp/install-venv/bin/icm --version
```

## Trusted Publishing Setup

The Trusted Publisher should match:

- Owner: `stickwithfiddle-sys`
- Repository: `interpretable-context-methodology-template`
- Workflow: `publish.yml`
- Environment: `pypi`

For TestPyPI, use the same repository and workflow with the `testpypi` environment.

## Publish Flow

1. Create and push a release tag, for example `v0.16.0`.
2. In GitHub Actions, run `Publish Python Package`.
3. Select the release tag as the workflow ref.
4. Choose `testpypi` first.
5. Install from TestPyPI in a clean environment and smoke test `icm new`.
6. Run the same workflow again for `pypi`.
7. Install from PyPI in a clean environment and smoke test `icm new`.

Do not publish from an untagged branch. The workflow intentionally fails unless it is run from a tag.
