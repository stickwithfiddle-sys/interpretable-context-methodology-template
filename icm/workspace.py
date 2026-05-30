"""Workspace operations for the ICM CLI."""

from __future__ import annotations

import datetime as dt
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "templates" / "icm-workspace"
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".ps1", ".gitignore"}
STAGE_NAME_PATTERN = re.compile(r"^\d{2}_[a-z0-9][a-z0-9_-]*$")
REQUIRED_STAGE_HEADINGS = ("Inputs", "Process", "Outputs", "Review Gate", "Verify")
REQUIRED_ROOT_DIRECTORIES = ("_config", "_templates", "shared", "stages")


@dataclass(frozen=True)
class WorkspaceCreation:
    target: Path
    project_name: str


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    def passed(self, strict: bool = False) -> bool:
        return not self.errors and not (strict and self.warnings)

    def exit_code(self, strict: bool = False) -> int:
        return 0 if self.passed(strict=strict) else 1

    def report_lines(self, strict: bool = False) -> list[str]:
        lines: list[str] = []
        lines.extend(f"WARN  {warning}" for warning in self.warnings)
        lines.extend(f"ERROR {error}" for error in self.errors)
        if self.passed(strict=strict):
            lines.append(f"OK: workspace passed validation with {len(self.warnings)} warning(s)")
        else:
            lines.append(f"FAILED: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
        return lines


@dataclass(frozen=True)
class TableRow:
    cells: tuple[str, ...]


@dataclass(frozen=True)
class StageStatus:
    name: str
    path: Path
    purpose: str
    declared_outputs: tuple[str, ...]
    existing_outputs: tuple[str, ...]
    missing_outputs: tuple[str, ...]
    state: str
    note: str


@dataclass(frozen=True)
class ReviewFinding:
    level: str
    message: str


@dataclass(frozen=True)
class StageReview:
    stage_name: str
    stage_path: Path
    output_path: Path | None
    findings: tuple[ReviewFinding, ...]

    @property
    def errors(self) -> tuple[ReviewFinding, ...]:
        return tuple(finding for finding in self.findings if finding.level == "FAIL")

    @property
    def warnings(self) -> tuple[ReviewFinding, ...]:
        return tuple(finding for finding in self.findings if finding.level == "WARN")

    @property
    def passes(self) -> tuple[ReviewFinding, ...]:
        return tuple(finding for finding in self.findings if finding.level == "PASS")

    def passed(self, strict: bool = False) -> bool:
        return not self.errors and not (strict and self.warnings)

    def exit_code(self, strict: bool = False) -> int:
        return 0 if self.passed(strict=strict) else 1


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


def create_workspace(target: Path, name: str | None = None) -> WorkspaceCreation:
    if not TEMPLATE_ROOT.exists():
        raise FileNotFoundError(f"Template folder not found: {TEMPLATE_ROOT}")

    resolved_target = target.expanduser().resolve()
    project_name = name or resolved_target.name.replace("-", " ").replace("_", " ").title()
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROJECT_SLUG}}": slugify(project_name),
        "{{CREATED_DATE}}": dt.date.today().isoformat(),
    }

    ensure_empty_target(resolved_target)
    copy_template(resolved_target)
    replace_tokens(resolved_target, replacements)
    return WorkspaceCreation(target=resolved_target, project_name=project_name)


def has_heading(markdown: str, heading: str) -> bool:
    pattern = re.compile(rf"^#+\s+{re.escape(heading)}\s*$", re.IGNORECASE | re.MULTILINE)
    return bool(pattern.search(markdown))


def collect_stage_directories(workspace_root: Path) -> list[Path]:
    stages_root = workspace_root / "stages"
    if not stages_root.exists():
        return []
    return sorted(path for path in stages_root.iterdir() if path.is_dir())


def validate_workspace(workspace_root: Path) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    workspace_root = workspace_root.expanduser().resolve()

    if not workspace_root.exists():
        errors.append(f"Workspace does not exist: {workspace_root}")
    elif not workspace_root.is_dir():
        errors.append(f"Workspace is not a directory: {workspace_root}")

    if errors:
        return ValidationResult(errors=tuple(errors), warnings=tuple(warnings))

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

    return ValidationResult(errors=tuple(errors), warnings=tuple(warnings))


