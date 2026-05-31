# Quality Gates

Use these standards when reviewing stage outputs.

## Completeness

- The output answers the stage purpose.
- All declared outputs exist in the stage `output/` folder.
- Open questions are marked explicitly instead of hidden in prose.

## Traceability

- Major claims point back to an input, reference file, or reviewer decision.
- Downstream recommendations do not contradict upstream decisions.
- Repeated output corrections are candidates for source-level updates.

## Usability

- The next stage can consume the output without guessing.
- File names match the stage contract.
- Tables and lists are used when they make handoffs easier to scan.

## Risk

- Safety, privacy, compliance, and operational risks are named.
- Assumptions that could invalidate the workflow are visible.
- Deterministic calculations or checks are delegated to scripts when practical.