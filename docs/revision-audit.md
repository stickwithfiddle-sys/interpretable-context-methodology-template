# Revision Audit

Last updated: 2026-05-31

Current release: `0.16.0`

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
- A first-10-minutes beginner walkthrough linked from the docs homepage.
- A dashboard-readiness spec for review queues, artifact-shape failures, doctor findings, and human acceptance.
- Machine-readable `--json` output for `icm status`, `icm review`, and `icm doctor`.
- GitHub Actions workflows updated to Node 24-native action versions without the temporary force env.
- Read-only local dashboard prototype through `icm dashboard`, backed by the same CLI JSON contract.

## Roadmap Position

The current `Now` work is mostly in place: first-run clarity, self-contained generated workspaces, PyPI install reliability, release hygiene, safe existing-project adoption, visual docs, deterministic review rubrics, source traceability, table/path checks, source-inventory/calendar/decision-log checks, common artifact starters, doctor-surfaced rubric failures, release-ready docs, workflow-specific rubric guidance, dashboard-readiness notes, machine-readable CLI output, a read-only local dashboard, and four completed examples are all covered.

The highest-value `Next` work is:

- A human acceptance marker for reviewed handoffs without hiding markdown.
- More workflow-specific examples for policy/process and lightweight release planning if demand appears.

## Beginner UX Assessment

The product is beginner-friendly for a technical user who can run Python commands. A new user can install the CLI, create or initialize a workspace, add common artifact starters, follow the first-10-minutes guide, fill the first brief, run doctor checks, validate structure, inspect completed examples, choose a rubric pattern by workflow type, expose the same state as JSON for local tooling, and open a read-only dashboard for stage and review status.

It is closer to world-class beginner UX, but not there yet. The main gaps are no human acceptance marker in the workspace model, no read/write dashboard flow, and no animated or recorded demo embedded directly in the docs site.

## Direction Options

1. Human acceptance marker: define how reviewed handoffs are accepted without hiding markdown.
2. Read/write dashboard path: decide which edits can safely happen in the browser.
3. Demo polish: add an animated or recorded walkthrough embedded in the docs site.
4. Example library: add policy/process or release-planning examples if demand appears.
5. Distribution polish: keep PyPI install, upgrade, and verification docs current.

## Recommendation

For `0.17.0`, prioritize a human acceptance marker for reviewed handoffs. The dashboard should show acceptance clearly, but the source of truth should remain a plain workspace file.
