# Setup Questionnaire

Use these questions before the first real weekly run. Answers should populate stable Layer 3 files.

## Must Answer

| Question | Why It Matters | Target File |
| --- | --- | --- |
| What channels are in scope for the first workflow? | Calendar planning needs valid channel names | `_config/channel-guide.md` |
| What tone should approved content use? | Review pack and validation need editorial standards | `_config/editorial-rules.md` |
| What counts as an acceptable source? | Prevents weak or unsourced items from moving downstream | `stages/05_validation/references/source-checklist.md` |
| Who approves themes before calendar planning? | Keeps the review gate actionable | `_config/project-profile.md` |
| What fields must every content calendar item include? | Enables deterministic checks later | `_config/quality-gates.md` |

## Helpful But Optional

| Question | Target File |
| --- | --- |
| What previous content should the workflow imitate? | `_config/editorial-rules.md` |
| Which topics should be avoided? | `_config/editorial-rules.md` |
| How many items should be planned per week? | `_config/channel-guide.md` |
| What priority labels should be used? | `stages/02_theme_selection/references/theme-rubric.md` |

## Seed Answers For This Example

| Question | Example Answer |
| --- | --- |
| Channels | Blog and newsletter first; social can wait |
| Tone | Clear, practical, lightly opinionated, and source-aware |
| Source standard | Each item needs a source link, approved internal decision, or explicit assumption |
| Theme approver | Hobo |
| Calendar fields | Date, channel, title, source, owner, status, notes |

## Recommendation

Collect the must-answer items before generating the project-specific workspace. Defer optional questions until after the first weekly run reveals which preferences actually matter.
