# Ops Boardroom Minimal Redesign

**Date:** 2026-05-24  
**Product:** Operations Report  
**Surface priority:** Dashboard first, recap second, shared shell system underneath both

## Goal

Replace the current dashboard/recap presentation with a boardroom-grade internal operations tool that feels restrained, precise, and obviously professional.

This redesign is explicitly correcting a failed direction. The previous pass read as self-conscious, hypey, and over-designed — closer to a startup ad or AI-generated premium concept than a serious operations product. The new direction must feel like a real internal tool used by executives and operators every day.

## Design north star

**Apple/Braun boardroom minimal with ops density.**

That means:
- restrained, almost industrial simplicity
- premium through typography, spacing, alignment, and reduction
- plain business language instead of invented product language
- serious information surfaces instead of decorated hero modules
- calm authority, not visual performance

The result should feel like:
- a premium internal boardroom tool
- a serious leadership operating system
- something built carefully by a strong product/design team

It must **not** feel like:
- a landing page
- a startup promo surface
- a dribbblized dashboard
- “luxury SaaS”
- a design exercise trying to impress with labels, glow, or pseudo-brand language

## Core correction

The main issue with the current version is not just visual styling. It is the combination of:
- hype-heavy naming
- over-signaled section framing
- too many chips, bands, and “special” surfaces
- copy that sounds authored for effect instead of utility
- card treatment that calls attention to itself

The redesign must subtract aggressively.

## Product language rules

All visible copy should use plain operations language.

### Preferred language
Use direct terms like:
- Ops
- Recap
- Reports
- Notes
- Issues
- Open items
- Coverage
- Managers
- Teams
- Milwaukee
- SLC
- Yesterday
- Today
- Follow-up
- Status
- Summary
- Metrics

### Avoid completely
Do not use language like:
- Quiet Command Luxury
- Executive control strip
- command band
- control spine
- weighted KPI rail
- attention pressure
- ranked read
- posture first
- command note
- any phrase that sounds coined for style instead of clarity

### Naming examples
Use plain replacements such as:
- `Executive command deck` → `Ops`
- `Executive control strip` → `Ops summary`
- `Weighted KPI rail` → `Key metrics`
- `Milwaukee control spine` → `Milwaukee`
- `AI executive brief` → `Ops notes`
- `Attention pressure by lane` → `Open issues by team`
- `Team coverage graph` → `Report coverage`
- `Execute recap` → `Generate recap`

## Screen archetype

Primary screen archetype:
- **dashboard / cockpit**

But the dashboard should be expressed more like a **boardroom operations console** than a conventional SaaS dashboard.

That means the page should behave like a leadership readout:
1. quick summary
2. key metrics
3. operating notes
4. major site/team sections
5. follow-up detail

Not:
1. hero concept
2. decorated feature blocks
3. marketing-style panels
4. secondary utility content

## Shared visual system

### Palette
Use a restrained boardroom palette:
- near-black background
- graphite surfaces
- soft gray typography
- off-white highlights
- extremely limited blue usage

Blue should only survive as a subtle interaction accent or selected-state hint. It should not define the emotional tone of the product.

Warm neutrals are acceptable in tiny doses if they make the surface feel more expensive, but the interface should remain predominantly neutral.

### Contrast
- text contrast should remain strong
- muted text should still be comfortably readable
- contrast should come from luminance, not from bright color

### Corners and elevation
- reduce radius further from the current system
- reduce shadows further from the current system
- use flatter planes and finer borders
- surfaces should feel machined, not plush

### Borders
- thin, quiet borders
- stronger use of separators/dividers where structure helps scanning
- less dependence on giant rounded cards to create grouping

### Typography
Typography should do most of the premium work.

Requirements:
- cleaner hierarchy
- shorter headings
- less theatrical sentence casing
- fewer all-caps moments
- stronger relationship between title, label, and value
- tighter label styles for metrics and metadata
- tabular figures everywhere counts matter

The visual impression should be:
- serious
- edited
- deliberate
- expensive because it is controlled

