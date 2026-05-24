# Operations Report Leadership Dashboard Design

**Status:** Approved design, ready for implementation planning
**Date:** 2026-05-24
**Product:** Operations Report
**Primary user:** Drake / leadership

## Goal
Turn the current Operations Report into a visually strong, executive-grade daily operating system that is easy to scan, easy to drill into, and able to produce a structured executive recap for downstream email distribution.

## Product intent
This surface should feel like:
- an executive operations cockpit
- a clean morning dashboard, not a wall of text
- a system that separates signal from noise
- a tool for understanding first, then distributing

It should not feel like:
- a Google Sheet clone
- a raw response dump
- a same-weight page where every answer looks equally important
- a generic AI summary with no operational structure

## Core morning workflow
1. Open the dashboard
2. Scroll quickly to see highlights
3. Dig into specific sections only where needed
4. Click **Execute Recap**
5. Review a drafted executive summary in-app
6. Later hand that draft off into email workflow
7. Add Drake-specific takeaways manually and send onward as needed

## Primary screen architecture
The app should become **dashboard-first**.

The dashboard is the main leadership home base.
From that home base, the user should have obvious paths to:
- recap
- report entry
- question editing / management

The recap becomes a deeper reading and review surface, not the first screen leadership lands on.

## Top-level navigation
The dashboard should contain prominent actions for:
- **Open recap**
- **Start entry**
- **Edit questions**
- **Execute recap**

The interaction goal is memory-free operation. The user should not need hidden routes or route recall.

## Dashboard structure

### 1. Top row
The top row should use a split layout.

#### Left: KPI strip
Show a compact leadership KPI band with high-signal daily metrics such as:
- reports in
- missing reports
- risks
- escalations

These KPIs should be visually distinct and immediately scannable.

#### Right: AI executive brief
Show a short AI-generated leadership brief with:
- short bullets
- thoughtful synthesis
- fast scan hierarchy
- clear prioritization

This brief should be concise enough to understand in seconds, but structured enough to reveal the main operating story of the day.

## 2. Milwaukee roll-up strip
Immediately under the top row, add a dedicated **Milwaukee roll-up strip** owned by **Ricardo**.

This strip acts as a city-level operating summary above the Milwaukee functional sections.

It should summarize:
- overall Milwaukee health
- biggest Milwaukee risks
- missing Milwaukee reports
- escalations needing leadership attention

Ricardo should not only appear as a person in a status list. He should appear as the roll-up owner for Milwaukee operations.

## 3. Functional section blocks
Under the Milwaukee roll-up strip, add distinct functional blocks.

### Milwaukee sections
- **Milwaukee Outbound** — Kody
- **Milwaukee Inventory** — Luis
- **Milwaukee Inbound / Returns** — Emily
- **Milwaukee 2nd Shift** — Hugh
- **Milwaukee Special Projects / B2B** — Adam

### Salt Lake City section
- **Salt Lake City Operations** — Norman

### Leadership layer above sections
- **Drake** remains the top-level leadership reader as VP Operations
- **Ricardo** is Milwaukee operations manager
- **Norman** is Salt Lake City operations manager

## Section composition
Each function block should follow the same visual structure.

### Header
Each section header should include:
- function name
- owner name
- health color

The health color is meant to provide instant scan value before the user reads the text.

### Main comparison row
Each section should have a two-column content row.

#### Left column: reported top 3 priorities
These come directly from the prior EOD inputs.
The workflow assumption is that each EOD flow will explicitly ask for that team or section's **top 3 priorities**.

#### Right column: AI-generated top 3 priorities
These are synthesized by AI based on the broader operating context.

The design intent is to create a deliberate comparison:
- what the team said matters
- what the AI thinks matters

This creates judgment value instead of just repeating operator input.

### Below: status grid
Under the priorities row, show a status grid.

The agreed shape is a **mixed grid**:
- team cards first
- drill-down people rows later

This means V1 should optimize for quick scan of group health rather than immediately exposing every person-level detail.

## Status behavior
The dashboard must clearly show:
- who submitted
- who did not submit
- where leadership risk exists
- where escalation or follow-up is required

If a manager or team did not input anything, that should appear as a visible flag rather than silent absence.

## Readability standard
The current system problem is that all text has the same visual weight. The redesign should explicitly solve that.

Required improvements:
- stronger hierarchy
- bolding of what matters
- filtered and grouped content
- short, thoughtful bulleting
- summary before detail
- color and spacing used for meaning, not decoration

The user should never need to read every single raw response to understand the day.

## AI recap model
The user wants AI synthesis, not just raw storage.

The dashboard and recap system should ultimately synthesize inputs from:
- employee EOD reports
- Slack
- ClickUp
- Gmail

The dashboard should show AI recaps from those sources in the defined operating structure.

The employee-report recap should be present first.
The Slack / ClickUp / Gmail integrations should appear as visible sections or cards, but may remain placeholders with fake data until later integration work is complete.

## Placeholder integration sections
The dashboard should visibly reserve space for:
- ClickUp
- Slack
- Email

