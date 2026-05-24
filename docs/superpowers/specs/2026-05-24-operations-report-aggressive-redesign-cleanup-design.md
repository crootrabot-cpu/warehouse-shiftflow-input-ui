# Operations Report — Aggressive Redesign + Repo Cleanup Design

**Status:** Proposed
**Date:** 2026-05-24
**Product:** Operations Report
**Branch:** `feature/ops-report-linear-stripe-ui`

## Goal
Execute one integrated pass that improves the live executive product surface while making the repository structurally honest.

This pass should make two things true at once:
1. the app feels like a premium leadership cockpit instead of a dressed-up internal tool
2. the repo clearly communicates which surfaces are active, which are legacy, and which files should not be touched during normal product work

## Decision
Chosen direction: **aggressive integrated pass**

This means:
- redesign the live FastAPI product surface and only the live FastAPI product surface
- stop treating prototype and experimental files as peers of the active app
- quarantine legacy experiments into an explicit non-canonical area
- update docs so a work-computer handoff is obvious and low-friction

## Current repo truth
The repository currently mixes three realities:
1. the active server-rendered FastAPI app
2. older static prototype surfaces
3. standalone dashboard experiment files that are no longer the product source of truth

That creates avoidable confusion. A contributor can currently look at the repo and reasonably wonder whether the real product is:
- `templates/` + `app/`
- `operations-report.html`
- `assets/operations-report-*`
- the older shiftflow prototype files

That ambiguity is the structural problem this pass fixes.

## Canonical product surface
The active app is:
- `app/`
- `templates/`
- `tests/`
- `requirements.txt`
- relevant product docs under `docs/`

The design and engineering work should treat these as the only canonical product surface.

## Legacy and experimental material
The following files should no longer sit in the main product path pretending to be current:
- `operations-report.html`
- `assets/operations-report-dashboard.css`
- `assets/operations-report-dashboard.js`
- `assets/operations-report-state.mjs`
- `test/operations-report-state.test.mjs`

There is also unrelated worktree drift that should not contaminate this redesign branch:
- `assets/shiftflow-state.mjs`
- `test/shiftflow-state.test.mjs`
- `.superpowers/`
- `data/operations-report.db`

## Repo structure proposal
Target repo shape:

```text
warehouse-shiftflow-input-ui/
├── app/
├── templates/
├── tests/
├── docs/
│   ├── work-computer-handoff.md
│   ├── plans/
│   └── superpowers/specs/
├── legacy/
│   └── experiments/
│       └── operations-report-static/
│           ├── operations-report.html
│           ├── assets/
│           └── test/
├── requirements.txt
└── README.md
```

## Repo cleanup stance
### Recommended action
**Move first, delete later.**

The dashboard experiment files should be moved into a quarantined legacy area instead of deleted immediately. This preserves reference material while making the active app unmistakable.

### Why this is better than immediate deletion
- safer during active iteration
- preserves useful reference code if any styling logic needs to be borrowed
- removes day-to-day confusion without pretending the static experiment is still canonical

### Documentation update requirement
The README should explicitly say:
- the active product is the FastAPI app under `app/` and `templates/`
- legacy experiments are preserved under `legacy/`
- feature work should not happen against quarantined static experiments unless explicitly revived

## Product direction
### Visual sentence
**Quiet, high-trust, decision-first operations software with Linear precision and Stripe restraint.**

### Product feeling
The app should feel like:
- a premium leadership operating system
- a daily command surface for VP operations
- calm, high-signal, and deliberate
- decision-oriented rather than report-oriented

It should not feel like:
- a dressed-up internal CRUD app
- a dashboard template with better colors
- a generic AI control panel
- a surface where every card shouts equally loudly

## Screen archetype
Primary archetype: **executive dashboard / cockpit**

The dashboard is not a feed, not a BI board, and not a generic admin panel. It should establish a strong reading order that makes decisions easier in the first 10 seconds.

## Token contract
The redesign should stay within a restrained system:

### Color
- near-black / graphite page shell
- lifted charcoal surfaces
- soft white and cool gray text
- one restrained accent in indigo-violet / deep electric blue territory
- semantic colors only for meaning: good, warning, bad, missing, escalation

### Typography
- compressed high-authority headings
- strong contrast between section eyebrow, title, body, and metadata
- tabular numerals for KPIs and counts
- short labels, not long soft headings

### Shape and depth
- moderate radii, not toy-like radii
- restrained border contrast
- minimal but premium depth
- subtle transitions only where they improve scanning and trust

## Reading order
Target reading order:
1. utility context and freshness
2. operating posture / main decision band
3. weighted KPI layer
4. Milwaukee control band
5. section-by-section operating surfaces
6. recap / executive memo surfaces
7. individual detail surfaces

If the first screen does not make the day’s posture and top decision clearer, the redesign has failed.

