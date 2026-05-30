# Template Design

This template adapts the paper into a model-neutral project starter for VS Code and other agentic coding environments.

## Adaptations

| Paper Pattern | Template Implementation |
| --- | --- |
| `CLAUDE.md` as Layer 0 | `AGENTS.md` as model-neutral Layer 0. Rename or copy it to `CLAUDE.md` if a tool specifically requires that filename. |
| Workspace-level `CONTEXT.md` | Included at the template root with routing and stage index. |
| Stage `CONTEXT.md` contracts | Included for every stage under `stages/`. |
| Stage `references/` folders | Included for stage-local Layer 3 guidance. |
| Stage `output/` folders | Included as Layer 4 handoff points. |
| Local scripts for mechanical work | `tools/validate_icm_workspace.py` and `tools/new_icm_workspace.py`. |

## Why This Is A Workspace-Builder

The paper describes a workspace-builder whose output is a new workspace. That is the most reusable form for "any project I start" because the project type is unknown at template time.

The builder asks six questions in order:

1. What project is being started?
2. What domain and workflow shape does it have?
3. Where are the natural breakpoints and review gates?
4. What folder structure and contracts should be generated?
5. What setup questionnaire is needed to configure the factory?
6. Does the resulting workspace validate and dry-run cleanly?

## Contract Extensions

The paper's basic stage contract is Inputs, Process, Outputs. This template requires two extra headings:

- Review Gate: keeps human oversight explicit.
- Verify: gives each stage a place for cheap local checks and cross-stage consistency tests.

These additions come from the paper's discussion of semantic debugging, source integrity, and future traceability.

## Project Outputs

The builder stages produce markdown plans rather than directly generating files into arbitrary projects. This keeps the first run reviewable. After the scaffold plan is approved, an agent or local script can create the actual project-specific ICM workspace from those plans.

## Codacy-Free By Design

This template does not depend on Codacy or any paid analysis service. Validation is handled with local Python scripts and plain markdown structure checks.