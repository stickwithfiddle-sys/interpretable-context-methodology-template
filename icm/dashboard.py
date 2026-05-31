"""Read-only local dashboard for ICM workspaces."""

from __future__ import annotations

import html
import json
import shlex
import subprocess
import sys
import webbrowser
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable
from urllib.parse import parse_qs, urlparse


CliJsonRunner = Callable[[list[str], Path], dict]


@dataclass(frozen=True)
class DashboardBinding:
    url: str
    server: ThreadingHTTPServer


def path_text(path: Path) -> str:
    return path.as_posix()


def command_text(args: list[str]) -> str:
    return shlex.join(["icm", *args])


def run_cli_json(args: list[str], workspace_root: Path) -> dict:
    """Run the installed ICM CLI and parse its JSON response."""
    command = [sys.executable, "-m", "icm", *args]
    try:
        process = subprocess.run(
            command,
            cwd=workspace_root if workspace_root.is_dir() else None,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return {
            "command": command_text(args),
            "passed": False,
            "error": str(error),
            "exit_code": 1,
        }
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError:
        payload = {
            "command": command_text(args),
            "passed": False,
            "error": "CLI command did not return valid JSON.",
            "stdout": process.stdout.strip(),
        }
    payload.setdefault("command", command_text(args))
    payload["exit_code"] = process.returncode
    if process.stderr.strip():
        payload["stderr"] = process.stderr.strip()
    return payload


def finding_count(findings: list[dict], level: str) -> int:
    return sum(1 for finding in findings if finding.get("level") == level)


def doctor_findings(doctor: dict) -> list[dict]:
    structure_findings = doctor.get("structure", {}).get("findings", [])
    content_findings = doctor.get("content", {}).get("findings", [])
    return [*structure_findings, *content_findings]


def collect_dashboard_payload(workspace: Path, cli_runner: CliJsonRunner = run_cli_json) -> dict:
    """Build the dashboard model by consuming the CLI JSON contract."""
    workspace_root = workspace.expanduser().resolve()
    status = cli_runner(["status", path_text(workspace_root), "--json"], workspace_root)
    doctor = cli_runner(["doctor", path_text(workspace_root), "--json"], workspace_root)

    reviews: list[dict] = []
    for stage in status.get("stages", []):
        if not stage.get("existing_outputs"):
            continue
        stage_path = str(stage.get("path", ""))
        if not stage_path:
            continue
        reviews.append(
            cli_runner(
                ["review", stage_path, "--workspace", path_text(workspace_root), "--json"],
                workspace_root,
            )
        )

    review_fails = sum(int(review.get("summary", {}).get("fail", 0)) for review in reviews)
    review_warnings = sum(int(review.get("summary", {}).get("warn", 0)) for review in reviews)
    all_doctor_findings = doctor_findings(doctor)

    return {
        "command": command_text(["dashboard", path_text(workspace_root)]),
        "workspace": path_text(workspace_root),
        "read_only": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "doctor": doctor,
        "reviews": reviews,
        "summary": {
            "stages": len(status.get("stages", [])),
            "accepted_stages": sum(1 for stage in status.get("stages", []) if stage.get("state") == "accepted"),
            "ready_for_review": sum(1 for stage in status.get("stages", []) if stage.get("state") == "ready_for_review"),
            "pending_acceptance": sum(len(stage.get("pending_acceptance_outputs", [])) for stage in status.get("stages", [])),
            "review_failures": review_fails,
            "review_warnings": review_warnings,
            "doctor_failures": finding_count(all_doctor_findings, "FAIL"),
            "doctor_warnings": finding_count(all_doctor_findings, "WARN"),
        },
    }


def resolve_workspace_file(workspace_root: Path, raw_path: str) -> Path:
    if not raw_path:
        raise FileNotFoundError("Missing source path.")
    relative_path = Path(raw_path)
    if relative_path.is_absolute():
        raise ValueError("Source path must be workspace-relative.")
    resolved = (workspace_root / relative_path).resolve()
    try:
        resolved.relative_to(workspace_root)
    except ValueError as error:
        raise ValueError("Source path must stay inside the workspace.") from error
    if not resolved.is_file():
        raise FileNotFoundError(f"Source file not found: {raw_path}")
    return resolved


DASHBOARD_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ICM Dashboard</title>
    <style>
      :root {
        color-scheme: light;
        --bg: #f4f7f8;
        --surface: #ffffff;
        --surface-soft: #eef5f3;
        --text: #172024;
        --muted: #5f6c72;
        --line: #d6e0e3;
        --teal: #00756b;
        --blue: #2459a6;
        --amber: #9a6700;
        --red: #b42318;
        --green-soft: #e5f5ef;
        --amber-soft: #fff4d8;
        --red-soft: #fde8e5;
        --blue-soft: #e8f0ff;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        background: var(--bg);
        color: var(--text);
      }
      a {
        color: var(--blue);
        text-decoration-thickness: 1px;
        text-underline-offset: 3px;
      }
      .shell {
        width: min(1280px, calc(100% - 32px));
        margin: 0 auto;
        padding: 24px 0 40px;
      }
      .topbar {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        gap: 16px;
        align-items: end;
        padding: 18px 0 24px;
      }
      h1, h2, h3, p { margin: 0; }
      h1 {
        font-size: 32px;
        line-height: 1.08;
        letter-spacing: 0;
      }
      h2 {
        font-size: 18px;
        line-height: 1.25;
        letter-spacing: 0;
      }
      h3 {
        font-size: 15px;
        line-height: 1.25;
        letter-spacing: 0;
      }
      .eyebrow {
        color: var(--teal);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0;
        text-transform: uppercase;
        margin-bottom: 8px;
      }
      .workspace-path {
        color: var(--muted);
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 13px;
        margin-top: 10px;
        overflow-wrap: anywhere;
      }
      .actions {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        justify-content: flex-end;
      }
      button, .badge {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
        color: var(--text);
        min-height: 38px;
        padding: 0 12px;
        font: inherit;
        font-weight: 700;
      }
      button {
        cursor: pointer;
      }
      button:hover {
        border-color: #9fb2b8;
      }
      .badge {
        display: inline-flex;
        align-items: center;
        color: var(--teal);
        background: var(--green-soft);
      }
      .layout {
        display: grid;
        grid-template-columns: minmax(0, 1.35fr) minmax(340px, 0.65fr);
        gap: 18px;
      }
      .panel {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 8px;
      }
      .panel + .panel {
        margin-top: 18px;
      }
      .panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        border-bottom: 1px solid var(--line);
        padding: 16px;
      }
      .panel-body {
        padding: 16px;
      }
      .metrics {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin-bottom: 18px;
      }
      .metric {
        min-height: 96px;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
        padding: 14px;
      }
      .metric-label {
        color: var(--muted);
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0;
      }
      .metric-value {
        display: block;
        margin-top: 12px;
        font-size: 28px;
        line-height: 1;
        font-weight: 850;
      }
      .metric-note {
        color: var(--muted);
        display: block;
        margin-top: 8px;
        font-size: 13px;
        line-height: 1.35;
        overflow-wrap: anywhere;
      }
      .stage-list, .review-list, .finding-list, .command-list {
        display: grid;
        gap: 10px;
      }
      .stage-row {
        display: grid;
        grid-template-columns: minmax(170px, 0.7fr) minmax(0, 1fr) minmax(140px, 0.4fr);
        gap: 12px;
        align-items: center;
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 12px;
        background: #fbfdfd;
      }
      .stage-name {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-weight: 800;
        overflow-wrap: anywhere;
      }
      .stage-purpose, .finding-message, .review-meta {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.45;
        overflow-wrap: anywhere;
      }
      .pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 28px;
        border-radius: 999px;
        padding: 3px 10px;
        font-size: 12px;
        font-weight: 850;
        line-height: 1;
        white-space: nowrap;
      }
      .pill.accepted, .pill.pass { background: var(--green-soft); color: var(--teal); }
      .pill.ready_for_review { background: var(--blue-soft); color: var(--blue); }
      .pill.needs_input, .pill.waiting, .pill.warn, .pill.partial { background: var(--amber-soft); color: var(--amber); }
      .pill.missing_contract, .pill.fail { background: var(--red-soft); color: var(--red); }
      .pill.info { background: var(--blue-soft); color: var(--blue); }
      .source-links {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: flex-end;
      }
      .source-links a, .command-chip {
        display: inline-flex;
        align-items: center;
        min-height: 30px;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
        padding: 4px 8px;
        color: var(--blue);
        font-size: 12px;
        font-weight: 800;
        overflow-wrap: anywhere;
      }
      .review-item, .finding-item {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: #fbfdfd;
        padding: 12px;
      }
      .review-top, .finding-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 8px;
      }
      .summary-line {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }
      .empty {
        color: var(--muted);
        border: 1px dashed var(--line);
        border-radius: 8px;
        padding: 18px;
      }
      .command-chip {
        justify-content: flex-start;
        width: 100%;
        color: var(--text);
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-weight: 650;
      }
      .status-line {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.4;
        overflow-wrap: anywhere;
      }
      @media (max-width: 900px) {
        .layout, .topbar, .stage-row {
          grid-template-columns: 1fr;
        }
        .actions, .source-links {
          justify-content: flex-start;
        }
        .metrics {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }
      }
      @media (max-width: 560px) {
        .shell {
          width: min(100% - 20px, 1280px);
          padding-top: 12px;
        }
        h1 { font-size: 26px; }
        .metrics {
          grid-template-columns: 1fr;
        }
      }
    </style>
  </head>
  <body>
    <main class="shell">
      <header class="topbar">
        <div>
          <p class="eyebrow">Local workspace</p>
          <h1>ICM Dashboard</h1>
          <p class="workspace-path" id="workspace-path">Loading...</p>
        </div>
        <div class="actions">
          <span class="badge">Read-only</span>
          <button id="refresh" type="button">Refresh</button>
        </div>
      </header>

      <section class="metrics" aria-label="Workspace summary">
        <div class="metric">
          <span class="metric-label">Stages</span>
          <span class="metric-value" id="metric-stages">-</span>
          <span class="metric-note" id="metric-ready">-</span>
        </div>
        <div class="metric">
          <span class="metric-label">Review</span>
          <span class="metric-value" id="metric-review">-</span>
          <span class="metric-note" id="metric-review-note">-</span>
        </div>
        <div class="metric">
          <span class="metric-label">Doctor</span>
          <span class="metric-value" id="metric-doctor">-</span>
          <span class="metric-note" id="metric-doctor-note">-</span>
        </div>
        <div class="metric">
          <span class="metric-label">Next</span>
          <span class="metric-value" id="metric-next">-</span>
          <span class="metric-note" id="metric-next-note">-</span>
        </div>
      </section>

      <div class="layout">
        <section>
          <section class="panel">
            <div class="panel-header">
              <h2>Stages</h2>
              <span class="status-line" id="generated-at"></span>
            </div>
            <div class="panel-body">
              <div class="stage-list" id="stage-list"></div>
            </div>
          </section>

          <section class="panel">
            <div class="panel-header">
              <h2>Review Queue</h2>
              <span class="status-line" id="review-command"></span>
            </div>
            <div class="panel-body">
              <div class="review-list" id="review-list"></div>
            </div>
          </section>
        </section>

        <aside>
          <section class="panel">
            <div class="panel-header">
              <h2>Doctor</h2>
              <span class="status-line" id="doctor-state"></span>
            </div>
            <div class="panel-body">
              <div class="finding-list" id="doctor-list"></div>
            </div>
          </section>

          <section class="panel">
            <div class="panel-header">
              <h2>CLI Source</h2>
            </div>
            <div class="panel-body">
              <div class="command-list" id="command-list"></div>
            </div>
          </section>
        </aside>
      </div>
    </main>

    <script>
      const byId = (id) => document.getElementById(id);
      const escapeHtml = (value) => String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
      const sourceLink = (path, label) => {
        if (!path) return "";
        return `<a href="/source?path=${encodeURIComponent(path)}">${escapeHtml(label || path)}</a>`;
      };
      const pill = (label, cls) => `<span class="pill ${escapeHtml(cls || "info").toLowerCase()}">${escapeHtml(label)}</span>`;
      const stateLabel = (state) => String(state || "unknown").replaceAll("_", " ");

      function renderMetrics(payload) {
        const summary = payload.summary || {};
        const status = payload.status || {};
        const nextAction = status.next_action || {};
        byId("workspace-path").textContent = payload.workspace || "";
        byId("generated-at").textContent = payload.generated_at ? `Updated ${new Date(payload.generated_at).toLocaleString()}` : "";
        byId("metric-stages").textContent = summary.stages ?? 0;
        byId("metric-ready").textContent = `${summary.accepted_stages ?? 0} accepted, ${summary.ready_for_review ?? 0} machine-passing`;
        byId("metric-review").textContent = summary.review_failures ?? 0;
        byId("metric-review-note").textContent = `${summary.review_warnings ?? 0} warnings`;
        byId("metric-doctor").textContent = summary.doctor_failures ?? 0;
        byId("metric-doctor-note").textContent = `${summary.doctor_warnings ?? 0} warnings`;
        byId("metric-next").textContent = stateLabel(nextAction.type || "ready");
        byId("metric-next-note").textContent = nextAction.message || "Review the workspace state.";
      }

      function renderStages(stages) {
        if (!stages || !stages.length) {
          byId("stage-list").innerHTML = `<div class="empty">No numbered stages found.</div>`;
          return;
        }
        byId("stage-list").innerHTML = stages.map((stage) => {
          const outputLinks = (stage.existing_outputs || []).map((name) =>
            sourceLink(`${stage.path}/output/${name}`, name)
          ).join("");
          const missing = (stage.missing_outputs || []).length
            ? `<div class="stage-purpose">Missing: ${escapeHtml((stage.missing_outputs || []).join(", "))}</div>`
            : "";
          return `
            <article class="stage-row">
              <div>
                <div class="stage-name">${escapeHtml(stage.name)}</div>
                ${pill(stateLabel(stage.state), stage.state)}
              </div>
              <div>
                <p class="stage-purpose">${escapeHtml(stage.purpose || stage.note || "")}</p>
                ${missing}
              </div>
              <div class="source-links">
                ${sourceLink(`${stage.path}/CONTEXT.md`, "CONTEXT.md")}
                ${outputLinks}
              </div>
            </article>
          `;
        }).join("");
      }

      function renderReviewFindings(findings) {
        const important = (findings || []).filter((finding) => finding.level !== "PASS");
        if (!important.length) return `<p class="review-meta">Machine checks passed.</p>`;
        return important.slice(0, 6).map((finding) => `
          <div class="finding-message">
            ${pill(finding.level, finding.level)}
            ${escapeHtml(finding.message)}
            ${finding.suggested_fix ? `<br>Fix: ${escapeHtml(finding.suggested_fix)}` : ""}
          </div>
        `).join("");
      }

      function renderReviews(reviews) {
        byId("review-command").textContent = reviews && reviews.length ? `${reviews.length} reviewed` : "";
        if (!reviews || !reviews.length) {
          byId("review-list").innerHTML = `<div class="empty">No completed outputs are ready for review.</div>`;
          return;
        }
        byId("review-list").innerHTML = reviews.map((review) => {
          const summary = review.summary || {};
          return `
            <article class="review-item">
              <div class="review-top">
                <h3>${escapeHtml(review.stage || review.target || "Review")}</h3>
                ${pill(review.acceptance && review.acceptance.accepted ? "accepted" : (review.passed ? "machine passing" : "needs repair"), review.acceptance && review.acceptance.accepted ? "accepted" : (review.passed ? "ready_for_review" : "fail"))}
              </div>
              <div class="summary-line">
                ${pill(`${summary.fail ?? 0} fail`, "fail")}
                ${pill(`${summary.warn ?? 0} warn`, "warn")}
                ${pill(`${summary.pass ?? 0} pass`, "pass")}
              </div>
              <p class="review-meta">${escapeHtml(review.command || "")}</p>
              <p class="review-meta">Human acceptance: ${escapeHtml(((review.acceptance || {}).outputs || []).filter((output) => output.accepted).length)} / ${escapeHtml(((review.acceptance || {}).outputs || []).length)} outputs accepted</p>
              <div class="source-links">
                ${sourceLink(`${review.stage_path}/CONTEXT.md`, "CONTEXT.md")}
                ${review.output_path ? sourceLink(review.output_path, review.output_path.split("/").pop()) : ""}
              </div>
              ${renderReviewFindings(review.findings)}
            </article>
          `;
        }).join("");
      }

      function renderDoctor(doctor) {
        const findings = [
          ...(((doctor || {}).structure || {}).findings || []),
          ...(((doctor || {}).content || {}).findings || [])
        ].filter((finding) => finding.level !== "PASS");
        byId("doctor-state").textContent = doctor && doctor.passed ? "passing" : "needs attention";
        if (!findings.length) {
          byId("doctor-list").innerHTML = `<div class="empty">No doctor failures or warnings.</div>`;
          return;
        }
        byId("doctor-list").innerHTML = findings.map((finding) => `
          <article class="finding-item">
            <div class="finding-top">
              ${pill(finding.level, finding.level)}
            </div>
            <p class="finding-message">${escapeHtml(finding.message)}</p>
            ${finding.suggested_fix ? `<p class="finding-message">Fix: ${escapeHtml(finding.suggested_fix)}</p>` : ""}
          </article>
        `).join("");
      }

      function renderCommands(payload) {
        const commands = [
          (payload.status || {}).command,
          (payload.doctor || {}).command,
          ...(payload.reviews || []).map((review) => review.command)
        ].filter(Boolean);
        byId("command-list").innerHTML = commands.map((command) =>
          `<code class="command-chip">${escapeHtml(command)}</code>`
        ).join("");
      }

      async function loadDashboard() {
        byId("refresh").disabled = true;
        try {
          const response = await fetch("/api/workspace", { cache: "no-store" });
          const payload = await response.json();
          renderMetrics(payload);
          renderStages((payload.status || {}).stages || []);
          renderReviews(payload.reviews || []);
          renderDoctor(payload.doctor || {});
          renderCommands(payload);
        } catch (error) {
          byId("workspace-path").textContent = String(error);
        } finally {
          byId("refresh").disabled = false;
        }
      }

      byId("refresh").addEventListener("click", loadDashboard);
      loadDashboard();
    </script>
  </body>
