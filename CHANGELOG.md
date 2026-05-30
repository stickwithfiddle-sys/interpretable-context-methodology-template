# Changelog

All notable changes to this project are documented here.

This project follows [Semantic Versioning](https://semver.org/) while it is pre-1.0:

- Minor versions may add or reshape product features.
- Patch versions are reserved for fixes and small documentation corrections.
- Breaking changes should be called out clearly, even before 1.0.

## [Unreleased]

Use this section while preparing the next version.

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

[Unreleased]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/stickwithfiddle-sys/interpretable-context-methodology-template/releases/tag/v0.1.0
