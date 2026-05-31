# Scaffold Rules

## Names

- Stage folders use `NN_slug` format.
- Slugs should describe the transformation, not the agent persona.
- Output file names should describe the artifact consumed downstream.

## Required Stage Contents

- `CONTEXT.md`
- `references/`
- `output/`

## Required Stage Contract Sections

- Purpose
- Inputs
- Process
- Outputs
- Review Gate
- Verify

## Keep It Portable

- Prefer markdown, JSON, CSV, and plain text.
- Add scripts only for deterministic checks or repeatable mechanical transformations.
- Keep vendor-specific instructions in optional reference files.