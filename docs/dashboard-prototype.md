# Dashboard Prototype

`icm dashboard` starts a local, read-only dashboard for an ICM workspace.

```bash
icm dashboard examples/completed-project-plan
```

By default, the dashboard opens at `http://127.0.0.1:8765/`. If that port is busy, ICM tries nearby ports. Use `--no-open` when you want to start the server without opening a browser:

```bash
icm dashboard examples/completed-project-plan --no-open
```

## What It Shows

- Stage states from `icm status --json`.
- Review queue findings from `icm review ... --json`.
- Workspace health findings from `icm doctor --json`.
- Source links back to workspace markdown files.
- The exact CLI commands that produced the dashboard data.

The prototype does not write workflow state, edit files, mark handoffs accepted, or use a database. Close the browser or stop the server and the workspace still works through the same CLI commands.

## Useful Examples

Run against the completed project-planning example:

```bash
icm dashboard examples/completed-project-plan
```

Run against your current workspace:

```bash
icm dashboard .
```

Choose a port:

```bash
icm dashboard . --port 8780
```

Bind only to localhost unless you have a specific reason to expose it elsewhere:

```bash
icm dashboard . --host 127.0.0.1
```

## Data Contract

The dashboard consumes the same JSON contract documented in [json-output.md](json-output.md):

```bash
icm status . --json
icm review stages/01_discovery --workspace . --json
icm doctor . --json
```

That keeps the browser view honest. If the dashboard and terminal disagree, the terminal JSON is the contract to debug first.
