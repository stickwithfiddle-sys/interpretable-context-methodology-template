# PyPI Upgrade And Verification

Use this when you already have ICM installed and want to confirm you are using the latest published package.

## Virtual Environment

From the environment where you run `icm`:

```bash
python -m pip install --upgrade icm-workspace-template
icm --version
python -m pip show icm-workspace-template
```

Then smoke test the installed package outside this repository:

```bash
rm -rf /tmp/icm-upgrade-smoke
icm new /tmp/icm-upgrade-smoke --name "Upgrade Smoke"
icm validate /tmp/icm-upgrade-smoke --strict
python /tmp/icm-upgrade-smoke/tools/validate_icm_workspace.py /tmp/icm-upgrade-smoke --strict
```

Expected validation output:

```text
OK: workspace passed validation with 0 warning(s)
```

## pipx

If you installed with `pipx`:

```bash
pipx upgrade icm-workspace-template
icm --version
pipx runpip icm-workspace-template show icm-workspace-template
```

Then run the same smoke test:

```bash
rm -rf /tmp/icm-upgrade-smoke
icm new /tmp/icm-upgrade-smoke --name "Upgrade Smoke"
icm validate /tmp/icm-upgrade-smoke --strict
```

## Version Check

The current package version is listed in the root README. Release notes live in the repository [CHANGELOG.md](https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/blob/main/CHANGELOG.md), and the published package page is [pypi.org/project/icm-workspace-template](https://pypi.org/project/icm-workspace-template/).

If `icm --version` does not match the package page, run the upgrade command again inside the same environment where your shell finds `icm`.

## Common Fixes

| Symptom | Fix |
| --- | --- |
| `icm --version` still shows an old version | Run `python -m pip install --upgrade icm-workspace-template` in the active virtual environment |
| `which icm` points outside your project | Activate the intended virtual environment first |
| `pipx upgrade` says the app is not installed | Use `pipx install icm-workspace-template`, or use the virtual environment path |
| New workspace validation fails | Re-run `icm new` in an empty folder and confirm the package version first |
