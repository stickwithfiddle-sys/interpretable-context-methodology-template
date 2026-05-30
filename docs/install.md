# Install

ICM can be run directly from a source checkout or installed as a CLI.

## From A Source Checkout

```bash
git clone https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template.git
cd interpretable-context-methodology-template
python -m icm --version
python -m icm new ../my-first-icm-workspace --name "My First ICM Workspace"
```

## Editable Development Install

Use a virtual environment so your system Python stays untouched:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
icm --version
icm status examples/completed-content-plan
```

## Install From GitHub

If you use `pipx`:

```bash
pipx install git+https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template.git
icm --version
icm new my-first-icm-workspace --name "My First ICM Workspace"
```

If you prefer a local virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install git+https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template.git
icm --version
icm new my-first-icm-workspace --name "My First ICM Workspace"
```

## Why Installability Matters

`icm new` uses a template embedded in the Python package. That means it can create a workspace even when you are not running inside this repository.

The generated workspace still includes a fallback validator:

```bash
python tools/validate_icm_workspace.py . --strict
```

So a generated workspace remains useful even if the global `icm` command is not available later.
