# Validation Report

## Structural Checks

| Check | Result | Notes |
| --- | --- | --- |
| Workspace validates with `icm validate --strict` | Pass | Required folders and stage contracts are present |
| Each proposed project stage has a declared output | Pass | Five project-specific stages are mapped |
| Review gates are present | Pass | Source triage, brief draft, and validation gates are explicit |

## Traceability Checks

| Check | Result | Notes |
| --- | --- | --- |
| Major claims must trace to source, decision, or assumption | Pass | Traceability is named in the scaffold and validation stage |
| Source quality is reviewed before synthesis | Pass | Source triage has its own review gate |
| Contradictions and gaps are preserved | Pass | Synthesis notes require both sections |

## Rubric Checks

| Check | Result | Notes |
| --- | --- | --- |
| Discovery report has a review rubric | Pass | `discovery-report-rubric.md` is present in references |
| Rubrics can be enforced by `icm review` | Pass | Required sections, terms, and forbidden terms are deterministic |

## Risks

- The first project-specific workspace should avoid over-automating evidence scoring.
- Private notes need clear handling before real source material is added.
- The final brief rubric should be tuned after one real research sprint.

## Go Or No-Go

Go. The proposed research brief workflow is ready to scaffold and dry-run with a small research question.
