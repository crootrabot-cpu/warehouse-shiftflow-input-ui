# Manager Question Flow Implementation Plan

> **For Hermes:** execute this directly; keep the UI prototype honest and local-first.

**Goal:** Expand ShiftFlow so the same page supports both end-of-day reporting and manager-driven question assignment, with hierarchy-aware permissions.

**Architecture:** Keep a pure front-end prototype, but split behavior into a small state/permission module plus UI wiring. The same selected person gets two modes: `Report update` and, if eligible, `Assign questions`. Manager assignment uses a hierarchy graph, local prototype state, and merged question lists so assigned questions immediately appear in the reporting flow.

**Tech Stack:** Static HTML/CSS/JS, ES modules, Node built-in test runner.

---

## Scope

1. Replace the seed roster with the org chart the user gave:
   - Drake → Ricardo, Norman
   - Ricardo → Cody, Luis, Adam, Nate, Emily
   - Cody → Ana, Danielle
   - Luis → Brenda, Ophelia, Remar
   - Adam → Edwin, Maria, Maria L
   - Drake can assign to anyone in the tree
   - Non-managers cannot assign questions
2. Keep one premium page with two modes:
   - `Report update`
   - `Assign questions` (only for eligible managers)
3. Add a manager composer for:
   - target person
   - question text
   - answer type
   - optional helper/options
   - cadence (`Today only`, `Until removed`, `Daily recurring`)
4. Merge default + assigned questions in the report flow so the effect is visible immediately.

## Implementation slices

### Slice 1 — State model and tests
- Create a pure helper module for:
  - people/org tree
  - assignable descendants
  - whether a user can assign
  - merged report questions
  - assignment normalization
- Write tests first for:
  - Drake can assign to all descendants
  - Ricardo only to his subtree
  - non-managers cannot assign
  - merged question list includes assigned questions in stable order

### Slice 2 — HTML structure
- Add mode tabs to the existing chat workspace.
- Add assign-mode panel with:
  - target picker
  - current assigned questions list
  - polished question builder form
  - preview card
- Keep reporting composer intact.

### Slice 3 — UI wiring
- Load the org/assignment data from the helper module.
- When a person is selected:
  - show report mode always
  - show assign mode only if they can manage others
- Persist in local prototype state only.
- Immediately re-render report questions for the assignee after new assignments.

### Slice 4 — Verification
- Run node tests.
- Run local preview.
- Capture screenshots of:
  - report mode
n  - assign mode
- Push the update to GitHub.

## Done definition
- Same page supports both reporting and assignment
- Hierarchy permissions match the provided org tree
- Non-managers cannot assign
- Managers can add polished question assignments intuitively
- Assigned questions appear in the report experience
- Tests pass and repo is pushed
