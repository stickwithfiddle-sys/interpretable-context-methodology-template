#!/usr/bin/env python3
"""Check that package-embedded assets match the source template assets."""

from __future__ import annotations

import filecmp
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_TEMPLATE = REPO_ROOT / "templates" / "icm-workspace"
PACKAGED_TEMPLATE = REPO_ROOT / "icm" / "templates" / "icm-workspace"
SOURCE_VALIDATOR = REPO_ROOT / "tools" / "validate_icm_workspace.py"
PACKAGED_VALIDATOR = REPO_ROOT / "icm" / "legacy_tools" / "validate_icm_workspace.py"


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def files_match(left: Path, right: Path) -> bool:
    return normalized_bytes(left) == normalized_bytes(right)


def compare_directories(left: Path, right: Path, label: str) -> list[str]:
    problems: list[str] = []
    if not left.exists():
        return [f"Missing source {label}: {left}"]
    if not right.exists():
        return [f"Missing packaged {label}: {right}"]

    comparison = filecmp.dircmp(left, right)
    problems.extend(f"Only in source {label}: {left / name}" for name in comparison.left_only)
    problems.extend(f"Only in packaged {label}: {right / name}" for name in comparison.right_only)
    problems.extend(f"Unclear {label} file: {left / name}" for name in comparison.funny_files)
    for name in comparison.diff_files:
        if not files_match(left / name, right / name):
            problems.append(f"Different {label} file: {left / name}")

    for common_dir in comparison.common_dirs:
        problems.extend(compare_directories(left / common_dir, right / common_dir, label))
    return problems


def main() -> int:
    problems = compare_directories(SOURCE_TEMPLATE, PACKAGED_TEMPLATE, "template")
    if not PACKAGED_VALIDATOR.exists():
        problems.append(f"Missing packaged validator: {PACKAGED_VALIDATOR}")
    elif not files_match(SOURCE_VALIDATOR, PACKAGED_VALIDATOR):
        problems.append(f"Packaged validator differs from source: {PACKAGED_VALIDATOR}")

    if problems:
        for problem in problems:
            print(f"ERROR {problem}")
        print(f"FAILED: {len(problems)} packaged asset issue(s)")
        return 1

    print("OK: packaged assets match source template assets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