</html>
"""


def render_dashboard_html() -> str:
    return DASHBOARD_HTML


def render_source_html(workspace_root: Path, source_path: Path) -> str:
    relative = source_path.relative_to(workspace_root).as_posix()
    text = source_path.read_text(encoding="utf-8", errors="replace")
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(relative)} | ICM Dashboard</title>
    <style>
      :root {{
        --bg: #f4f7f8;
        --surface: #ffffff;
        --text: #172024;
        --muted: #5f6c72;
        --line: #d6e0e3;
        --blue: #2459a6;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      * {{ box-sizing: border-box; }}
      body {{ margin: 0; background: var(--bg); color: var(--text); }}
      main {{ width: min(1080px, calc(100% - 32px)); margin: 0 auto; padding: 24px 0 40px; }}
      a {{ color: var(--blue); text-underline-offset: 3px; }}
      h1 {{ font-size: 24px; line-height: 1.2; letter-spacing: 0; overflow-wrap: anywhere; }}
      .path {{ color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; overflow-wrap: anywhere; }}
      pre {{
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
        margin: 20px 0 0;
        padding: 18px;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 14px;
        line-height: 1.5;
      }}
    </style>
  </head>
  <body>
    <main>
      <p><a href="/">Back to dashboard</a></p>
      <h1>{html.escape(source_path.name)}</h1>
      <p class="path">{html.escape(relative)}</p>
      <pre>{html.escape(text)}</pre>
    </main>
  </body>
</html>
"""


class DashboardHTTPServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], workspace_root: Path, cli_runner: CliJsonRunner = run_cli_json) -> None:
        self.workspace_root = workspace_root.expanduser().resolve()
        self.cli_runner = cli_runner
        super().__init__(server_address, DashboardRequestHandler)


class DashboardRequestHandler(BaseHTTPRequestHandler):
    server: DashboardHTTPServer

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002 - inherited API name.
        return

    def send_body(self, body: str | bytes, content_type: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        if isinstance(body, str):
            body_bytes = body.encode("utf-8")
        else:
            body_bytes = body
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)

    def send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_body(json.dumps(payload, indent=2, sort_keys=True), "application/json; charset=utf-8", status)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/index.html"}:
            self.send_body(render_dashboard_html(), "text/html; charset=utf-8")
            return

        if parsed.path == "/api/workspace":
            payload = collect_dashboard_payload(self.server.workspace_root, self.server.cli_runner)
            self.send_json(payload)
            return

        if parsed.path == "/api/source":
            self.handle_source_api(parsed.query)
            return

        if parsed.path == "/source":
            self.handle_source_page(parsed.query)
            return

        self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def source_from_query(self, query: str) -> Path:
        params = parse_qs(query)
        raw_path = params.get("path", [""])[0]
        return resolve_workspace_file(self.server.workspace_root, raw_path)

    def handle_source_api(self, query: str) -> None:
        try:
            source_path = self.source_from_query(query)
        except (FileNotFoundError, ValueError) as error:
            self.send_json({"error": str(error)}, HTTPStatus.NOT_FOUND)
            return
        self.send_json(
            {
                "path": source_path.relative_to(self.server.workspace_root).as_posix(),
                "text": source_path.read_text(encoding="utf-8", errors="replace"),
            }
        )

    def handle_source_page(self, query: str) -> None:
        try:
            source_path = self.source_from_query(query)
        except (FileNotFoundError, ValueError) as error:
            back = '<p><a href="/">Back to dashboard</a></p>'
            self.send_body(f"<!doctype html><html><body>{back}<p>{html.escape(str(error))}</p></body></html>", "text/html; charset=utf-8", HTTPStatus.NOT_FOUND)
            return
        self.send_body(render_source_html(self.server.workspace_root, source_path), "text/html; charset=utf-8")


