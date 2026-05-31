"""Command-line interface for Interpretable Context Methodology workspaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .workspace import (
    create_workspace,
    doctor_workspace,
    extract_section,
    initialize_workspace,
    next_stage,
    parse_contract_rows,
    review_stage,
    resolve_stage_path,
    suggest_fix,
    unquote_markdown_cell,
    validate_workspace,
    workspace_statuses,
)


def print_common_artifacts(created: tuple[str, ...], skipped: tuple[str, ...]) -> None:
    if not created and not skipped:
        return
    print()
    print("Common artifact starters:")
    for file_name in created:
        print(f"  - {file_name}")
    for file_name in skipped:
        print(f"  - {file_name} (already available)")


def path_text(path: Path) -> str:
    return path.as_posix()


def relative_path_text(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def print_json(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def stage_status_to_json(status, workspace_root: Path) -> dict:
    return {
        "name": status.name,
        "path": relative_path_text(status.path, workspace_root),
        "purpose": status.purpose,
        "state": status.state,
        "note": status.note,
        "declared_outputs": list(status.declared_outputs),
        "existing_outputs": list(status.existing_outputs),
        "missing_outputs": list(status.missing_outputs),
    }


def next_action_to_json(workspace_root: Path, statuses: list) -> dict:
    recommended = next_stage(statuses)
    if not statuses:
        return {
            "type": "run_doctor",
            "message": "No stages found. Run icm doctor for setup checks.",
        }
    if recommended is None:
        return {
            "type": "review_or_restart",
            "message": "All declared outputs are present. Review the latest output or start a new run.",
        }
    relative_stage = relative_path_text(recommended.path, workspace_root)
    if recommended.state == "needs_input":
        intake_path = recommended.path / "output" / "project-brief.md"
        return {
            "type": "fill_intake",
            "stage": recommended.name,
            "path": relative_path_text(intake_path, workspace_root),
            "message": f"Fill or review {relative_stage}/output/project-brief.md.",
        }
    return {
        "type": "run_or_repair_stage",
        "stage": recommended.name,
        "path": relative_stage,
        "message": f"Run or repair {relative_stage}.",
    }


def review_finding_to_json(finding) -> dict:
    suggested_fix_text = None if finding.level == "PASS" else suggest_fix(finding.message)
    return {
        "level": finding.level,
        "message": finding.message,
        "suggested_fix": suggested_fix_text,
    }


def validation_finding_to_json(level: str, message: str) -> dict:
    return {
        "level": level,
        "message": message,
        "suggested_fix": suggest_fix(message),
    }


def review_to_json_payload(workspace_root: Path, target: str, review, strict: bool) -> dict:
    return {
        "command": f"icm review {target} --workspace {path_text(workspace_root)} --json",
        "workspace": path_text(workspace_root),
        "target": target,
        "stage": review.stage_name,
        "stage_path": relative_path_text(review.stage_path, workspace_root),
        "output_path": relative_path_text(review.output_path, workspace_root) if review.output_path is not None else None,
        "strict": strict,
        "passed": review.passed(strict=strict),
        "summary": {
            "fail": len(review.errors),
            "warn": len(review.warnings),
            "pass": len(review.passes),
        },
        "findings": [review_finding_to_json(finding) for finding in review.findings],
        "next_actions": [suggest_fix(finding.message) for finding in (*review.errors, *review.warnings)],
    }


def doctor_to_json_payload(workspace_root: Path, validation_result, doctor_result, statuses: list, strict: bool) -> dict:
    validation_findings = [
        *(validation_finding_to_json("WARN", warning) for warning in validation_result.warnings),
        *(validation_finding_to_json("FAIL", error) for error in validation_result.errors),
    ]
    content_findings = [review_finding_to_json(finding) for finding in doctor_result.findings]
    return {
        "command": f"icm doctor {path_text(workspace_root)} --json",
        "workspace": path_text(workspace_root),
        "strict": strict,
        "passed": validation_result.passed(strict=strict) and doctor_result.passed(strict=strict),
        "structure": {
            "passed": validation_result.passed(strict=False),
            "strict_passed": validation_result.passed(strict=strict),
            "errors": list(validation_result.errors),
            "warnings": list(validation_result.warnings),
            "findings": validation_findings,
        },
        "content": {
            "passed": doctor_result.passed(strict=False),
            "strict_passed": doctor_result.passed(strict=strict),
            "findings": content_findings,
        },
        "stages": [stage_status_to_json(status, workspace_root) for status in statuses],
        "next_action": next_action_to_json(workspace_root, statuses),
    }


def print_creation_next_steps(
    target: Path,
    project_name: str,
    created_common_artifacts: tuple[str, ...] = (),
    skipped_common_artifacts: tuple[str, ...] = (),
) -> None:
    print(f"Created ICM workspace: {target}")
    print(f"Project name: {project_name}")
    print_common_artifacts(created_common_artifacts, skipped_common_artifacts)
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
        created = create_workspace(
            Path(args.target),
            name=args.name,
            include_common_artifacts=args.with_common_artifacts,
        )
    except (FileNotFoundError, ValueError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 1
    print_creation_next_steps(
        created.target,
        created.project_name,
        created.created_common_artifacts,
        created.skipped_common_artifacts,
    )
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    try:
        initialized = initialize_workspace(
            Path(args.target),
            name=args.name,
            include_common_artifacts=args.with_common_artifacts,
        )
    except (FileNotFoundError, ValueError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 1

    print(f"Initialized ICM workspace: {initialized.target}")
    print(f"Project name: {initialized.project_name}")
    print(f"Created files: {len(initialized.created_files)}")
    if initialized.skipped_files:
        print(f"Skipped existing files: {len(initialized.skipped_files)}")
        for file_name in initialized.skipped_files[:8]:
            print(f"  - {file_name}")
        if len(initialized.skipped_files) > 8:
            print(f"  - ...and {len(initialized.skipped_files) - 8} more")
    print_common_artifacts(initialized.created_common_artifacts, initialized.skipped_common_artifacts)
    print()
    print("Next steps:")
    print("  1. Run icm doctor")
    print("  2. Fill stages/00_intake/output/project-brief.md")
    print("  3. Ask your agent to run stages/00_intake and stop at the Review Gate")
    print("  4. Run icm validate --strict")
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
    if args.json:
        payload = {
            "command": f"icm status {path_text(workspace_root)} --json",
            "workspace": path_text(workspace_root),
            "passed": bool(statuses),
            "stages": [stage_status_to_json(status, workspace_root) for status in statuses],
            "next_action": next_action_to_json(workspace_root, statuses),
        }
        print_json(payload)
        return 0 if statuses else 1

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
    result = validate_workspace(workspace_root)
    doctor = doctor_workspace(workspace_root)
    statuses = workspace_statuses(workspace_root)

    if args.json:
        print_json(doctor_to_json_payload(workspace_root, result, doctor, statuses, args.strict))
        return 1 if result.exit_code(strict=args.strict) or doctor.exit_code(strict=args.strict) else 0

    print(f"ICM doctor: {workspace_root}")
    print()

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

    print()
    if doctor.findings:
        print("Content checks: needs attention")
        for finding in (*doctor.failures, *doctor.warnings):
            print(f"{finding.level:<4} {finding.message}")
            print(f"     Fix: {suggest_fix(finding.message)}")
    else:
        print("Content checks: OK")

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

    return 1 if result.exit_code(strict=args.strict) or doctor.exit_code(strict=args.strict) else 0


def cmd_review(args: argparse.Namespace) -> int:
    workspace_root = Path(args.workspace).expanduser().resolve()
    try:
        review = review_stage(workspace_root, args.target)
    except FileNotFoundError as error:
        if args.json:
            print_json(
                {
                    "command": f"icm review {args.target} --workspace {path_text(workspace_root)} --json",
                    "workspace": path_text(workspace_root),
                    "target": args.target,
                    "passed": False,
                    "summary": {"fail": 1, "warn": 0, "pass": 0},
                    "findings": [
                        {
                            "level": "FAIL",
                            "message": str(error),
                            "suggested_fix": suggest_fix(str(error)),
                        }
                    ],
                    "next_actions": [suggest_fix(str(error))],
                }
            )
            return 1
        print(f"ERROR {error}", file=sys.stderr)
        return 1

    if args.json:
        print_json(review_to_json_payload(workspace_root, args.target, review, args.strict))
        return review.exit_code(strict=args.strict)

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


def cmd_dashboard(args: argparse.Namespace) -> int:
    from .dashboard import serve_dashboard

    try:
        serve_dashboard(
            Path(args.workspace),
            host=args.host,
            port=args.port,
            open_browser=not args.no_open,
        )
    except KeyboardInterrupt:
        print()
        print("Dashboard stopped.")
        return 0
    except OSError as error:
        print(f"ERROR Could not start dashboard: {error}", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="icm", description="Work with Interpretable Context Methodology workspaces.")
    parser.add_argument("--version", action="version", version=f"icm {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a new ICM workspace")
    new_parser.add_argument("target", help="Directory to create. It must be empty if it already exists.")
    new_parser.add_argument("--name", help="Human-readable project name. Defaults to the target directory name.")
    new_parser.add_argument(
        "--with-common-artifacts",
        action="store_true",
        help="Add starter source inventory, release calendar, and decision log files under shared/.",
    )
    new_parser.set_defaults(func=cmd_new)

    init_parser = subparsers.add_parser("init", help="Add ICM files to an existing project without overwriting files")
    init_parser.add_argument("target", nargs="?", default=".", help="Project directory to initialize. Defaults to the current directory.")
    init_parser.add_argument("--name", help="Human-readable project name. Defaults to the target directory name.")
    init_parser.add_argument(
        "--with-common-artifacts",
        action="store_true",
        help="Add starter source inventory, release calendar, and decision log files under shared/.",
    )
    init_parser.set_defaults(func=cmd_init)

    validate_parser = subparsers.add_parser("validate", help="Validate an ICM workspace")
    validate_parser.add_argument("workspace", nargs="?", default=".", help="Path to the workspace. Defaults to the current directory.")
    validate_parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    validate_parser.set_defaults(func=cmd_validate)

    status_parser = subparsers.add_parser("status", help="Show stage and output status")
    status_parser.add_argument("workspace", nargs="?", default=".", help="Path to the workspace. Defaults to the current directory.")
    status_parser.add_argument("--json", action="store_true", help="Print machine-readable JSON for dashboard integrations.")
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
    doctor_parser.add_argument("--json", action="store_true", help="Print machine-readable JSON for dashboard integrations.")
    doctor_parser.set_defaults(func=cmd_doctor)

    review_parser = subparsers.add_parser("review", help="Review a stage output against its contract")
    review_parser.add_argument("target", help="Stage name/path or output file path to review.")
    review_parser.add_argument("--workspace", default=".", help="Workspace root. Defaults to the current directory.")
    review_parser.add_argument("--strict", action="store_true", help="Return failure when warnings exist.")
    review_parser.add_argument("--json", action="store_true", help="Print machine-readable JSON for dashboard integrations.")
    review_parser.set_defaults(func=cmd_review)

    dashboard_parser = subparsers.add_parser("dashboard", help="Start a read-only local dashboard")
    dashboard_parser.add_argument("workspace", nargs="?", default=".", help="Path to the workspace. Defaults to the current directory.")
    dashboard_parser.add_argument("--host", default="127.0.0.1", help="Host interface for the local dashboard. Defaults to 127.0.0.1.")
    dashboard_parser.add_argument("--port", type=int, help="Port for the local dashboard. Defaults to 8765 and tries nearby ports if busy.")
    dashboard_parser.add_argument("--no-open", action="store_true", help="Do not open the dashboard in a browser.")
    dashboard_parser.set_defaults(func=cmd_dashboard)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
