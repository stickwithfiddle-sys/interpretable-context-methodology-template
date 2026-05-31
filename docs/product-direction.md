# Product Direction

This repo should become beginner-friendly before it becomes a full product. The filesystem is the core UX: a future app should make the folders easier to understand, not replace them with an opaque database.

## Hermes Agent Inspiration

[NousResearch/hermes-agent](https://github.com/nousresearch/hermes-agent), checked on 2026-05-30, suggests a few product patterns worth adapting:

- A fast first run: one obvious command, then immediate success.
- A setup wizard for configuring providers, tools, and preferences.
- A `doctor`-style diagnostic command for explaining what is broken and how to fix it.
- A command quick reference that separates beginner actions from advanced options.
- Context files, skills, memory, and tools treated as visible user-facing concepts.
- Provider choice without locking the workflow to one model vendor.
- Multiple interfaces over the same core system: CLI, messaging, TUI, and web.

ICM has a different center of gravity. Hermes is an agent runtime that grows with the user; ICM is a workflow architecture where the folder structure is the source of truth. The product opportunity is to make that architecture delightful to create, inspect, validate, and run.

## UX Principles

- Files remain authoritative. The UI reads and writes the workspace, but the workspace should still work without the UI.
- Every screen should answer: what stage am I in, what inputs are loaded, what output changed, and what should the human review?
- The first-run path should avoid theory until the user has seen a stage run.
- Validation should explain fixes in human language, not only report failures.
- Model and editor choices should stay optional. ICM should work with any coding agent that can read files and follow markdown instructions.

## Repo-First Roadmap

1. Beginner README, glossary, tutorial, and completed example workspace.
2. Friendlier command output from `new_icm_workspace.py`.
3. A small CLI facade:

```bash
icm new my-project
icm validate
icm status
icm next
icm explain stages/01_discovery
icm review stages/01_discovery
icm doctor
icm status --json
icm review stages/01_discovery --json
icm doctor --json
icm dashboard
```

4. Better validator messages with suggested fixes.
5. Example workflows for research, content planning, documentation, and project planning.
6. Docs site generated from the repo docs.

## Current Product Spine

The CLI now supports both adoption paths:

```bash
icm new my-project
icm init . --with-common-artifacts
icm doctor
icm review stages/01_discovery
icm status --json
icm dashboard .
```

`icm new` is for a clean workspace. `icm init` is for an existing project and skips files that already exist. The `--with-common-artifacts` flag adds starter files for source inventories, release calendars, and decision logs. `icm doctor` checks both structure and content-quality issues such as empty required sections, missing config inputs, undeclared outputs, broken handoffs after outputs are present, and review-rubric failures on declared outputs. `icm review` can load artifact-specific rubrics from stage references, including source-traceability checks, required table-column checks, link/path-count checks, and artifact-shape checks for source inventories, calendars, and decision logs.

The example library now covers content planning, research briefs, documentation refreshes, and project planning. The documentation-refresh and project-planning examples are the clearest demos of the review system because their discovery reports must include a `Source Traceability` table, and their validation stages include source inventories, calendars, and decision logs checked by artifact-shape rubrics. `docs/workflow-rubrics.md` helps beginners choose validators by use case, and `docs/first-10-minutes.md` gives them a fast install-to-review loop before they read the deeper tutorial. `icm dashboard` now gives those same users a read-only browser view over the CLI JSON contract.

## Dashboard Concept

The first dashboard is a read-only local product layer over the CLI and examples.

| View | Purpose |
| --- | --- |
| Stage Map | Show numbered stages, current status, handoffs, and review gates |
| Stage Runner | Show current contract, declared inputs, output diff, and verify results |
| Review Queue | List outputs waiting for human acceptance |
| Source Improvements | Suggest edits to `_config/`, `references/`, or `CONTEXT.md` based on repeated fixes |
| Decision Log | Keep cross-stage decisions visible |
| Workspace Health | Run validator checks and explain fixes |

The dashboard should feel like a cockpit for the workspace, not a replacement for the workspace.

The dashboard-readiness spec in `docs/dashboard-readiness.md` narrows the prototype to local files, review queues, artifact-shape failures, doctor findings, and explicit human acceptance. The JSON contract in `docs/json-output.md` gives the dashboard stable `status`, `review`, and `doctor` data without inventing a second source of truth. The current read-only implementation is documented in `docs/dashboard-prototype.md`.

## Product Risks

- Hiding the files would weaken the central ICM idea.
- Adding too many abstractions too early would make beginners learn the product before they learn the workflow.
- A dashboard without strong examples would look polished but fail to teach the method.
- Tying the workflow to one model provider would reduce the template's usefulness.

## Recommended Next Product Step

Next, define a human acceptance marker for reviewed handoffs without hiding markdown. A read/write dashboard should wait until acceptance is represented clearly in the filesystem model.
