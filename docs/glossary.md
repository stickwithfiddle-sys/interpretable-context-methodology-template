# ICM Glossary

Plain-language terms for reading and using this repository.

| Term | Meaning | Example |
| --- | --- | --- |
| ICM | Interpretable Context Methodology. A way to use folders and markdown files as the architecture for staged agent work. | A research workflow with `00_intake`, `01_discovery`, and `02_stage_mapping` folders |
| Workspace | The project folder that contains the ICM files. | `my-first-icm-workspace/` |
| Stage | One numbered step in the workflow. A stage should have one job. | `stages/01_discovery/` |
| Stage contract | The `CONTEXT.md` file inside a stage. It tells the agent what to read, do, write, review, and verify. | `stages/01_discovery/CONTEXT.md` |
| Handoff | The output from one stage that becomes input to a later stage. | `project-brief.md` becomes input for discovery |
| Review gate | A deliberate stopping point where a human checks the output before the workflow continues. | Reviewing `stage-map.md` before scaffolding |
| Layer 0 | Workspace identity and overall agent operating rules. | `AGENTS.md` |
| Layer 1 | Workspace routing and stage index. | Root `CONTEXT.md` |
| Layer 2 | Stage-specific instructions. | `stages/02_stage_mapping/CONTEXT.md` |
| Layer 3 | Stable reference material that should be reused across runs. | `_config/quality-gates.md`, `references/stage-patterns.md` |
| Layer 4 | Working artifacts that change during a run. | Files in `stages/*/output/` |
| Source-level improvement | Moving a repeated manual fix into a reusable instruction, reference, or script. | Updating `_config/style-guide.md` after fixing tone repeatedly |
| Deterministic check | A check that code can perform reliably without model judgment. | Verifying every stage has `CONTEXT.md`, `references/`, and `output/` |
| Builder workspace | A workspace whose job is to design another ICM workspace. | The default template in this repository |
| Project-specific workspace | A generated workspace customized for one project or workflow. | A content-planning ICM workspace |
| Agent prompt file | Optional editor prompt that gives a reusable command to an agent. | `.github/prompts/run-icm-stage.prompt.md` |

## One-Minute Version

An ICM workspace is a folder-based checklist for an AI agent. The agent reads the root rules, opens one stage, reads only the inputs named by that stage, writes the declared output, and stops so a human can review the handoff.
