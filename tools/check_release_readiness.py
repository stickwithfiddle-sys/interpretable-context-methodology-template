"""Check package and release metadata before tagging a release."""

from __future__ import annotations

import re
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.10 only.
    import tomli as tomllib


REPO_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPO_ROOT / "pyproject.toml"
INIT = REPO_ROOT / "icm" / "__init__.py"
README = REPO_ROOT / "README.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
INSTALL_DOC = REPO_ROOT / "docs" / "install.md"
DOCS_INDEX = REPO_ROOT / "docs" / "index.html"
PUBLISH_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "publish.yml"


def package_version() -> str:
    match = re.search(r'__version__\s*=\s*"([^"]+)"', INIT.read_text(encoding="utf-8"))
    if not match:
        raise ValueError("Could not find icm.__version__")
    return match.group(1)


def main() -> int:
    problems: list[str] = []
    pyproject = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    project = pyproject.get("project", {})
    version = str(project.get("version", ""))
    module_version = package_version()

    if version != module_version:
        problems.append(f"pyproject version {version!r} does not match icm.__version__ {module_version!r}")

    if project.get("name") != "icm-workspace-template":
        problems.append("project.name should remain icm-workspace-template unless the PyPI name intentionally changes")

    if project.get("readme") != "README.md":
        problems.append("project.readme should point to README.md for PyPI rendering")

    if project.get("license") != "MIT":
        problems.append("project.license should use the MIT SPDX expression")

    if sorted(project.get("license-files", [])) != ["LICENSE", "NOTICE"]:
        problems.append("project.license-files should include LICENSE and NOTICE")

    if project.get("requires-python") != ">=3.10":
        problems.append("requires-python should stay explicit before publishing")

    scripts = project.get("scripts", {})
    if scripts.get("icm") != "icm.cli:main":
        problems.append("project.scripts.icm should point to icm.cli:main")

    urls = project.get("urls", {})
    for key in ("Homepage", "Repository", "Issues", "Changelog", "Documentation"):
        if key not in urls:
            problems.append(f"Missing project URL metadata: {key}")

    package_data = pyproject.get("tool", {}).get("setuptools", {}).get("package-data", {}).get("icm", [])
    for required_pattern in ("templates/icm-workspace/**/*", "legacy_tools/*.py"):
        if required_pattern not in package_data:
            problems.append(f"Missing package-data pattern: {required_pattern}")

    readme_text = README.read_text(encoding="utf-8")
    if f"Current package version: `{version}`" not in readme_text:
        problems.append("README current package version does not match pyproject")

    changelog_text = CHANGELOG.read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog_text:
        problems.append(f"CHANGELOG is missing a section for {version}")

    install_text = INSTALL_DOC.read_text(encoding="utf-8")
    docs_index_text = DOCS_INDEX.read_text(encoding="utf-8")
    expected_tag = f"@v{version}"
    if expected_tag not in install_text:
        problems.append(f"docs/install.md does not reference {expected_tag}")
    if expected_tag not in docs_index_text:
        problems.append(f"docs/index.html does not reference {expected_tag}")

    if not PUBLISH_WORKFLOW.exists():
        problems.append("Missing PyPI publishing workflow: .github/workflows/publish.yml")

    if problems:
        for problem in problems:
            print(f"ERROR {problem}")
        return 1

    print(f"OK: release metadata is ready for {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
