# Stage Map

## Proposed Project-Specific Workflow

| Stage | Purpose | Primary Inputs | Main Output | Review Gate | Verify |
| --- | --- | --- | --- | --- | --- |
| `00_intake` | Capture research question, audience, deadline, and constraints | Project profile, prior decisions | `research-brief-intake.md` | Confirm decision question and audience | Intake names question, audience, deadline, sources, and open questions |
| `01_source_triage` | Classify source links and notes by relevance and source quality | Intake, evidence rules | `source-triage.md` | Confirm no important source is missing | Every source has type, relevance, quality, and use decision |
| `02_synthesis` | Extract themes, contradictions, confidence, and open gaps | Source triage, evidence rules | `synthesis-notes.md` | Confirm synthesis is balanced | Notes separate facts, interpretations, assumptions, contradictions, and gaps |
| `03_brief_draft` | Produce a decision-ready research brief | Synthesis notes, brief style | `research-brief.md` | Approve, request changes, or block recommendation | Brief includes recommendation, evidence, confidence, and risks |
| `04_validation` | Check traceability and readiness before acceptance | Research brief, traceability checklist | `validation-report.md` | Go/no-go decision | Every major claim traces to source, decision, or assumption |

## Handoff Pattern

```text
research-brief-intake.md
  -> source-triage.md
  -> synthesis-notes.md
  -> research-brief.md
  -> validation-report.md
```

## Layer 3 Files To Seed

| File | Used By |
| --- | --- |
| `_config/evidence-rules.md` | Source triage, synthesis, validation |
| `_config/brief-style.md` | Brief draft |
| `shared/decision-log.md` | All stages |
| `stages/01_source_triage/references/source-types.md` | Source triage |
| `stages/04_validation/references/traceability-checklist.md` | Validation |

## Review Gate Rationale

- Source triage is the cheapest place to correct missing or weak evidence.
- Brief draft is the cheapest place to correct framing before validation.
- Validation prevents recommendations from moving forward without traceability.

## Recommendation

Approve this map for scaffold planning. Do not add automated source scoring until the human rubric has been used on real research inputs.