Not:
- loud
- expressive
- brand-performative

## Layout strategy

### Dashboard top area
The current top area is too concept-driven.

Replace it with a more practical structure:
- left: page title + one-line ops summary
- right: date + primary action + secondary navigation

This should read as a professional tool header, not a hero section.

### Summary row
The first meaningful content row should become an ops summary row with very plain framing:
- reports in
- missing reports
- open issues
- follow-ups

Visually:
- flatter
- more even
- less “feature card” energy
- easier to scan in one glance

### Metrics row
Metrics should look like metrics, not promotional statistic blocks.

Requirements:
- plain labels
- disciplined values
- quieter support text
- consistent alignment
- less oversized emphasis unless one value truly deserves it

### Notes block
The current AI/summary surface should become a plain internal notes block.

Requirements:
- rename it to something like `Ops notes`
- make it feel editorial and operational
- remove synthetic “AI premium module” styling
- use a simpler list treatment with clearer ranking

### Milwaukee surface
Milwaukee should remain important because it is operationally important, not because it has a special branded container.

Requirements:
- heading simply `Milwaukee`
- clear owner line
- direct summary text
- issues / next steps / notes structure
- less decorative framing
- stronger operational readability

Milwaukee should feel like the most important region on the page because of layout priority and clarity, not because it is wrapped in dramatic styling.

### Section modules
Section modules should move away from chunky cards and toward calmer structured blocks.

Requirements:
- less boxiness
- better use of internal dividers
- clearer owner / summary / status order
- reported vs recommended priorities should be renamed in plainer language
- status items should look like instrumentation, not colorful badges

### Graphs
Graphs should become quieter and more precise.

Requirements:
- thinner strokes / more restrained fills where possible
- less toy-like bar-card feel
- fewer heavy boxes around tiny visualizations
- labels should read like reporting labels, not dashboard features

Graph titles should also be renamed more plainly.

## Recap page direction

The recap should feel like the dashboard’s sibling in the same system.

It should read like a premium internal memo.

Requirements:
- simpler header
- less splashy hero treatment
- more memo-like rhythm
- stronger alignment in the metric row
- email draft area should look like a serious internal output artifact
- submitted updates / missing updates / follow-ups should feel like structured review sections, not feature cards

## Interaction model

The interaction model should remain simple and familiar.

Do not add novelty.

Preferred interaction tone:
- obvious primary action
- calm secondary actions
- less pill overload
- fewer visually “special” controls
- no experimental motion language

## What to remove or reduce immediately

The next implementation pass should aggressively remove or reduce:
- invented naming
- premium-posturing copy
- oversized hero framing
- chip clutter
- decorative gradient emphasis
- chunky graph cards
- over-separated sections
- flashy emphasis where simple alignment would be better

## Success criteria

The redesign is successful only if:
- the user no longer feels it looks like a cheap ad
- the copy sounds like a real ops tool, not a brand exercise
- the dashboard reads as professionally restrained within 3 seconds
- the page feels cooler and more expensive through control, not decoration
- Milwaukee remains important without theatrical framing
- recap feels like part of the same system
- the whole product looks like it was carefully edited by experienced designers

## Implementation priorities

### Phase A — Immediate correction pass
1. remove hypey language from dashboard and recap
2. rename major sections into plain ops terms
3. reduce glow, color, and decorative framing
4. flatten top-of-page treatment into a tool header + summary row
5. quiet the metrics and graphs

### Phase B — Structural polish pass
1. tighten Milwaukee layout
2. rework section modules into calmer review blocks
3. refine recap into memo-quality output
4. unify spacing and divider logic across both pages

### Phase C — Final taste pass
1. polish typography ratios
2. refine borders and density
3. reduce any remaining startup-dashboard energy
4. ensure mobile still feels premium and clear

## Non-goals

This redesign is not trying to:
- make the app look futuristic
- make the app look luxury-branded
- increase visual drama
- add more concept language
- impress through novelty

It is trying to make the app look **obviously professional, restrained, and real**.
