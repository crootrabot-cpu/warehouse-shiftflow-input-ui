# Operations Report UI Redesign — Linear × Stripe Executive Cockpit

**Status:** Selected direction
**Date:** 2026-05-24
**Product:** Operations Report
**Chosen direction:** Linear × Stripe executive cockpit

## Decision
The UI direction is locked to a **Linear × Stripe executive cockpit**.

This means:
- Linear-level hierarchy, darkness, spacing discipline, and precision
- Stripe-level polish, trust, premium data presentation, and executive credibility
- no generic AI dashboard styling
- no rainbow admin-template behavior
- no wall of same-sized cards

## Product feeling
The app should feel like:
- a premium leadership operating system
- a sharp daily cockpit for VP/ops leadership
- a calm but high-signal command surface
- a tool that separates what matters from what can wait

It should not feel like:
- an internal CRUD app with nicer colors
- a noisy NOC board
- a generic startup analytics template
- a “look, AI summary” toy

## Visual doctrine

### Foundation
- dark-mode-first shell
- near-black background with soft layered panels
- monochrome base with one primary accent
- restrained use of semantic health colors
- typography-first hierarchy

### Color strategy
Use a mostly neutral palette:
- background: near-black / graphite
- panels: slightly lifted charcoal
- text: soft white and cool gray
- accent: indigo-violet or deep electric blue
- semantic colors only for health, risk, missing inputs, and escalation

Color must be used for meaning, not decoration.

### Typography strategy
Borrow the strongest shared traits from Linear and Stripe:
- compressed, authoritative headings
- high contrast between headline, section label, body, and metadata
- tabular numerals for KPI surfaces
- short executive labels and eyebrow text
- stronger distinction between primary and secondary text

## Layout system

### Global page structure
1. top utility bar
2. leadership hero / control band
3. KPI + executive brief row
4. city roll-up band
5. section grid
6. integration / intelligence layer
7. drill-down detail surfaces

### Top utility bar
Must include:
- product title
- today/date context
- freshness timestamp
- quick filters or scope controls later
- primary actions: Open recap, Start entry, Edit questions, Execute recap

This bar should look expensive and intentional, not like plain nav links.

### Leadership hero / control band
Add a slim but high-impact leadership band that establishes:
- current operating posture
- biggest risk
- biggest opportunity
- number of missing manager inputs

This should read like a cockpit header, not a marketing hero.

### KPI row
The KPI row should become more premium and more legible:
- larger tabular numerals
- tighter labels
- optional delta/signal chips
- stronger spacing between cards
- one card can be visually dominant if the day has a major problem

KPIs should feel financially trustworthy, not dashboard-generator generic.

### AI executive brief panel
This panel should feel like a serious executive artifact:
- premium surface treatment
- stronger title and subtitle hierarchy
- structured bullets with rank/order
- callouts for urgent items
- optional micro-tags like Risk, Coverage, Throughput, SLA

The AI brief should feel curated, not dumped.

## Milwaukee roll-up treatment
The Milwaukee roll-up should become a signature surface.

It should have:
- stronger horizontal band treatment
- Ricardo clearly presented as owner
- health status visible instantly
- key Milwaukee attention items surfaced without requiring paragraph reading
- missing Milwaukee reports shown as chips or flags

This is not just another card. It is the city-level operational spine of the page.

## Section card redesign
All section cards should be rebuilt with a premium cockpit system.

### Section card anatomy
1. eyebrow label
2. section title
3. owner line
4. health chip
5. summary sentence
6. left/right priority comparison
7. status grid
8. escalation / missing-input / next-action footer if needed

### Priority comparison row
The reported-vs-AI comparison must be visually obvious.

Recommended treatment:
- left column = Reported priorities
- right column = AI priorities
- subtle divider or contrast shift between columns
- identical structure so comparison is fast

### Status grid
Avoid generic stacked boxes.

Use:
- compact team tiles
- stronger chips for submitted/missing/risk
- owner or team markers
- optional progress bars or density markers later

## Integration layer
ClickUp, Slack, Gmail, and CPO should look intentional even while placeholder-backed.

They should be designed as:
- intelligence modules
- not disabled junk cards
- each module gets a short summary, freshness note, and one useful key line

The point is to make future integrations feel inevitable, not bolted on.

## Report detail and recap styling
The product must become visually unified.

### Recap page
Should feel like:
- a polished executive memo
- stronger than the current generic output
- clearer sectional hierarchy
- same design language as dashboard

### Report detail page
Should feel like:
- one person’s operating snapshot
- grouped signal blocks
- easier scan of summary, top 3, and watchouts

## Motion and polish
Use subtle motion only where it adds quality:
- hover lift
- soft transitions on cards/chips/buttons
- active/focus states that feel premium
- no gimmick animation

## Interaction standards
- obvious primary actions
- keyboard-focus visible and tasteful
- drill-downs should later open in-panel or modal, not force constant page hops
- filters and timestamps should make screenshots self-explanatory

## Anti-patterns to ban
- too many same-sized cards
- thick glowing gradients everywhere
- full rainbow status systems
- giant charts with low value
- generic bootstrap/tailwind-template look
- oversized border radii that make it feel toy-like
- generic AI sparkle iconography
- long undifferentiated paragraphs

## Implementation guidance

### Phase 1: shell and tokens
- replace current ad-hoc styles with a tokenized visual system
- define spacing, radius, border, shadow, and typography scales
- add premium shared components in base template

### Phase 2: dashboard restructure
- rebuild dashboard with stronger hierarchy
- promote Milwaukee roll-up into a signature band
- rebuild section cards and KPI/brief row

### Phase 3: recap and report detail unification
- bring recap and submitted report surfaces into same visual system
- tighten readability and executive memo feel

### Phase 4: richer interactions
- richer filters
- drill-down panels
- saved views later
- real integration states later

## GitHub workflow recommendation
The app should be worked in GitHub, not Telegram.

Recommended operating model:
- keep GitHub as source of truth
- keep deployable main branch clean
- do UI redesign work on a focused feature branch
- pull that branch from the work computer
- edit there and push back normally

Suggested branch naming:
- `feature/ops-report-linear-stripe-ui`

## Success criteria
This redesign is successful when:
- a first glance immediately feels premium and current
- the app no longer reads like a bland AI dashboard
- the hierarchy is obvious in under 3 seconds
- Milwaukee roll-up feels important and differentiated
- section cards feel sharp and decision-oriented
- recap and report surfaces feel like one product
- the UI is good enough that showing it side-by-side with top modern SaaS dashboards is not embarrassing
