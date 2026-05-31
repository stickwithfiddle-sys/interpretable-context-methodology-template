# Changelog

All notable changes to this project are documented here.

This project follows [Semantic Versioning](https://semver.org/) while it is pre-1.0:

- Minor versions may add or reshape product features.
- Patch versions are reserved for fixes and small documentation corrections.
- Breaking changes should be called out clearly, even before 1.0.

## [Unreleased]

Use this section while preparing the next version.

## [0.18.0] - 2026-05-31

### Added

- Added copyable review and acceptance command affordances to the read-only dashboard review queue.
- Added copyable command rows for the dashboard CLI source panel.
- Added dashboard payload command fields for human review, human acceptance, and JSON integration commands.

### Changed

- Dashboard docs, product direction, roadmap, revision audit, docs homepage, and dashboard tests now reflect the command-copy workflow.

## [0.17.0] - 2026-05-31

### Added

- Added `shared/acceptance-log.md` as the plain-file source of truth for human-reviewed handoff acceptance.
- Added `icm accept` with text and JSON output for recording accepted stage outputs without hidden state.
- Added an end-to-end playtest guide with a complete project idea so beginners can experience the full workflow.

### Changed

- `icm status`, `icm review --json`, and the dashboard now distinguish machine-passing outputs from human-accepted handoffs.
- Generated workspace docs, README, JSON contract docs, dashboard docs, roadmap, product direction, and revision audit now include the acceptance workflow.

## [0.16.0] - 2026-05-31

### Added

- Added `icm dashboard`, a read-only local dashboard that renders workspace status, review findings, doctor findings, source links, and CLI source commands.
- Added dashboard payload and HTTP smoke tests.
- Added dashboard prototype documentation and a dashboard screenshot asset for the docs homepage.

### Changed

- README, docs homepage, dashboard readiness notes, product direction, roadmap, revision audit, release docs, and contribution checks now include the dashboard prototype.

## [0.15.0] - 2026-05-31

### Added

- Added `--json` output for `icm status`, `icm review`, and `icm doctor` for dashboard and editor integrations.
- Added JSON output documentation and tests for the machine-readable command contract.
- Added CI smoke coverage for JSON status, review, and doctor output.

### Changed

- Updated GitHub Actions to Node 24-native action versions and removed the temporary Node 24 force environment.
- README, docs site, dashboard readiness notes, roadmap, product direction, and revision audit now reflect the JSON data contract.

## [0.14.0] - 2026-05-31

### Added

- Added a first-10-minutes beginner walkthrough from install to first review loop.
- Added a dashboard-readiness spec for review queues, artifact-shape failures, doctor findings, and human acceptance.
- Added a visual walkthrough asset to the GitHub Pages docs homepage.

### Changed

- README, docs site, demo guide, roadmap, product direction, revision audit, and release metadata now reflect the walkthrough and dashboard-readiness release.

## [0.13.0] - 2026-05-30

### Added

- Added a completed project-planning example workspace with source inventory, project calendar, and decision-log artifact-shape checks.
- Added workflow-specific rubric guidance for choosing validators by use case.
- Added test and CI coverage for the completed project-planning example.

### Changed

- README, docs site, demo guide, roadmap, product direction, revision audit, and release checklists now reflect the project-planning example and workflow rubric guide.
- GitHub Actions workflows now opt into Node 24 for JavaScript actions to address the Node 20 deprecation warning.

## [0.12.0] - 2026-05-30

### Added

- Added `--with-common-artifacts` to `icm new` and `icm init` for starter source inventory, release calendar, and decision-log files.
- Added release-ready workspace documentation that ties together CLI version checks, validation, doctor, review, changelog updates, and PyPI upgrade verification.
- Added tests for common artifact scaffolding and doctor-surfaced artifact-shape failures.

### Changed

- `icm doctor` now reports review-rubric failures for existing declared outputs, including invalid source-inventory, calendar, and decision-log shapes.
- The generated shared decision log now uses Date, Decision, Status, and Rationale columns so it matches the deterministic decision-log validator.
- README, docs site, install docs, demo docs, review-rubric docs, roadmap, product direction, and revision audit now reflect the v0.12.0 adoption improvements.

## [0.11.0] - 2026-05-30

### Added

- Added `Required Artifact Shapes` rubric checks for source inventories, calendars, and decision logs.
- Added artifact-shape fixture outputs and rubrics to the completed documentation-refresh example.
- Added beginner-facing PyPI upgrade and install verification documentation.

### Changed

- Review-rubric docs now explain common artifact-shape validators and examples.
- Roadmap, product direction, revision audit, README, docs site, and release checklists now reflect the v0.11.0 validator work.

### Fixed

- Fixed the GitHub Pages homepage link for the demo walkthrough so it opens the generated HTML page.

## [0.10.0] - 2026-05-30

### Added

- Added deterministic `icm review` rubric checks for required markdown table columns.
- Added deterministic `icm review` rubric checks for minimum link/path reference counts.
- Added a completed documentation-refresh example workspace that demonstrates table-column and path-count checks.
- Added a copy-paste demo walkthrough and a visual docs homepage demo section.

### Changed

- Beginner install docs continue to lead with the live PyPI package.
- Roadmap, product direction, revision audit, and release checklists now reflect the v0.10.0 demo and validator work.

## [0.9.0] - 2026-05-30

### Added

- Added rubric-driven source-traceability checks to `icm review` through `Required Sources` and `Required Source References` sections.
- Added `Source Traceability` sections and required-source checks to the completed content-plan and research-brief examples.
- Added a starter discovery report rubric to generated workspaces.
- Added source-traceability documentation.
- Added PyPI readiness documentation and a manual Trusted Publishing workflow for TestPyPI or PyPI.
- Added `tools/check_release_readiness.py` for version, metadata, docs, and publishing workflow checks.

### Changed

- CI now builds source and wheel distributions with `python -m build` and checks package rendering with `twine check`.
- Project metadata now includes documentation, changelog, and issue tracker URLs for package indexes.
- Package metadata now uses an SPDX license expression and explicit license files.

## [0.8.0] - 2026-05-30

### Added

- Added artifact-specific `icm review` rubrics from stage `references/` files.
- Added deterministic rubric checks for required sections, required terms, and forbidden terms.
- Added a completed research-brief example workspace with a discovery report rubric.
- Added review-rubric documentation.

### Fixed

- Fixed the GitHub Pages workspace-flow diagram so the red stage-contract label stays inside its box.

## [0.7.0] - 2026-05-30

### Added

- Added `icm init` to initialize existing project folders without overwriting existing files.
- Added richer `icm doctor` content checks for empty stage sections, missing declared inputs, undeclared output files, empty outputs, and broken handoffs.
- Added a GitHub Pages docs homepage with visual CLI screenshots and a workspace flow diagram.
- Added `tools/check_docs_site.py` and CI coverage for local docs site references.
- Added dashboard direction notes with readiness criteria and MVP boundaries.

### Changed

- Updated beginner docs to show both clean-start and existing-project adoption flows.
- Updated the roadmap and revision audit now that `icm init`, richer `doctor`, and the visual docs site are in place.

## [0.6.0] - 2026-05-30

### Added

- Added a security policy and repository code ownership.
- Added pytest coverage for CLI commands, workspace creation, packaged resources, status detection, and review checks.
- Added a revision audit document summarizing product progress, UX status, roadmap position, and next direction options.

### Changed

- CI now installs development dependencies and runs the pytest suite before smoke tests.
- Beginner install docs now lead with installing the versioned CLI from GitHub.

## [0.5.0] - 2026-05-30

### Added

- Embedded the ICM workspace template and fallback validator inside the Python package.
- Added `tools/check_packaged_assets.py` to keep source and package-embedded assets synchronized.
- Added CI wheel-build and installed-package smoke tests that run outside the source checkout.
- Added install documentation for GitHub, virtualenv, and local development flows.

### Changed

- `icm new` now works from an installed wheel, not only from an editable source checkout.

## [0.4.0] - 2026-05-30

### Added

- Added `icm review` for deterministic stage-output review against the stage contract.
- Review checks now inspect required contract headings, declared inputs, declared outputs, output content, review gate text, verify text, undeclared extra outputs, and intake brief readiness.
- Added review smoke checks to docs, CI, and contribution/release checklists.

## [0.3.0] - 2026-05-30

### Added

- Added the `icm` CLI package with `new`, `validate`, `status`, `next`, `explain`, and `doctor` commands.
- Added package metadata and console entry point in `pyproject.toml`.
- Added GitHub contribution, issue, pull request, CI, and release-process files.

### Changed

- Updated beginner docs to teach the CLI path first while preserving legacy script fallbacks.

## [0.2.0] - 2026-05-30

### Added

- Added first-workspace tutorial.
- Added plain-language glossary.
- Added completed content-plan example workspace.
- Added product direction notes inspired by Hermes Agent.

### Changed

- Reworked the README for beginner onboarding.
- Improved generated workspace README and first-run command output.

## [0.1.0] - 2026-05-30

### Added

- Initial reusable ICM workspace template.
- Added workspace generator and validator scripts.
- Added research summary, template design notes, MIT license, and attribution notice.

[Unreleased]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.18.0...HEAD
[0.18.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.17.0...v0.18.0
[0.17.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.16.0...v0.17.0
[0.16.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/releases/tag/v0.1.0