def extract_section(markdown: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", markdown[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end].strip()


def first_paragraph(markdown: str) -> str:
    for block in re.split(r"\n\s*\n", markdown.strip()):
        text = " ".join(line.strip() for line in block.splitlines()).strip()
        if text:
            return text
    return ""


def split_markdown_table_row(line: str) -> TableRow | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    cells = tuple(cell.strip() for cell in stripped.strip("|").split("|"))
    if not cells:
        return None
    if all(not cell.replace("-", "").replace(":", "").strip() for cell in cells):
        return None
    return TableRow(cells=cells)


def parse_markdown_table(section: str) -> list[TableRow]:
    rows: list[TableRow] = []
    for line in section.splitlines():
        row = split_markdown_table_row(line)
        if row is None:
            continue
        if rows or not any(cell.lower() in {"layer", "file", "path", "location", "purpose", "use"} for cell in row.cells):
            rows.append(row)
    return rows


def unquote_markdown_cell(cell: str) -> str:
    match = re.search(r"`([^`]+)`", cell)
    if match:
        return match.group(1).strip()
    return cell.strip()


def parse_declared_outputs(context_markdown: str) -> tuple[str, ...]:
    outputs_section = extract_section(context_markdown, "Outputs")
    outputs: list[str] = []
    for row in parse_markdown_table(outputs_section):
        if len(row.cells) < 2:
            continue
        output_name = unquote_markdown_cell(row.cells[0])
        location = unquote_markdown_cell(row.cells[1])
        if output_name.lower() == "file" or not output_name:
            continue
        if "output" in location:
            outputs.append(output_name)
    return tuple(outputs)


def parse_contract_rows(context_markdown: str, section_name: str) -> list[TableRow]:
    return parse_markdown_table(extract_section(context_markdown, section_name))


def parse_input_paths(context_markdown: str) -> tuple[str, ...]:
    paths: list[str] = []
    for row in parse_contract_rows(context_markdown, "Inputs"):
        if len(row.cells) < 2:
            continue
        input_path = unquote_markdown_cell(row.cells[1])
        if input_path.lower() == "path" or not input_path:
            continue
        paths.append(input_path)
    return tuple(paths)


def parse_output_specs(context_markdown: str) -> tuple[tuple[str, str], ...]:
    specs: list[tuple[str, str]] = []
    for row in parse_contract_rows(context_markdown, "Outputs"):
        if len(row.cells) < 2:
            continue
        output_name = unquote_markdown_cell(row.cells[0])
        location = unquote_markdown_cell(row.cells[1])
        if output_name.lower() == "file" or not output_name:
            continue
        specs.append((output_name, location))
    return tuple(specs)


def existing_output_files(stage_directory: Path) -> tuple[str, ...]:
    output_dir = stage_directory / "output"
    if not output_dir.is_dir():
        return ()
    return tuple(sorted(path.name for path in output_dir.iterdir() if path.is_file() and path.name != ".gitkeep"))


def section_has_content(markdown: str, heading: str) -> bool:
    content = extract_section(markdown, heading)
    stripped = "\n".join(line.strip() for line in content.splitlines()).strip()
    if not stripped:
        return False
    if stripped in {"-", "- ", "N/A", "n/a"}:
        return False
    return True


def intake_needs_input(stage_directory: Path) -> bool:
    brief_path = stage_directory / "output" / "project-brief.md"
    if not brief_path.exists():
        return False
    text = brief_path.read_text(encoding="utf-8")
    required_sections = ("Desired Outcome", "Audience Or Users", "Success Criteria")
    return any(not section_has_content(text, section) for section in required_sections)


def stage_status(stage_directory: Path) -> StageStatus:
    context_path = stage_directory / "CONTEXT.md"
    if not context_path.exists():
        return StageStatus(
            name=stage_directory.name,
            path=stage_directory,
            purpose="Missing CONTEXT.md",
            declared_outputs=(),
            existing_outputs=existing_output_files(stage_directory),
            missing_outputs=(),
            state="missing_contract",
            note="Add a stage CONTEXT.md before running this stage.",
        )

    context_markdown = context_path.read_text(encoding="utf-8")
    declared_outputs = parse_declared_outputs(context_markdown)
    existing_outputs = existing_output_files(stage_directory)
    missing_outputs = tuple(output for output in declared_outputs if output not in existing_outputs)
    purpose = first_paragraph(extract_section(context_markdown, "Purpose")) or "No purpose found."

    if stage_directory.name.startswith("00_") and intake_needs_input(stage_directory):
        state = "needs_input"
        note = "Fill or review the intake brief before running downstream stages."
    elif missing_outputs and existing_outputs:
        state = "partial"
        note = "Some declared outputs are missing."
    elif missing_outputs:
        state = "waiting"
        note = "No declared output is ready yet."
    else:
        state = "ready_for_review"
        note = "Declared outputs are present; review before continuing."

    return StageStatus(
        name=stage_directory.name,
        path=stage_directory,
        purpose=purpose,
        declared_outputs=declared_outputs,
        existing_outputs=existing_outputs,
        missing_outputs=missing_outputs,
        state=state,
        note=note,
    )


def workspace_statuses(workspace_root: Path) -> list[StageStatus]:
    return [stage_status(stage_directory) for stage_directory in collect_stage_directories(workspace_root.expanduser().resolve())]


def next_stage(statuses: list[StageStatus]) -> StageStatus | None:
    for status in statuses:
        if status.state == "needs_input":
            return status
    for status in statuses:
        if status.state in {"missing_contract", "partial", "waiting"}:
            return status
    return None


def resolve_stage_path(workspace_root: Path, stage: str) -> Path:
    workspace_root = workspace_root.expanduser().resolve()
    candidate = Path(stage).expanduser()
    if candidate.is_absolute() and candidate.exists():
        return candidate
    if candidate.exists():
        return candidate.resolve()
    workspace_candidate = workspace_root / stage
    if workspace_candidate.exists():
        return workspace_candidate.resolve()
    stages_candidate = workspace_root / "stages" / stage
    if stages_candidate.exists():
        return stages_candidate.resolve()
    raise FileNotFoundError(f"Stage not found: {stage}")


def find_stage_for_output(workspace_root: Path, output_path: Path) -> Path:
    workspace_root = workspace_root.expanduser().resolve()
    resolved_output = output_path.expanduser().resolve()
    if not resolved_output.exists() or not resolved_output.is_file():
        raise FileNotFoundError(f"Output file not found: {output_path}")

    if resolved_output.parent.name == "output" and (resolved_output.parent.parent / "CONTEXT.md").exists():
        return resolved_output.parent.parent

    for parent in resolved_output.parents:
        if (parent / "CONTEXT.md").exists() and parent.parent.name == "stages":
            return parent

    try:
        resolved_output.relative_to(workspace_root)
    except ValueError:
        pass

    raise FileNotFoundError(f"Could not find a containing ICM stage for output: {output_path}")


def resolve_review_target(workspace_root: Path, target: str) -> tuple[Path, Path | None]:
    candidate = Path(target).expanduser()
    workspace_root = workspace_root.expanduser().resolve()

    if candidate.exists() and candidate.is_file():
        output_path = candidate.resolve()
        return find_stage_for_output(workspace_root, output_path), output_path

    workspace_candidate = workspace_root / target
    if workspace_candidate.exists() and workspace_candidate.is_file():
        output_path = workspace_candidate.resolve()
        return find_stage_for_output(workspace_root, output_path), output_path

    stage_path = resolve_stage_path(workspace_root, target)
    return stage_path, None


def resolve_contract_path(stage_path: Path, contract_path: str) -> Path:
    return (stage_path / contract_path).resolve()


def path_label(stage_path: Path, path: Path) -> str:
    try:
        return str(path.relative_to(stage_path))
    except ValueError:
        return str(path)


def review_stage(workspace_root: Path, target: str) -> StageReview:
    stage_path, requested_output = resolve_review_target(workspace_root, target)
    context_path = stage_path / "CONTEXT.md"
    findings: list[ReviewFinding] = []

    if not context_path.exists():
        return StageReview(
            stage_name=stage_path.name,
            stage_path=stage_path,
            output_path=requested_output,
            findings=(ReviewFinding("FAIL", f"Missing stage contract: {context_path}"),),
        )

    context_markdown = context_path.read_text(encoding="utf-8")
    for heading in REQUIRED_STAGE_HEADINGS:
        if has_heading(context_markdown, heading):
            findings.append(ReviewFinding("PASS", f"Contract has required heading: {heading}"))
        else:
            findings.append(ReviewFinding("FAIL", f"Contract missing required heading: {heading}"))

    purpose = extract_section(context_markdown, "Purpose")
    if first_paragraph(purpose):
        findings.append(ReviewFinding("PASS", "Purpose is present."))
    else:
        findings.append(ReviewFinding("FAIL", "Purpose section is empty."))

    input_paths = parse_input_paths(context_markdown)
    if not input_paths:
        findings.append(ReviewFinding("WARN", "No declared inputs found."))
    for input_path in input_paths:
        resolved_input = resolve_contract_path(stage_path, input_path)
        if resolved_input.exists():
            findings.append(ReviewFinding("PASS", f"Declared input exists: {input_path}"))
        else:
            findings.append(ReviewFinding("FAIL", f"Declared input is missing: {input_path}"))

    output_specs = parse_output_specs(context_markdown)
    if not output_specs:
        findings.append(ReviewFinding("FAIL", "No declared outputs found."))

    declared_output_names = {output_name for output_name, _ in output_specs}
    selected_output_name = requested_output.name if requested_output is not None else None
    if selected_output_name and selected_output_name not in declared_output_names:
        findings.append(ReviewFinding("WARN", f"Requested output is not declared by the stage: {selected_output_name}"))

    for output_name, location in output_specs:
        if requested_output is not None and output_name != requested_output.name:
            continue
        output_path = resolve_contract_path(stage_path, str(Path(location) / output_name))
        if not output_path.exists():
            findings.append(ReviewFinding("FAIL", f"Declared output is missing: {path_label(stage_path, output_path)}"))
            continue
        if output_path.parent.name != "output":
            findings.append(ReviewFinding("WARN", f"Declared output is outside output/: {path_label(stage_path, output_path)}"))
        else:
            findings.append(ReviewFinding("PASS", f"Declared output is in output/: {output_name}"))
        if output_path.stat().st_size == 0:
            findings.append(ReviewFinding("FAIL", f"Declared output is empty: {output_name}"))
        else:
            findings.append(ReviewFinding("PASS", f"Declared output has content: {output_name}"))
        if output_name == "project-brief.md" and intake_needs_input(stage_path):
            findings.append(
                ReviewFinding(
                    "FAIL",
                    "Project brief is missing one or more required sections: Desired Outcome, Audience Or Users, Success Criteria",
                )
            )

    extra_outputs = set(existing_output_files(stage_path)) - declared_output_names
    if requested_output is None:
        for output_name in sorted(extra_outputs):
            findings.append(ReviewFinding("WARN", f"Output file is not declared in the contract: output/{output_name}"))

    review_gate = extract_section(context_markdown, "Review Gate")
    if first_paragraph(review_gate):
        findings.append(ReviewFinding("PASS", "Review Gate gives the human something to inspect."))
    else:
        findings.append(ReviewFinding("FAIL", "Review Gate is empty."))

    verify = extract_section(context_markdown, "Verify")
    if first_paragraph(verify):
        findings.append(ReviewFinding("PASS", "Verify section is present."))
    else:
        findings.append(ReviewFinding("FAIL", "Verify section is empty."))

    if requested_output is not None and requested_output.exists() and requested_output.stat().st_size > 0:
        text = requested_output.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^#\s+", text, re.MULTILINE):
            findings.append(ReviewFinding("PASS", f"Requested output has a top-level heading: {requested_output.name}"))
        else:
            findings.append(ReviewFinding("WARN", f"Requested output has no top-level markdown heading: {requested_output.name}"))

    return StageReview(
        stage_name=stage_path.name,
        stage_path=stage_path,
        output_path=requested_output,
        findings=tuple(findings),
    )


def suggest_fix(message: str) -> str:
    if "Missing Layer 0" in message:
        return "Add AGENTS.md at the workspace root, or copy it from templates/icm-workspace/."
    if "Missing Layer 1" in message:
        return "Add CONTEXT.md at the workspace root with the stage index and routing notes."
    if "Missing required directory" in message:
        directory = message.rsplit(":", 1)[-1].strip()
        return f"Create {directory} at the workspace root."
    if "No stage directories" in message:
        return "Create at least one numbered stage under stages/, for example stages/00_intake/."
    if "Stage name should match" in message:
        return "Rename the folder to NN_slug format, for example 01_discovery."
    if "Missing stage contract" in message:
        return "Add CONTEXT.md to the stage folder using templates/icm-workspace/_templates/stage-context.md."
    if "missing heading" in message:
        return "Add the missing required heading to the stage CONTEXT.md."
    if "Missing Layer 3 folder" in message:
        return "Create a references/ folder inside the stage."
    if "Missing Layer 4" in message:
        return "Create an output/ folder inside the stage."
    if "Declared input is missing" in message:
        missing_path = message.rsplit(":", 1)[-1].strip()
        return f"Create or restore the declared input, or update the Inputs table if it should not be required: {missing_path}"
    if "Declared output is missing" in message:
        missing_path = message.rsplit(":", 1)[-1].strip()
        return f"Run the stage or create the declared output before review: {missing_path}"
    if "Declared output is empty" in message:
        output_name = message.rsplit(":", 1)[-1].strip()
        return f"Fill the output file with the artifact required by the stage contract: {output_name}"
    if "not declared in the contract" in message:
        return "Either add the file to the Outputs table or move it out of the stage output folder."
    if "Requested output is not declared" in message:
        return "Review the stage Outputs table and either declare this output or choose a declared output file."
    if "Project brief is missing" in message:
        return "Fill Desired Outcome, Audience Or Users, and Success Criteria before treating intake as reviewed."
    if "top-level markdown heading" in message:
        return "Add a top-level markdown heading so the artifact is easier to scan and review."
    return "Review the named file or folder and align it with the ICM template."
