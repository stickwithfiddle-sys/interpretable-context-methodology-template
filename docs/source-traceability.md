# Source Traceability

Source traceability means an output names the files, inputs, references, or decisions it relied on.

In ICM, this matters because a human reviewer should be able to answer: "Where did this claim, stage decision, or recommendation come from?"

## Beginner Pattern

Add a short section to important outputs:

```markdown
## Source Traceability

| Source | Used For |
| --- | --- |
| `../00_intake/output/project-brief.md` | Goals, audience, constraints, and success criteria |
| `references/discovery-question-bank.md` | Question coverage |
| `../../_config/quality-gates.md` | Review and validation expectations |
```

Then add the same source paths to the stage rubric:

```markdown
## Required Sources

- ../00_intake/output/project-brief.md
- references/discovery-question-bank.md
- ../../_config/quality-gates.md
```

Run:

```bash
icm review stages/01_discovery
```

The review fails when the output does not cite a required source by path or filename.

## Good Habits

- Cite the source path when the output depends on a file, prior stage output, or reusable reference.
- Cite a decision-log entry when the output depends on an approved decision.
- Cite assumptions separately from facts.
- Keep private or sensitive source material in references and summarize only approved facts in outputs.
- Do not use traceability as proof that a claim is true; use it as a pointer for human review.
