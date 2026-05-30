# Discovery Report

## Known Facts

- The target workflow produces a decision-ready research brief.
- Inputs arrive as research questions, source links, notes, transcripts, and prior decisions.
- Source quality matters because recommendations should be traceable.
- Human review gates are needed before synthesis becomes recommendation.
- The first implementation should stay model-neutral and file-based.

## Assumptions

- A small research sprint can use markdown artifacts without a database.
- One stakeholder is available to approve source quality and final recommendations.
- Low/medium/high confidence labels are easier to review than numeric scores at first.
- Sensitive source material can be summarized without copying private details into final outputs.

## Open Questions

- Which source types count as primary evidence for this project?
- Should contradictory evidence block the final recommendation or become a risk note?
- Should final briefs include a separate source appendix?

## Source Traceability

| Source | Used For |
| --- | --- |
| `../00_intake/output/project-brief.md` | Research question, audience, constraints, and success criteria |
| `references/discovery-question-bank.md` | Discovery coverage and question prompts |
| `../../_config/quality-gates.md` | Review gate, traceability, and validation expectations |

## Users And Reviewers

| Role | Need | Review Concern |
| --- | --- | --- |
| Researcher | Turn mixed evidence into a brief | Missing sources or weak synthesis |
| Stakeholder | Decide what to do next | Hidden assumptions or overclaiming |
| Reader | Understand the recommendation quickly | Unclear evidence strength |

## Candidate Workflow

1. Capture the research question, audience, decision deadline, and constraints.
2. Inventory sources and classify evidence strength.
3. Synthesize themes, contradictions, and confidence.
4. Draft the brief with claims, evidence, and recommendation.
5. Validate traceability, confidence, and open risks.

## Candidate Layer 3 Material

| File | Purpose |
| --- | --- |
| `_config/evidence-rules.md` | Stable rules for source quality and confidence |
| `_config/brief-style.md` | Expected brief structure and tone |
| `shared/decision-log.md` | Cross-run research and scope decisions |
| `stages/01_source_triage/references/source-types.md` | Source classification guidance |
| `stages/04_validation/references/traceability-checklist.md` | Final evidence checks |

## Candidate Layer 4 Artifacts

| Artifact | Produced By | Consumed By |
| --- | --- | --- |
| `research-brief-intake.md` | Intake | Source triage |
| `source-triage.md` | Source triage | Synthesis |
| `synthesis-notes.md` | Synthesis | Brief draft |
| `research-brief.md` | Brief draft | Validation |
| `validation-report.md` | Validation | Human go/no-go decision |

## Risks

| Risk | Mitigation |
| --- | --- |
| Weak source quality supports a strong recommendation | Require confidence labels and validation checks |
| Sensitive notes leak into public-ready output | Keep private notes in references and summarize only approved facts |
| Synthesis hides contradictory evidence | Require contradictions and uncertainty to be named |
| Review happens too late | Add review gates after source triage and validation |

## Discovery Recommendation

Proceed to stage mapping with a five-stage workflow. Keep traceability explicit, make source quality visible, and avoid adding a dashboard until the CLI review language stabilizes.
