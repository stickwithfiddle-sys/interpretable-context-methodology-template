# Project Brief

## Project Name

Documentation Refresh Example

## Desired Outcome

Create a project-specific ICM workspace for refreshing stale product documentation without losing source traceability or reviewer control.

## Starting Material

- Current README and install docs.
- A product roadmap with recent CLI and PyPI changes.
- Existing release notes and user-facing docs.
- A small set of support questions from beginners who are unsure what to read first.

## Audience Or Users

- Primary user: maintainer refreshing docs before a release.
- Secondary user: beginner evaluating whether ICM is worth trying.
- Reviewer: product owner checking that claims match the current release.

## Success Criteria

- Every proposed doc change traces to a source file, release note, or approved decision.
- Stale install commands are found before publication.
- The final update plan separates quick fixes from larger rewrite work.
- A human can review risks before any docs are rewritten.

## Constraints

- Time: one focused documentation pass.
- Budget: no paid services or new docs platform.
- Tools: markdown, local CLI checks, GitHub Pages, and package metadata.
- Privacy or compliance: do not include private support messages verbatim.
- Must avoid: unsourced claims, stale install commands, hidden assumptions, and broad rewrites without review.

## Natural Review Points

- After source inventory.
- After gap analysis.
- Before accepting the update plan.
- Before publishing final docs.

## Open Questions

- Which docs should be treated as source of truth when README and website differ?
- Should screenshots be regenerated for every minor release or only when commands change?
- What minimum source coverage should be required for a documentation update plan?
