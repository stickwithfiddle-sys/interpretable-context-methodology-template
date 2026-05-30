# Security Policy

## Supported Versions

This project is pre-1.0 and currently supports the latest released version only. Please upgrade to the newest release before reporting a bug that may already be fixed.

## Reporting A Vulnerability

Please do not post secrets, exploit details, or sensitive workspace content in a public issue.

Use GitHub's private vulnerability reporting from the repository Security tab when it is available. If private reporting is unavailable, open a public issue with only a high-level description and ask for a maintainer contact path.

Useful reports include:

- The affected ICM version or commit.
- The command or workflow involved.
- The operating system and Python version.
- Whether generated workspaces, package installation, or GitHub configuration are involved.
- A minimal reproduction that does not include private data.

## Secret Handling

ICM workspaces are plain files by design. Do not commit API keys, credentials, private customer data, or sensitive source material unless your own repository policy explicitly allows it.

Generated workspaces include a `.gitignore`, but maintainers and users should still review files before committing.

## Package Publishing

PyPI publishing should use the manual `Publish Python Package` GitHub Actions workflow with PyPI Trusted Publishing. Do not add long-lived PyPI API tokens to repository secrets unless the Trusted Publishing path is unavailable and the release process has been updated.
