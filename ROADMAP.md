# Roadmap

This roadmap keeps product work visible without turning the README into a backlog.

## Now

- Make ICM understandable in the first five minutes.
- Keep generated workspaces self-contained and inspectable.
- Keep the installable CLI reliable outside the source checkout.
- Keep security, ownership, CI, and pytest coverage visible before release.
- Support both clean-start and existing-project adoption with `icm new` and `icm init`.
- Keep the PyPI install path healthy for beginners.
- Keep the GitHub Pages docs site useful as the visual first stop.
- Support artifact-specific `icm review` rubrics.
- Support source-traceability checks in `icm review` rubrics.
- Support deterministic table-column and link/path-count checks in `icm review` rubrics.
- Support source-inventory, calendar, and decision-log artifact-shape checks in `icm review` rubrics.
- Support optional common artifact starter files through `icm new/init --with-common-artifacts`.
- Surface review-rubric failures in `icm doctor` for existing declared outputs.
- Keep package metadata, build checks, and Trusted Publishing workflow ready for PyPI.
- Maintain at least three completed example workspaces, including content planning, research briefs, and documentation refreshes.
- Keep a copy-paste demo path visible from the docs homepage.
- Keep a first-10-minutes walkthrough visible from the docs homepage.
- Keep beginner-facing PyPI upgrade and install verification docs available.
- Keep a release-ready workspace checklist available for validation, review, changelog, and upgrade checks.
- Maintain a completed project-planning example with source-inventory, calendar, and decision-log checks.
- Keep workflow-specific rubric guidance available for beginners.
- Keep dashboard-readiness criteria visible before building the dashboard.
- Expose machine-readable `--json` output for `icm status`, `icm review`, and `icm doctor`.
- Provide a read-only local dashboard prototype through `icm dashboard`.
- Keep the plain-file human acceptance marker in `shared/acceptance-log.md`.
- Show accepted vs machine-passing handoffs in CLI JSON and the dashboard.
- Provide dashboard affordances for copying review and acceptance commands.

## Next

- Add workflow-specific examples for policy/process and lightweight release planning if demand appears.
- Add clearer dashboard source-file previews for review failures and acceptance-log entries.

## Later

- Add a lightweight read/write dashboard that reads and writes the same filesystem workspace.
- Add optional Git integration for showing output diffs at review gates.
- Add richer release attestations and install verification docs after PyPI is live.
