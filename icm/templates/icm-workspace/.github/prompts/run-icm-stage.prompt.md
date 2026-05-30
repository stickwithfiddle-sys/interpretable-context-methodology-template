---
description: "Run one ICM stage from its stage contract and write the declared outputs"
argument-hint: "Stage path, for example stages/02_stage_mapping"
agent: "agent"
---

Run the ICM stage named in the user's message.

Follow this protocol:

1. Read `AGENTS.md` and `CONTEXT.md`.
2. Read the selected stage's `CONTEXT.md`.
3. Load only the Layer 3 and Layer 4 inputs declared by that stage.
4. Execute the Process section.
5. Write only the declared Outputs into the stage `output/` folder.
6. Run the Verify section and report the result.
7. Stop at the Review Gate and summarize what the human should inspect.