#!/usr/bin/env python3
"""Validate an Interpretable Context Methodology workspace."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


STAGE_NAME_PATTERN = re.compile(r"^\d{2}_[a-z0-9][a-z0-9_-]*$")
REQUIRED_STAGE_HEADINGS = ("Inputs", "Process", "Outputs", "Review Gate", "Verify")
REQUIRED_ROOT_DIRECTORIES = ("_config", "_templates", "shared", "stages")


def has_heading(markdown: str, heading: str) -> bool:
    pattern = re.compile(rf"^#+\s+{re.escape(heading)}\s*$", re.IGNORECASE | re.MULTILINE)
    return bool(pattern.search(markdown))


def collect_stage_directories(workspace_root: Path) -> list[Path]:
    stages_root = workspace_root / "stages"
    if not stages_root.exists():
        return []
    return sorted(path for path in stages_root.iterdir() if path.is_dir())


def validate_workspace(workspace_root: Path, strict: bool = False) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not workspace_root.exists():
        errors.append(f"Workspace does not exist: {workspace_root}")
    elif not workspace_root.is_dir():
        errors.append(f"Workspace is not a directory: {workspace_root}")

    if errors:
        return report(errors, warnings, strict)

    if not ((workspace_root / "AGENTS.md").exists() or (workspace_root / "CLAUDE.md").exists()):
        errors.append("Missing Layer 0 identity file: add AGENTS.md or CLAUDE.md")

    if not (workspace_root / "CONTEXT.md").exists():
        errors.append("Missing Layer 1 routing file: CONTEXT.md")

    for directory_name in REQUIRED_ROOT_DIRECTORIES:
        if not (workspace_root / directory_name).is_dir():
            errors.append(f"Missing required directory: {directory_name}/")

    stage_directories = collect_stage_directories(workspace_root)
    if not stage_directories:
        errors.append("No stage directories found under stages/")

    seen_stage_numbers: set[str] = set()
    for stage_directory in stage_directories:
        stage_name = stage_directory.name
        if not STAGE_NAME_PATTERN.match(stage_name):
            warnings.append(f"Stage name should match NN_slug: stages/{stage_name}/")

        stage_number = stage_name.split("_", 1)[0]
        if stage_number in seen_stage_numbers:
            errors.append(f"Duplicate stage number: {stage_number}")
        seen_stage_numbers.add(stage_number)

        context_path = stage_directory / "CONTEXT.md"
        if not context_path.exists():
            errors.append(f"Missing stage contract: stages/{stage_name}/CONTEXT.md")
        else:
            context_markdown = context_path.read_text(encoding="utf-8")
            for heading in REQUIRED_STAGE_HEADINGS:
                if not has_heading(context_markdown, heading):
                    errors.append(f"stages/{stage_name}/CONTEXT.md missing heading: {heading}")
            if "Layer 3" not in context_markdown or "Layer 4" not in context_markdown:
                warnings.append(f"stages/{stage_name}/CONTEXT.md should explicitly separate Layer 3 and Layer 4 inputs")

        if not (stage_directory / "references").is_dir():
            errors.append(f"Missing Layer 3 folder: stages/{stage_name}/references/")
        if not (stage_directory / "output").is_dir():
            errors.append(f"Missing Layer 4 handoff folder: stages/{stage_name}/output/")

    return report(errors, warnings, strict)


def report(errors: list[str], warnings: list[str], strict: bool) -> int:
    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"ERROR {error}")

    if errors or (strict and warnings):
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"OK: workspace passed validation with {len(warnings)} warning(s)")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an ICM workspace folder.")
    parser.add_argument("workspace", nargs="?", default=".", help="Path to the ICM workspace to validate")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace_root = Path(args.workspace).resolve()
    return validate_workspace(workspace_root, strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())