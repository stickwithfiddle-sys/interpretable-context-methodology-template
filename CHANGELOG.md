# Changelog

All notable changes to this project are documented here.

This project follows [Semantic Versioning](https://semver.org/) while it is pre-1.0:

- Minor versions may add or reshape product features.
- Patch versions are reserved for fixes and small documentation corrections.
- Breaking changes should be called out clearly, even before 1.0.

## [Unreleased]

Use this section while preparing the next version.

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

[Unreleased]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.9.0...HEAD
[0.9.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/releases/tag/v0.1.0
