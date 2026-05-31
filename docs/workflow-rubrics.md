# Workflow Rubric Guide

Use this guide when you know the kind of workflow you are building, but you are not sure which deterministic `icm review` checks to use.

The rule of thumb: keep human judgment in the Review Gate, and use rubrics for artifact shape, source coverage, required sections, placeholder cleanup, and other checks a script can verify repeatably.

## Choose By Workflow

| Workflow | Useful Artifacts | Good Rubric Checks | Example |
| --- | --- | --- | --- |
| Project planning | Source inventory, milestone map, project calendar, decision log, review pack | Required sources, table columns, link/path count, `source-inventory`, `calendar`, `decision-log` | `examples/completed-project-plan` |
| Research brief | Source traceability table, source triage, synthesis, recommendation | Required sections, required sources, required terms, forbidden placeholders | `examples/completed-research-brief` |
| Content planning | Source inventory, theme selection, content calendar, approval pack | Required sections, required sources, table columns, calendar shape once dates stabilize | `examples/completed-content-plan` |
| Documentation refresh | Source inventory, gap analysis, update plan, release calendar, decision log | Table columns, link/path count, `source-inventory`, `calendar`, `decision-log` | `examples/completed-documentation-refresh` |
| Release readiness | Validation report, source inventory, changelog check, upgrade smoke | Required sections, required terms, path count, source inventory shape | `docs/release-ready-workspace.md` |

## Project Planning Starter

For a project-planning workflow, begin with source traceability and common artifact shapes.

Discovery report rubric:

```markdown
## Required Sections

- Known Facts
- Assumptions
- Open Questions
- Source Traceability
- Candidate Workflow
- Risks
- Discovery Recommendation

## Required Sources

- ../00_intake/output/project-brief.md
- references/discovery-question-bank.md
- ../../_config/quality-gates.md

## Required Table Columns

- Source
- Used For

## Required Link Or Path Count

- 3
```

Project calendar rubric:

```markdown
## Required Sections

- Calendar
- Review Notes

## Required Artifact Shapes

- calendar
```

Decision log rubric:

```markdown
## Required Sections

- Decisions
- Review Notes

## Required Artifact Shapes

- decision-log
```

## Research Starter

Research workflows should emphasize source coverage and recommendation discipline.

```markdown
## Required Sections

- Known Facts
- Source Traceability
- Source Quality
- Recommendation
- Risks

## Required Terms

- confidence
- source quality
- traceability

## Required Sources

- ../00_intake/output/project-brief.md
- references/discovery-question-bank.md

## Forbidden Terms

- TBD
- lorem ipsum
```

## Documentation Starter

Documentation workflows often need both source coverage and table shape checks.

```markdown
## Required Table Columns

- Source
- Used For

## Required Link Or Path Count

- 3

## Required Artifact Shapes

- source-inventory
```

## Practical Advice

- Use required sections when the artifact needs a predictable reading order.
- Use required terms when a concept must appear somewhere, but not necessarily as a heading.
- Use required sources when an artifact must cite specific upstream files or decisions.
- Use table-column checks when a human reviewer expects scan-friendly rows.
- Use path counts only as a floor; a human still decides whether the cited sources are good.
- Use artifact shapes for source inventories, calendars, and decision logs that should stay machine-checkable.
- Add forbidden terms for placeholders and known failure modes.