These sections can use placeholder / fake data initially.
The point is to establish final information architecture now without blocking visual work on external integration wiring.

## CPO / labor / out-of-SLA section
The dashboard also needs a dedicated section for CPO-related operations data.

This section should be designed to support:
- labor inputs from Ricardo and Norman
- out-of-SLA orders
- related operational exceptions

This data will later be pulled from a separate App Script source that already exists.

In V1, the section can be visually designed and represented with placeholder content.

It should be treated as a first-class operating block, not buried inside another recap paragraph.

## Execute Recap flow
The dashboard needs an **Execute Recap** button.

### Purpose
This action is for turning the dashboard's understanding layer into a distribution-ready leadership summary.

### V1 behavior
When the user clicks **Execute Recap**, the system should:
1. generate a draft executive summary
2. open an in-app review screen
3. let the user review the output before any email handoff happens

The user explicitly chose review-first behavior instead of immediate email draft creation.

### Why review-first
This avoids low-trust one-click draft behavior and keeps the user in control before downstream distribution.

## Executive recap review screen
The review screen should compile:
- quick top summary
- Milwaukee roll-up
- Salt Lake City summary
- functional section summaries
- missing input flags
- CPO / labor / out-of-SLA section
- AI recaps from employee reports
- AI recaps from Slack / ClickUp / Gmail as they become available

The summary should be:
- short at the top
- detailed underneath
- sectioned clearly
- written like a polished executive brief

Milwaukee should naturally receive more weight and more detail than lighter-operating sections because it is busier.

## Future email handoff
After the in-app review flow is accepted, the next stage should support drafting an executive email to Drake.

That future email should include:
- quick summary on top
- section-by-section breakdown below
- issues called out under each relevant section
- missing manager input flags
- both human and AI context combined into one readable brief

Drake will then add final takeaways manually and forward it to whoever needs it.

The system should optimize for this sequence:
- machine composes the structured brief
- human adds judgment and final commentary
- human decides recipients and forwards

## Report detail and recap surfaces
The redesign should not only change the dashboard. It should also improve:
- the recap page
- the individual report reading experience

### Dashboard
Fast-scan leadership home base.

### Recap
Deeper structured readout for leadership review.

### Report detail
Cleaner page for reading one person's submitted content without same-weight text overload.

The three surfaces should feel like parts of one product, not disconnected pages.

## Visual design doctrine
The user explicitly wants this to look visually good and appealing.

The UI should therefore optimize for:
- premium internal-tool feel
- clear visual hierarchy in under 3 seconds
- calm spacing
- bold signal callouts
- restrained color use
- no spreadsheet ugliness
- no generic AI slop styling

The interface should look intentional enough to feel trustworthy for daily leadership use.

## Recommended implementation order
1. Redesign dashboard UI and information architecture
2. Redesign recap UI for executive readability
3. Redesign individual report reading/detail surfaces
4. Add AI summary scaffolding using placeholder or fake generated content
5. Wire real AI summary generation
6. Add Execute Recap review screen
7. Add email draft handoff after in-app review is working
8. Add voice playback of the AI briefing
9. Replace placeholder Slack / ClickUp / Gmail / CPO sections with live integrations

## Voice playback
The user wants a future playback mode where pressing a play button reads the briefing aloud.

This is a real desired feature, but should come after the visual dashboard and review workflow are shaped correctly.

The expected future interaction is:
- open dashboard
- optionally press play
- hear a spoken AI leadership briefing

## Out of scope for this phase
These are explicitly not required to be fully wired in this design phase:
- live Slack integration
- live ClickUp integration
- live Gmail integration
- live CPO / App Script ingestion
- one-click email send
- fully polished voice playback implementation

Placeholders and scaffolding are acceptable for these areas during early implementation.

## Acceptance criteria for the redesign direction
The redesign should be considered directionally successful when:
- the dashboard is clearly the main home base
- the user can scan highlights without reading every raw answer
- Milwaukee and Salt Lake City have clear operating structure
- each major section compares reported priorities vs AI priorities
- missing inputs are visible
- the Execute Recap flow opens a review screen first
- recap and report detail pages feel more readable and intentional
- placeholder external sections exist in the correct locations for later wiring

## Implementation implications
This design implies likely feature additions or changes in the product model:
- explicit top-3-priorities data capture in EOD inputs
- city-level and function-level roll-ups
- section ownership metadata
- health state representation
- dashboard aggregation rules
- review-screen generation logic
- placeholder integration surfaces for external systems
- future AI summarization orchestration across multiple inputs

## Final design decision summary
Locked decisions:
- main surface is dashboard-first
- top row is KPI strip left, AI brief right
- Milwaukee has a Ricardo roll-up strip
- functional sections are grouped by real operating ownership
- each section compares reported top 3 vs AI top 3
- status grid is mixed: team cards first, deeper rows later
- Execute Recap opens an in-app review screen first
- ClickUp / Slack / Email / CPO areas can start as placeholders
- visual quality is a primary requirement, not a nice-to-have
