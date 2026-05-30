#!/usr/bin/env python3
"""Create a new ICM workspace from the reusable template."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "templates" / "icm-workspace"
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".ps1", ".gitignore"}


def slugify(value: str) -> str:
    characters: list[str] = []
    previous_dash = False
    for character in value.lower():
        if character.isalnum():
            characters.append(character)
            previous_dash = False
        elif not previous_dash:
            characters.append("-")
            previous_dash = True
    return "".join(characters).strip("-") or "icm-project"


def ensure_empty_target(target: Path) -> None:
    if target.exists() and any(target.iterdir()):
        raise ValueError(f"Target directory is not empty: {target}")
    target.mkdir(parents=True, exist_ok=True)


def copy_template(target: Path) -> None:
    shutil.copytree(TEMPLATE_ROOT, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    target_tools = target / "tools"
    target_tools.mkdir(exist_ok=True)
    shutil.copy2(REPO_ROOT / "tools" / "validate_icm_workspace.py", target_tools / "validate_icm_workspace.py")


def replace_tokens(target: Path, replacements: dict[str, str]) -> None:
    for file_path in target.rglob("*"):
        if not file_path.is_file() or file_path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            original_text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated_text = original_text
        for token, replacement in replacements.items():
            updated_text = updated_text.replace(token, replacement)
        if updated_text != original_text:
            file_path.write_text(updated_text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new ICM workspace from this template.")
    parser.add_argument("target", help="Directory to create. It must be empty if it already exists.")
    parser.add_argument("--name", help="Human-readable project name. Defaults to the target directory name.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    project_name = args.name or target.name.replace("-", " ").replace("_", " ").title()
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROJECT_SLUG}}": slugify(project_name),
        "{{CREATED_DATE}}": dt.date.today().isoformat(),
    }

    if not TEMPLATE_ROOT.exists():
        print(f"Template folder not found: {TEMPLATE_ROOT}", file=sys.stderr)
        return 1

    try:
        ensure_empty_target(target)
        copy_template(target)
        replace_tokens(target, replacements)
    except ValueError as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 1

    print(f"Created ICM workspace: {target}")
    print(f"Project name: {project_name}")
    print("Next steps:")
    print("  1. Open the new folder in VS Code.")
    print("  2. Fill stages/00_intake/output/project-brief.md.")
    print("  3. Run python tools/validate_icm_workspace.py . --strict")
    return 0


if __name__ == "__main__":
    sys.exit(main())