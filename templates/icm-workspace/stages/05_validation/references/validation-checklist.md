# Validation Checklist

## Structure

- Does the workspace have Layer 0 and Layer 1 files?
- Does every stage have one job?
- Does every stage have `CONTEXT.md`, `references/`, and `output/`?
- Are stage names ordered and readable?

## Context Scoping

- Does each stage list exact Layer 3 inputs?
- Does each stage list exact Layer 4 inputs?
- Is there any reference material loaded by stages that do not need it?

## Handoffs

- Does every downstream stage consume an upstream output?
- Are review gates located where correction is cheapest?
- Can a human edit an output file without breaking the next stage?

## Verification

- Are deterministic checks handled by scripts when practical?
- Do stage contracts name consistency checks?
- Are unresolved questions visible before the workflow proceeds?