def bind_dashboard_server(
    workspace_root: Path,
    host: str,
    preferred_port: int,
    allow_port_fallback: bool,
    cli_runner: CliJsonRunner = run_cli_json,
) -> DashboardBinding:
    ports = [preferred_port]
    if allow_port_fallback and preferred_port != 0:
        ports.extend(range(preferred_port + 1, preferred_port + 11))

    last_error: OSError | None = None
    for port in ports:
        try:
            server = DashboardHTTPServer((host, port), workspace_root, cli_runner)
        except OSError as error:
            last_error = error
            continue
        actual_host, actual_port = server.server_address[:2]
        if actual_host in {"", "0.0.0.0"}:
            actual_host = host
        url_host = f"[{actual_host}]" if ":" in str(actual_host) else str(actual_host)
        return DashboardBinding(url=f"http://{url_host}:{actual_port}/", server=server)

    if last_error is None:
        raise OSError("Could not bind dashboard server.")
    raise last_error


def serve_dashboard(
    workspace: Path,
    host: str = "127.0.0.1",
    port: int | None = None,
    open_browser: bool = True,
    cli_runner: CliJsonRunner = run_cli_json,
) -> None:
    workspace_root = workspace.expanduser().resolve()
    preferred_port = 8765 if port is None else port
    binding = bind_dashboard_server(
        workspace_root=workspace_root,
        host=host,
        preferred_port=preferred_port,
        allow_port_fallback=port is None,
        cli_runner=cli_runner,
    )

    print(f"ICM dashboard: {binding.url}")
    print(f"Workspace: {workspace_root}")
    print("Read-only. Press Ctrl+C to stop.")
    if open_browser:
        webbrowser.open(binding.url)

    try:
        binding.server.serve_forever()
    finally:
        binding.server.server_close()
