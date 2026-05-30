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
```

4. Better validator messages with suggested fixes.
5. Example workflows for research, content planning, documentation, and project planning.
6. Docs site generated from the repo docs.

## Dashboard Concept

A dashboard could become the product layer after the CLI and examples are strong.

| View | Purpose |
| --- | --- |
| Stage Map | Show numbered stages, current status, handoffs, and review gates |
| Stage Runner | Show current contract, declared inputs, output diff, and verify results |
| Review Queue | List outputs waiting for human acceptance |
| Source Improvements | Suggest edits to `_config/`, `references/`, or `CONTEXT.md` based on repeated fixes |
| Decision Log | Keep cross-stage decisions visible |
| Workspace Health | Run validator checks and explain fixes |

The dashboard should feel like a cockpit for the workspace, not a replacement for the workspace.

## Product Risks

- Hiding the files would weaken the central ICM idea.
- Adding too many abstractions too early would make beginners learn the product before they learn the workflow.
- A dashboard without strong examples would look polished but fail to teach the method.
- Tying the workflow to one model provider would reduce the template's usefulness.

## Recommended Next Product Step

Build a small `icm` CLI before building a web dashboard. The CLI will clarify the domain language, expose the needed status model, and make the later dashboard much easier to design.