## Dashboard redesign
### 1. Top utility bar
The top utility bar should feel expensive and operational, not like plain navigation.

It should contain:
- product title
- date context
- freshness timestamp
- later-ready scope controls
- action cluster: Open recap, Start entry, Edit questions, Execute recap

### 2. Leadership control band
The current hero is good but still too overview-shaped. It should become a decision band.

It should surface:
- current operating posture
- biggest risk
- biggest opportunity
- missing inputs count with visible names or chips if relevant
- one dominant primary action, usually Execute recap

Example content shape:
- **Operating posture:** At risk
- **Biggest risk:** Milwaukee outbound is carrying unresolved labor pressure into first wave
- **Biggest opportunity:** Returns and inventory can absorb cleanup if outbound is protected
- **Missing inputs:** Hugh, Adam

This should read like a morning command band, not a product-marketing hero.

### 3. KPI row
The KPI row should stop implying equal importance every day.

Required changes:
- larger tabular numerals
- shorter, tighter labels
- one dominant KPI surface when the day has a clear operational issue
- secondary KPI cards for supporting metrics
- richer subtext that explains why the number matters

A missing-input or escalation card should be able to dominate when that is the real story.

### 4. Milwaukee control band
Milwaukee should become the unmistakable operational spine of the page.

Required content:
- owner identity: Ricardo
- city health posture
- what is observed
- what leadership needs now
- what happens if nothing changes

Example structure:
- **Observed**
- **Need now**
- **Consequence**

This is better than generic bullet recap because it creates a decision window.

### 5. Section card redesign
Each section should move from information module to stance-oriented operating surface.

Recommended section anatomy:
1. eyebrow label
2. owner + role
3. health posture
4. executive read sentence
5. observed priorities vs interpreted priorities comparison
6. compact status grid
7. leadership stance / next trigger footer

Example footer:
- **Leadership stance:** Monitor only
- **Next trigger:** Escalate if dock slip exceeds 30 minutes

The footer is important because it turns reading into action framing.

### 6. Integration layer
Integration placeholders should remain, but they must look intentional.

Each should present:
- short summary
- freshness or placeholder note
- one useful implication line

They should feel like inevitable future intelligence modules, not disabled junk cards.

## Recap and detail redesign
### Recap page
The recap should become a real executive memo.

It should reorganize around:
- **Do now**
- **Watch**
- **Ignore for now**
- corroborated wins
- corroborated risks
- follow-up answers
- appendix / raw support

This is a stronger reading model than simply grouping “submitted” and “missing.”

### Execute recap page
The execute recap surface should become the sharpest decision artifact in the product.

It should support:
- a concise decision stack
- stronger stance language
- obvious separation between now / watch / ignore
- cleaner executive handoff / email-prep framing

### Submitted report detail page
The individual report page should stop being a flat answer dump.

It should be reorganized into grouped signal blocks such as:
- summary
- top 3 priorities
- risks / watchouts
- assigned answers
- leadership takeaway

The goal is to make one person’s report feel like an operating snapshot.

## Cleanup boundaries
### Keep active
- `app/`
- `templates/`
- `tests/`
- `docs/`
- `requirements.txt`
- `README.md`

### Quarantine
- `operations-report.html`
- `assets/operations-report-dashboard.css`
- `assets/operations-report-dashboard.js`
- `assets/operations-report-state.mjs`
- `test/operations-report-state.test.mjs`

### Investigate separately
- `assets/shiftflow-state.mjs`
- `test/shiftflow-state.test.mjs`
- `.superpowers/`
- `data/operations-report.db`

These should not be silently rolled into this redesign without an explicit reason.

## Execution order
1. declare canonical structure in docs and repo layout
2. quarantine legacy static dashboard experiment files
3. update README to explain active vs legacy surfaces
4. strengthen dashboard reading order and hierarchy
5. upgrade recap and detail surfaces into one unified memo-like system
6. run tests and route verification
7. review git diff for structural clarity

## Constraints
- do not migrate the stack away from FastAPI + Jinja just to chase trendiness
- do not create a second competing frontend system
- do not preserve ambiguity about which files are canonical
- do not over-design with gradients, oversized radii, or decorative AI chrome

## Success criteria
This pass is successful when:
- the repo clearly tells a new contributor what the real product is
- the live app feels like a premium executive cockpit in under 3 seconds
- the top of the dashboard clarifies posture and decision window immediately
- Milwaukee feels structurally important, not just visually present
- section cards express stance, not just information
- recap and detail pages feel like part of the same leadership product
- the branch is easier to continue from a work computer without guesswork

## Non-goals
This pass does not need to:
- wire real integrations yet
- invent new data models unrelated to presentation and organization
- solve all legacy drift in the repository beyond clearly quarantining it
- build advanced charts just to look enterprise
