# First 10 Minutes With ICM

This is the shortest path from "I installed the package" to "I understand the loop."

The goal is not to finish a full workflow. The goal is to see the ICM rhythm once:

1. Create a workspace.
2. Fill the first brief.
3. Ask an agent to run one stage.
4. Review the output.
5. Validate the workspace.

## Minute 0: Install

Use a virtual environment so the trial stays clean:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install icm-workspace-template
icm --version
```

Expected version for this release:

```text
icm 0.17.0
```

## Minute 1: Create A Workspace

```bash
icm new my-first-icm-workspace --name "My First ICM Workspace" --with-common-artifacts
cd my-first-icm-workspace
```

The `--with-common-artifacts` flag adds starter files for source inventories, release calendars, and decision logs. You can ignore them at first, but they are useful once a workflow needs traceability.

## Minute 2: Open The First Brief

Open this file:

```text
stages/00_intake/output/project-brief.md
```

Paste a small brief:

```markdown
# Project Brief

## Project Name

Weekly Research Digest

## Desired Outcome

A repeatable workflow for turning source links and notes into a concise weekly research digest.

## Starting Material

- Source links collected during the week
- Notes from the project owner

## Audience Or Users

Busy technical readers who want the important points without reading every source.

## Success Criteria

- Claims cite their source material.
- A human reviews the outline before final drafting.
- The workflow can be repeated next week.

## Constraints

- Keep the first version small.
- Use markdown files and normal coding-agent tools.
- Avoid unsourced claims.

## Natural Review Points

- After source triage
- After outline
- Before final publication

## Open Questions

- How long should the digest be?
- Should the workflow create social posts too?
```

## Minute 4: Ask Your Agent To Run One Stage

Use this prompt:

```text
Read AGENTS.md and CONTEXT.md, then run stages/00_intake.
Load only the inputs declared in stages/00_intake/CONTEXT.md.
Write only the declared outputs, run Verify, and stop at the Review Gate.
```

The important part is "one stage." ICM works because each handoff is small enough to inspect.

## Minute 7: Review The Output

Read:

```text
stages/00_intake/output/project-brief.md
```

Edit it directly if needed. The file is now the source of truth for the next stage.

Record the human acceptance in plain markdown:

```bash
icm accept stages/00_intake --reviewer "Hobo" --note "Brief is ready for discovery."
```

Then ask:

```text
Run stages/01_discovery using the approved output from stages/00_intake.
Write the declared output, run Verify, and stop at the Review Gate.
```

## Minute 9: Check The Workspace

Run:

```bash
icm doctor .
icm validate . --strict
```

`icm doctor` explains what needs attention. `icm validate --strict` confirms the workspace structure is still sound.

## Minute 10: Know What You Just Learned

You have seen the whole loop:

| Habit | Why It Matters |
| --- | --- |
| One numbered stage at a time | Keeps context small and reviewable |
| Markdown contracts | Makes instructions visible |
| Output files as handoffs | Gives the next stage a stable input |
| Review gates | Lets humans stop drift early |
| Doctor and validate | Separates repair guidance from structure checks |

## What To Try Next

- Run `icm status .` to see stage state.
- Run `icm next .` to see the likely next stage.
- Run `icm explain stages/01_discovery` to inspect the stage contract.
- Run `icm review stages/01_discovery` after the discovery output exists.
- Run `icm accept stages/01_discovery` when a human approves the discovery handoff.
- Run `icm dashboard .` when you want a read-only browser view.
- Read [handoff-acceptance.md](handoff-acceptance.md) to understand machine-passing vs accepted outputs.
- Read [demo.md](demo.md) to see completed review checks.
- Read [e2e-playtest.md](e2e-playtest.md) when you want a complete idea and full workflow script.
- Read [workflow-rubrics.md](workflow-rubrics.md) when you want deterministic artifact checks.
