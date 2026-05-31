# First Workspace Tutorial

This tutorial gets you from a blank folder to a validated ICM workspace and a first review gate.

## What You Are Building

You are creating a small workflow where:

1. A project idea becomes a short brief.
2. The brief becomes a discovery report.
3. The discovery report becomes a stage map.
4. Each stage output is reviewed before the next one runs.

The point is not automation for its own sake. The point is to keep the workflow inspectable.

## Step 1: Create A Workspace

From this repository root:

```bash
python -m icm new ../my-first-icm-workspace --name "My First ICM Workspace"
```

Expected output:

```text
Created ICM workspace: /path/to/my-first-icm-workspace
Project name: My First ICM Workspace

Next steps:
  1. cd "/path/to/my-first-icm-workspace"
  2. Fill stages/00_intake/output/project-brief.md
  3. Ask your agent:
     Read AGENTS.md and CONTEXT.md, then run stages/00_intake.
     Write only the declared outputs, run Verify, and stop at the Review Gate.
  4. Run icm validate --strict
```

## Step 2: Fill The First Input

Open:

```text
stages/00_intake/output/project-brief.md
```

Fill it with a rough idea. It does not need to be perfect. ICM expects review and revision.

Example:

```markdown
# Project Brief

## Project Name

Weekly Research Digest

## Desired Outcome

A repeatable workflow for turning source links and notes into a concise weekly research digest.

## Starting Material

- Source links collected during the week
- Notes from the project owner
- Previous digest examples, if available

## Audience Or Users

Busy technical readers who want a clear summary without reading every source.

## Success Criteria

- The digest separates facts, assumptions, and recommendations.
- Every claim can be traced back to source material.
- A human can review the outline before final drafting.

## Constraints

- Time: should fit a weekly publishing rhythm
- Budget: use local files and normal coding-agent tools first
- Tools: markdown, git, local scripts
- Privacy or compliance: do not include private notes in public output
- Must avoid: unsourced claims

## Natural Review Points

- After source triage
- After outline
- Before final publication

## Open Questions

- How long should the final digest be?
- Should the workflow include social posts or only the main digest?
```

## Step 3: Validate The Structure

From the new workspace root:

```bash
python -m icm validate . --strict
```

Expected output:

```text
OK: workspace passed validation with 0 warning(s)
```

This check does not judge whether the content is brilliant. It checks whether the folder structure, stage contracts, and handoff folders are present.

Optional: if your first workspace will track source material, dated milestones, or durable decisions, add the common artifact starters:

```bash
python -m icm init . --with-common-artifacts
```

This creates starter files under `shared/` without overwriting existing files.

## Step 4: Run One Stage

Ask your agent:

```text
Read AGENTS.md and CONTEXT.md, then run stages/00_intake.
Load only the inputs declared in stages/00_intake/CONTEXT.md.
Write only the declared outputs, run Verify, and stop at the Review Gate.
```

When the agent stops, read:

```text
stages/00_intake/output/project-brief.md
```

Edit it directly if needed. Your edits become the authoritative input for the next stage.

## Step 5: Move To The Next Stage

After you accept the brief, ask:

```text
Run stages/01_discovery using the approved output from stages/00_intake.
Write the declared output, run Verify, and stop at the Review Gate.
```

The starter discovery rubric expects the discovery report to include a `Source Traceability` section. If `icm review` says a required source is missing, cite the source path or filename in the output.

Repeat that pattern through the numbered stages.

## CLI Helpers

These commands help you see what is going on:

```bash
python -m icm status .
python -m icm next .
python -m icm explain stages/01_discovery
python -m icm review stages/01_discovery
python -m icm doctor .
python -m icm dashboard .
```

## Step 6: Improve The Source

If you keep fixing the same issue in an output file, move the fix upstream.

| Repeated Problem | Better Source File To Update |
| --- | --- |
| The agent misunderstands the stage job | `stages/NN_slug/CONTEXT.md` |
| The output tone is wrong | `_config/style-guide.md` |
| A domain rule is missing | `_config/glossary.md` or a stage `references/` file |
| A decision should affect later stages | `shared/decision-log.md` |
| The same validation check is repeated manually | Add or update a script under `tools/` |

## Beginner Checklist

- You can explain each numbered stage in one sentence.
- Every stage has a clear input and output.
- Every output is something a human can read.
- The next stage can use the previous output without guessing.
- Review gates happen before expensive mistakes can spread.
