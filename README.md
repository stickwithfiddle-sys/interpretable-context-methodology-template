# Interpretable Context Methodology (ICM) Reusable Template

This repository turns the paper [Interpretable Context Methodology: Folder Structure as Agent Architecture](https://arxiv.org/html/2603.16021v2) into a reusable starter kit for new projects.

ICM is useful when a workflow is sequential, reviewable, and repeatable: one stage produces a plain-text artifact, a human can inspect or edit it, and the next stage reads that artifact as input. The folder structure becomes the orchestration layer. Markdown files define agent behavior. Small scripts handle deterministic mechanical checks.

## Status

Experimental starter kit. The template is intended to make ICM easy to try, inspect, and adapt; it is not an official release of the original ICM protocol.

Maintained by Hobo.

## Quick Start

Create a new ICM workspace from the template:

```powershell
python tools/new_icm_workspace.py ..\my-new-project --name "My New Project"
```

Validate the template itself:

```powershell
python tools/validate_icm_workspace.py templates\icm-workspace --strict
```

After creating a project workspace:

1. Open the new folder.
2. Fill in `stages/00_intake/output/project-brief.md`.
3. Ask your agent to run `stages/00_intake`, then review the output before moving on.
4. Continue through each numbered stage, editing outputs at review gates.
5. When a repeated edit pattern appears, update the stage contract or reference file so future runs improve at the source.

## What Is Included

```text
templates/icm-workspace/
  AGENTS.md                 Layer 0: workspace identity and agent operating rules
  CONTEXT.md                Layer 1: routing and stage index
  _config/                  Layer 3: stable project rules and reusable preferences
  _templates/               Reusable markdown templates for new stages and reviews
  shared/                   Cross-stage notes, decisions, backlog, and glossary
  stages/                   Layer 2 stage contracts and Layer 4 output folders
  .github/prompts/          Optional VS Code prompt files for running/reviewing stages
tools/
  new_icm_workspace.py      Copies the template into a new project folder
  validate_icm_workspace.py Checks stage naming, contracts, and handoff folders
docs/
  research-summary.md       Practical findings extracted from the paper
  template-design.md        Design decisions and adaptation notes
```

## Builder Pipeline

The included template is a workspace-builder. Its output is a project-specific ICM workspace.

| Stage | Purpose | Main Output |
| --- | --- | --- |
| `00_intake` | Capture the project brief and constraints | `project-brief.md` |
| `01_discovery` | Identify domain, users, deliverables, risks, and workflow shape | `discovery-report.md` |
| `02_stage_mapping` | Choose natural breakpoints, review gates, and handoffs | `stage-map.md` |
| `03_scaffold` | Define the project workspace tree and stage contracts | `scaffold-plan.md` |
| `04_questionnaire` | Produce setup questions and reference-material prompts | `setup-questionnaire.md` |
| `05_validation` | Dry-run the workflow and report gaps before use | `validation-report.md` |

## When To Use ICM

Use it for project planning, research synthesis, content production, analysis workflows, deliverable pipelines, documentation systems, and other work where intermediate artifacts should be readable and editable.

Use a conventional framework instead when you need real-time multi-agent collaboration, high-concurrency service infrastructure, automated branching based on model decisions, or tight message-passing loops.

## Research Basis

The ICM paper was authored by Jake Van Clief and David McDermott. It argues for five design principles: one stage, one job; plain text as the interface; layered context loading; every output as an edit surface; and configuring the factory rather than each product. This template applies those principles with a model-neutral `AGENTS.md` Layer 0 file, explicit stage contracts, scoped Layer 3 references, Layer 4 output handoffs, and a validator script.

See [docs/research-summary.md](docs/research-summary.md) for the research notes and [docs/template-design.md](docs/template-design.md) for implementation choices.

## Attribution

This project is an independent reusable template based on the paper:

> Jake Van Clief and David McDermott. "Interpretable Context Methodology: Folder Structure as Agent Architecture." arXiv:2603.16021v2, 18 Mar. 2026.

The ICM protocol referenced by the paper is described as open source under the MIT license. This repository is a derived starter template and should not be read as an official repository or endorsement by the paper authors.

## License

MIT. See [LICENSE](LICENSE).
