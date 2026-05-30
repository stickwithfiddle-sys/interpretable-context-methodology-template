# Roadmap

This roadmap keeps product work visible without turning the README into a backlog.

## Now

- Make ICM understandable in the first five minutes.
- Keep generated workspaces self-contained and inspectable.
- Keep the installable CLI reliable outside the source checkout.

## Next

- Add richer `icm doctor` checks for empty required sections and broken handoffs.
- Add `icm init` for converting an existing folder into an ICM workspace.
- Add richer `icm review` checks for artifact-specific rubrics and source traceability.
- Add pytest coverage for the CLI and workspace helpers.
- Add examples for research synthesis, project planning, and documentation pipelines.
- Add a docs site once the CLI vocabulary stabilizes.

## Later

- Add a lightweight dashboard that reads and writes the same filesystem workspace.
- Add optional Git integration for showing output diffs at review gates.
- Add deterministic validators for common artifact types such as calendars, source inventories, and decision logs.
- Publish to PyPI once the CLI interface and template format stabilize.
