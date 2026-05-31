# Revision Audit

Last updated: 2026-05-30

Current release: `0.13.0`

## What We Have Achieved

- Public GitHub-ready project with MIT licensing, NOTICE attribution, changelog, contribution guide, issue templates, pull request template, and release process.
- Correct ICM attribution to Jake Van Clief and David McDermott, with Hobo credited as the template maintainer.
- Installable `icm` CLI for creating, validating, inspecting, explaining, reviewing, and diagnosing workspaces.
- Package-embedded template assets so `icm new` works outside a source checkout.
- Completed example workspace that shows what a successful run looks like.
- Beginner docs for install, first workspace, glossary, product direction, release process, and template design.
- CI smoke tests, wheel install smoke tests, package asset checks, and pytest coverage for CLI and workspace helpers.
- Security policy and code ownership so contribution paths are public while protected code changes stay maintainer-controlled.
- Safe `icm init` flow for adding ICM to an existing project without overwriting files.
- Richer `icm doctor` content checks for empty sections, missing inputs, undeclared outputs, and broken handoffs.
- GitHub Pages docs homepage with visual CLI screenshots and a workspace flow diagram.
- Artifact-specific `icm review` rubrics for required sections, required terms, and forbidden terms.
- Source-traceability rubric checks that require outputs to cite source paths or filenames.
- A second completed example workspace for a research-brief workflow.
- Live PyPI package, PyPI readiness checks, package build/render checks, and a manual Trusted Publishing workflow.
- A copy-paste demo walkthrough linked from the docs homepage.
- Deterministic rubric checks for required markdown table columns and minimum link/path reference counts.
- A third completed example workspace for a documentation-refresh workflow.
- Deterministic artifact-shape rubric checks for source inventories, calendars, and decision logs.
- Beginner-facing PyPI upgrade and install verification documentation.
- Optional common artifact starter files through `icm new/init --with-common-artifacts`.
- `icm doctor` now surfaces review-rubric failures for existing declared outputs.
- Release-ready workspace documentation tying together validation, review, changelog updates, and PyPI upgrade checks.
- A completed project-planning example workspace with source-inventory, project-calendar, and decision-log checks.
- Workflow-specific rubric guidance for choosing validators by use case.

## Roadmap Position

The current `Now` work is mostly in place: first-run clarity, self-contained generated workspaces, PyPI install reliability, release hygiene, safe existing-project adoption, visual docs, deterministic review rubrics, source traceability, table/path checks, source-inventory/calendar/decision-log checks, common artifact starters, doctor-surfaced rubric failures, release-ready docs, workflow-specific rubric guidance, and four completed examples are all covered.

The highest-value `Next` work is:

- More example workspaces for project planning and other common use cases.
- Short recorded demo or animated walkthrough for the docs site.
- More workflow-specific rubric guidance for beginners.
- A dashboard prototype once the CLI vocabulary and example library settle.

## Beginner UX Assessment

The product is beginner-friendly for a technical user who can run Python commands. A new user can install the CLI, create or initialize a workspace, add common artifact starters, fill the first brief, run doctor checks, validate structure, inspect completed examples, and choose a rubric pattern by workflow type.

It is closer to world-class beginner UX, but not there yet. The main gaps are no short demo recording, no project-planning example, and no local dashboard for visual review queues.

## Direction Options

1. Demo polish: add a short screen recording or animated walkthrough.
2. Dashboard readiness: map review queues and artifact-shape failures to a future UI.
3. Example library: add policy/process or release-planning examples if demand appears.
4. Dashboard prototype: build a read/write web UI over the same filesystem workspace.
5. Distribution polish: add release verification docs and upgrade guidance.

## Recommendation

For `0.14.0`, prioritize a short recorded walkthrough plus dashboard-readiness notes for review queues and artifact-shape failures. After that, consider the first dashboard prototype if the review vocabulary still feels stable.
