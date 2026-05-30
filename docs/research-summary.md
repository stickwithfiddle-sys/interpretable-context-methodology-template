# Research Summary

Source: Jake Van Clief and David McDermott, [arXiv:2603.16021v2](https://arxiv.org/html/2603.16021v2), current as of 2026-05-30.

## Core Claim

Interpretable Context Methodology replaces framework-level orchestration with filesystem structure for sequential, human-reviewed AI workflows. Numbered folders encode stage order. Markdown files encode agent roles, context, inputs, process, and outputs. Local scripts do deterministic mechanical work.

The result is a single agent that changes behavior by reading different stage context rather than a code framework that instantiates multiple agents.

## Design Principles Used In This Template

1. One stage, one job. Each stage has a single responsibility and writes its own output.
2. Plain text as the interface. Markdown and JSON are the default artifacts because humans and tools can inspect them.
3. Layered context loading. Agents read only the context needed for the current stage.
4. Every output is an edit surface. Humans review and revise intermediate files before downstream stages run.
5. Configure the factory, not the product. Stable project preferences live in reference files and improve future runs.

## Five-Layer Context Model

| Layer | Role | Template Location |
| --- | --- | --- |
| 0 | Workspace identity: where am I and how should I behave? | `AGENTS.md` |
| 1 | Workspace routing: where do I go for this task? | `CONTEXT.md` |
| 2 | Stage contract: what do I do now? | `stages/NN_slug/CONTEXT.md` |
| 3 | Reference material: stable rules and reusable constraints | `_config/`, `shared/`, `stages/*/references/` |
| 4 | Working artifacts: per-run inputs and outputs | `stages/*/output/` |

Layer 3 and Layer 4 are intentionally separated. Reference material should constrain behavior; working artifacts should be transformed.

## Stage Contracts

Each stage contract should answer three operational questions:

- Inputs: exactly which Layer 3 and Layer 4 files should the agent load?
- Process: what transformation should the agent perform?
- Outputs: which files should be written, and where?

This template also adds two sections inspired by the paper's future-work discussion:

- Review Gate: what should a human inspect before the next stage runs?
- Verify: what consistency checks should the agent or local scripts run?

## Where ICM Fits

ICM works best for workflows that are sequential, reviewable, and repeatable. Examples from the paper include script-to-animation production, slide deck generation, research analysis, policy workflows, training material development, and workspace-building itself.

ICM is a poor fit for real-time multi-agent collaboration, high-concurrency services, complex automated branching, or systems that need production-grade queues and state isolation.

## Practical Observations From The Paper

- Human edits tend to concentrate near the first stage and final stage: direction-setting early, alignment/debugging late.
- Non-technical users can edit stage behavior by editing `CONTEXT.md` files.
- Copying and adapting an existing workspace is often faster than starting from a blank folder.
- Observability is a side effect: every intermediate artifact is already a readable file.
- Source-level improvements matter. Repeated output edits should become updates to reference files or stage contracts.

## Naming Note

The HTML paper uses Interpretable Context Methodology (ICM). This template uses the full phrase and acronym in public-facing names so the repository is easier to find.
