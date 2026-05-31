# End-To-End Playtest

Use this when you want to experience the whole ICM loop without inventing a project idea.

The idea: build an ICM workspace plan for a tiny product called **Meeting Notes To Action Plan**. The final workspace should help a solo operator turn rough meeting notes into a prioritized action plan with owners, dates, and risks.

## 1. Create The Playtest Workspace

```bash
python -m pip install --upgrade icm-workspace-template
rm -rf ~/icm-meeting-notes-playtest
icm new ~/icm-meeting-notes-playtest --name "Meeting Notes To Action Plan" --with-common-artifacts
cd ~/icm-meeting-notes-playtest
icm status .
```

## 2. Fill The Intake Brief

Replace `stages/00_intake/output/project-brief.md` with:

```markdown
# Project Brief

## Desired Outcome

Create a project-specific ICM workspace that turns messy meeting notes into a clear action plan.

The workflow should take one markdown file of rough notes and produce:

- A concise meeting summary.
- A table of action items with owner, due date, priority, and status.
- A risks and open questions section.
- A short follow-up message that can be sent to the team.

## Audience Or Users

The primary user is a solo operator or small-team lead who has meeting notes but does not want to manually extract every action item.

The reviewer is the person who attended the meeting and can confirm whether the action items are accurate.

## Success Criteria

- The generated workflow has no more than five stages.
- Every stage has one clear output file.
- The action-item output uses a markdown table with Owner, Action, Due Date, Priority, and Status columns.
- The workflow includes a review gate before any follow-up message is drafted.
- The final validation stage checks for missing owners, fuzzy dates, and unresolved open questions.

## Constraints

- Keep everything in markdown.
- Do not assume a project-management app.
- Dates should use YYYY-MM-DD when known.
- Unknown owners or dates should be marked as open questions, not invented.
```

## 3. Review And Accept Intake

```bash
icm review stages/00_intake
icm accept stages/00_intake --reviewer Hobo --note "Brief is clear enough for discovery."
icm status .
```

Open the dashboard and confirm `00_intake` is accepted:

```bash
icm dashboard .
```

## 4. Ask Your Agent To Run Discovery

Paste this into your coding agent:

```text
Read AGENTS.md and CONTEXT.md, then run stages/01_discovery.
Load only the inputs declared in stages/01_discovery/CONTEXT.md.
Use the project brief to discover the workflow for Meeting Notes To Action Plan.
Write stages/01_discovery/output/discovery-report.md.
Run the Verify checks and stop at the Review Gate.
```

Then run:

```bash
icm review stages/01_discovery
icm accept stages/01_discovery --reviewer Hobo --note "Discovery has enough source traceability and workflow shape."
```

## 5. Continue Stage By Stage

Use the same pattern for each stage:

```bash
icm next .
icm explain stages/02_stage_mapping
```

Paste this prompt, changing the stage path each time:

```text
Read AGENTS.md and CONTEXT.md, then run the next stage shown by `icm next .`.
Load only the inputs declared in that stage's CONTEXT.md.
Write only the declared outputs.
Run the Verify checks and stop at the Review Gate.
```

After each stage:

```bash
icm review stages/02_stage_mapping
icm accept stages/02_stage_mapping --reviewer Hobo --note "Accepted for the playtest."

icm review stages/03_scaffold
icm accept stages/03_scaffold --reviewer Hobo --note "Accepted for the playtest."

icm review stages/04_questionnaire
icm accept stages/04_questionnaire --reviewer Hobo --note "Accepted for the playtest."

icm review stages/05_validation
icm accept stages/05_validation --reviewer Hobo --note "Validation is accepted for this playtest."
```

## 6. Finish The Playtest

```bash
icm validate . --strict
icm doctor . --strict
icm status .
```

Open:

```bash
shared/acceptance-log.md
```

You should see accepted rows for each reviewed handoff. In the dashboard, accepted stages should look different from machine-passing stages.

## What To Notice

- You did not need to invent an idea.
- The agent only worked one numbered stage at a time.
- `icm review` checked the handoff.
- `icm accept` recorded your human decision in a markdown file.
- The dashboard read the same files and CLI JSON as the terminal.
