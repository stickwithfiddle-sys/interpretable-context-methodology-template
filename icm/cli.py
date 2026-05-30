"""Command-line interface for Interpretable Context Methodology workspaces."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .workspace import (
    create_workspace,
    extract_section,
    next_stage,
    parse_contract_rows,
    review_stage,
    resolve_stage_path,
    suggest_fix,
    unquote_markdown_cell,
    validate_workspace,
    workspace_statuses,
)


def print_creation_next_steps(target: Path, project_name: str) -> None:
    print(f"Created ICM workspace: {target}")
    print(f"Project name: {project_name}")
    print()
    print("Next steps:")
    print(f"  1. cd \"{target}\"")
    print("  2. Fill stages/00_intake/output/project-brief.md")
    print("  3. Ask your agent:")
    print("     Read AGENTS.md and CONTEXT.md, then run stages/00_intake.")
    print("     Write only the declared outputs, run Verify, and stop at the Review Gate.")
    print("  4. Run icm validate --strict")


def cmd_new(args: argparse.Namespace) -> int:
    try:
        created = create_workspace(Path(args.target), name=args.name)
    except (FileNotFoundError, ValueError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 1
    print_creation_next_steps(created.target, created.project_name)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    result = validate_workspace(Path(args.workspace))
    for line in result.report_lines(strict=args.strict):
        print(line)
    return result.exit_code(strict=args.strict)


def format_outputs(outputs: tuple[str, ...], missing: tuple[str, ...]) -> str:
    if not outputs:
        return "(none declared)"
    rendered: list[str] = []
    missing_set = set(missing)
    for output in outputs:
        suffix = " missing" if output in missing_set else ""
        rendered.append(f"{output}{suffix}")
    return ", ".join(rendered)


def cmd_status(args: argparse.Namespace) -> int:
    workspace_root = Path(args.workspace).expanduser().resolve()
    statuses = workspace_statuses(workspace_root)
    if not statuses:
        print(f"No stages found in {workspace_root}")
        print("Run icm doctor for setup checks.")
        return 1

    print(f"Workspace: {workspace_root}")
    print()
    print(f"{'Stage':<24} {'State':<18} Outputs")
    print(f"{'-' * 24} {'-' * 18} {'-' * 40}")
    for status in statuses:
        print(f"{status.name:<24} {status.state:<18} {format_outputs(status.declared_outputs, status.missing_outputs)}")

    recommended = next_stage(statuses)
    print()
    if recommended is None:
        print("Next: all declared outputs are present. Review the latest output or start a new run.")
    elif recommended.state == "needs_input":
        print(f"Next: fill or review {recommended.path / 'output' / 'project-brief.md'}")
    else:
        print(f"Next: run or repair {recommended.path.relative_to(workspace_root)}")
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    workspace_root = Path(args.workspace).expanduser().resolve()
    statuses = workspace_statuses(workspace_root)
    recommended = next_stage(statuses)

    if not statuses:
        print("No stages found. Run icm doctor for setup checks.")
        return 1

    if recommended is None:
        print("All declared outputs are present.")
        print("Review the latest stage output, accept the workflow, or start a new run.")
        return 0

    relative_stage = recommended.path.relative_to(workspace_root)
    if recommended.state == "needs_input":
        print("Next action:")
        print(f"Fill or review {relative_stage}/output/project-brief.md")
        print()
        print("Then ask your agent:")
        print(f"Run {relative_stage}. Write the declared output, run Verify, and stop at the Review Gate.")
        return 0

    print("Next agent prompt:")
    print()
    print(f"Run {relative_stage}.")
    print("Load only the inputs declared in that stage's CONTEXT.md.")
    print("Write only the declared outputs, run Verify, and stop at the Review Gate.")
    if recommended.missing_outputs:
        print()
        print("Missing declared outputs:")
        for output in recommended.missing_outputs:
            print(f"- {output}")
    return 0


def print_rows(rows: list, fallback: str) -> None:
    if not rows:
        print(fallback)
        return
    for row in rows:
        cells = [unquote_markdown_cell(cell) for cell in row.cells]
        if len(cells) >= 3:
            print(f"- {cells[0]}: {cells[1]} - {cells[2]}")
        else:
            print("- " + " | ".join(cells))


def cmd_explain(args: argparse.Namespace) -> int:
    workspace_root = Path(args.workspace).expanduser().resolve()
    try:
        stage_path = resolve_stage_path(workspace_root, args.stage)
    except FileNotFoundError as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 1

    context_path = stage_path / "CONTEXT.md"
    if not context_path.exists():
        print(f"ERROR Missing stage contract: {context_path}", file=sys.stderr)
        return 1

    context_markdown = context_path.read_text(encoding="utf-8")
    print(f"Stage: {stage_path.name}")
    print()
    print("Purpose:")
    print(extract_section(context_markdown, "Purpose") or "(missing)")
    print()
    print("Inputs:")
    print_rows(parse_contract_rows(context_markdown, "Inputs"), "(no inputs table found)")
    print()
    print("Outputs:")
    print_rows(parse_contract_rows(context_markdown, "Outputs"), "(no outputs table found)")
    print()
    print("Review Gate:")
    print(extract_section(context_markdown, "Review Gate") or "(missing)")
    print()
    print("Verify:")
    print(extract_section(context_markdown, "Verify") or "(missing)")
    print()
    print("Agent prompt:")
    try:
        relative_stage = stage_path.relative_to(workspace_root)
    except ValueError:
        relative_stage = stage_path
    print(f"Run {relative_stage}. Write the declared outputs, run Verify, and stop at the Review Gate.")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    workspace_root = Path(args.workspace).expanduser().resolve()
    print(f"ICM doctor: {workspace_root}")
    print()

    result = validate_workspace(workspace_root)
    if result.passed(strict=False):
        print("Structure: OK")
    else:
        print("Structure: needs attention")

    if result.warnings:
        print()
        print("Warnings:")
        for warning in result.warnings:
            print(f"- {warning}")
            print(f"  Fix: {suggest_fix(warning)}")

    if result.errors:
        print()
        print("Errors:")
        for error in result.errors:
            print(f"- {error}")
            print(f"  Fix: {suggest_fix(error)}")

    statuses = workspace_statuses(workspace_root)
    if statuses:
        print()
        print("Stage summary:")
        for status in statuses:
            print(f"- {status.name}: {status.state} ({status.note})")

        recommended = next_stage(statuses)
        print()
        if recommended is None:
            print("Likely next action: review the latest output or start a new run.")
        elif recommended.state == "needs_input":
            print(f"Likely next action: fill or review {recommended.path / 'output' / 'project-brief.md'}")
        else:
            try:
                relative_stage = recommended.path.relative_to(workspace_root)
            except ValueError:
                relative_stage = recommended.path
            print(f"Likely next action: run or repair {relative_stage}")

    return result.exit_code(strict=args.strict)


def cmd_review(args: argparse.Namespace) -> int:
    workspace_root = Path(args.workspace).expanduser().resolve()
    try:
        review = review_stage(workspace_root, args.target)
    except FileNotFoundError as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 1

    print(f"Review: {review.stage_name}")
    print(f"Stage path: {review.stage_path}")
    if review.output_path is not None:
        print(f"Output: {review.output_path}")
    print()

    for finding in review.findings:
        print(f"{finding.level:<4} {finding.message}")

    print()
    print(f"Summary: {len(review.errors)} fail, {len(review.warnings)} warn, {len(review.passes)} pass")
    if review.passed(strict=args.strict):
        print("Result: review checks passed.")
    else:
        print("Result: review checks need attention.")

    if review.errors or review.warnings:
        print()
        print("Next actions:")
        for finding in (*review.errors, *review.warnings):
            print(f"- {suggest_fix(finding.message)}")

    return review.exit_code(strict=args.strict)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="icm", description="Work with Interpretable Context Methodology workspaces.")
    parser.add_argument("--version", action="version", version=f"icm {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a new ICM workspace")
    new_parser.add_argument("target", help="Directory to create. It must be empty if it already exists.")
    new_parser.add_argument("--name", help="Human-readable project name. Defaults to the target directory name.")
    new_parser.set_defaults(func=cmd_new)

    validate_parser = subparsers.add_parser("validate", help="Validate an ICM workspace")
    validate_parser.add_argument("workspace", nargs="?", default=".", help="Path to the workspace. Defaults to the current directory.")
    validate_parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    validate_parser.set_defaults(func=cmd_validate)

    status_parser = subparsers.add_parser("status", help="Show stage and output status")
    status_parser.add_argument("workspace", nargs="?", default=".", help="Path to the workspace. Defaults to the current directory.")
    status_parser.set_defaults(func=cmd_status)

    next_parser = subparsers.add_parser("next", help="Print the next recommended action")
    next_parser.add_argument("workspace", nargs="?", default=".", help="Path to the workspace. Defaults to the current directory.")
    next_parser.set_defaults(func=cmd_next)

    explain_parser = subparsers.add_parser("explain", help="Explain a stage contract in plain language")
    explain_parser.add_argument("stage", help="Stage name or path, for example stages/01_discovery or 01_discovery.")
    explain_parser.add_argument("--workspace", default=".", help="Workspace root. Defaults to the current directory.")
    explain_parser.set_defaults(func=cmd_explain)

    doctor_parser = subparsers.add_parser("doctor", help="Diagnose workspace health and likely next action")
    doctor_parser.add_argument("workspace", nargs="?", default=".", help="Path to the workspace. Defaults to the current directory.")
    doctor_parser.add_argument("--strict", action="store_true", help="Return failure when warnings exist.")
    doctor_parser.set_defaults(func=cmd_doctor)

    review_parser = subparsers.add_parser("review", help="Review a stage output against its contract")
    review_parser.add_argument("target", help="Stage name/path or output file path to review.")
    review_parser.add_argument("--workspace", default=".", help="Workspace root. Defaults to the current directory.")
    review_parser.add_argument("--strict", action="store_true", help="Return failure when warnings exist.")
    review_parser.set_defaults(func=cmd_review)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
