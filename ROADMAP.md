# Roadmap

This roadmap keeps product work visible without turning the README into a backlog.

## Now

- Make ICM understandable in the first five minutes.
- Keep generated workspaces self-contained and inspectable.
- Build a small CLI that exposes status, next actions, explanation, and diagnostics.

## Next

- Add richer `icm doctor` checks for empty required sections and broken handoffs.
- Add `icm init` for converting an existing folder into an ICM workspace.
- Add `icm review` for checking a stage output against its contract.
- Add examples for research synthesis, project planning, and documentation pipelines.
- Add a docs site once the CLI vocabulary stabilizes.

## Later

- Add a lightweight dashboard that reads and writes the same filesystem workspace.
- Add optional Git integration for showing output diffs at review gates.
- Add deterministic validators for common artifact types such as calendars, source inventories, and decision logs.
- Explore packaging templates inside the Python distribution for non-editable installs.
