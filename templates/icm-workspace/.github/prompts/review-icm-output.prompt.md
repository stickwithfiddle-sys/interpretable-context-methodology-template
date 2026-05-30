---
description: "Review a stage output against its ICM contract and upstream sources"
argument-hint: "Stage path or output file to review"
agent: "agent"
---

Review the stage output named in the user's message.

Check it against:

1. The stage `CONTEXT.md`.
2. The Layer 3 reference files declared in Inputs.
3. The upstream Layer 4 artifacts declared in Inputs.
4. The stage's Verify section.

Report mismatches, missing requirements, stale assumptions, and source-level fixes that would improve future runs.