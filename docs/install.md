# Install

ICM can be run directly from a source checkout or installed as a CLI.

## Install From PyPI

If you use `pipx`:

```bash
pipx install icm-workspace-template
icm --version
icm new my-first-icm-workspace --name "My First ICM Workspace"
```

If you prefer a local virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install icm-workspace-template
icm --version
icm new my-first-icm-workspace --name "My First ICM Workspace"
```

## Install A Pinned GitHub Release

Use this path when you want to test a specific repository tag before it reaches PyPI:

```bash
python -m pip install git+https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template.git@v0.14.0
icm --version
```

## Add ICM To An Existing Project

`icm init` copies only missing ICM starter files. It does not overwrite existing files.

```bash
cd my-existing-project
icm init . --name "My Existing Project"
icm doctor
```

If your project already has `AGENTS.md` or `CONTEXT.md`, `icm init` leaves them alone. `icm doctor` will tell you if those files need the ICM Stage Index or operating guidance merged in.

If the project will use source inventories, release calendars, or decision logs, add starter files for the common artifact-shape validators:

```bash
icm init . --with-common-artifacts
```

## From A Source Checkout

```bash
git clone https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template.git
cd interpretable-context-methodology-template
python -m icm --version
python -m icm new ../my-first-icm-workspace --name "My First ICM Workspace"
```

## PyPI Status

The package is live on PyPI as [`icm-workspace-template`](https://pypi.org/project/icm-workspace-template/).

For upgrade commands and a clean smoke test, see [pypi-upgrade.md](pypi-upgrade.md).

See [pypi-readiness.md](pypi-readiness.md) for the package checks and Trusted Publishing setup.

## Editable Development Install

Use a virtual environment so your system Python stays untouched:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
icm --version
icm status examples/completed-content-plan
```

## Why Installability Matters

`icm new` uses a template embedded in the Python package. That means it can create a workspace even when you are not running inside this repository.

`icm init` uses the same embedded template, but skips files that already exist.

The generated workspace still includes a fallback validator:

```bash
python tools/validate_icm_workspace.py . --strict
```

So a generated workspace remains useful even if the global `icm` command is not available later.
