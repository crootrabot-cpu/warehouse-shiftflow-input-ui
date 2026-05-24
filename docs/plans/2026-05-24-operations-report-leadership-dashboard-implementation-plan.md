# Operations Report Leadership Dashboard Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Ship a dashboard-first executive operations surface with Milwaukee/Salt Lake City roll-ups, sectioned priorities, mixed status grid, placeholder external integrations, and an Execute Recap review screen.

**Architecture:** Keep the current FastAPI + server-rendered Jinja + SQLite stack. Extend the domain model with section metadata and richer default report questions, add aggregation/view-model helpers for dashboard and recap review, then replace the basic templates with an executive-grade cockpit layout.

**Tech Stack:** FastAPI, Jinja2, SQLite, pytest, existing systemd/cloudflared deployment.

---

## Task 1: Lock plan assumptions into failing dashboard tests

**Objective:** Add route/page tests that encode the new leadership dashboard shape before touching implementation.

**Files:**
- Modify: `tests/test_pages.py`

**Step 1: Write failing tests**
Add tests covering:
- `/dashboard` shows KPI strip, AI executive brief, Execute Recap, Open recap, Start entry, Edit questions
- `/dashboard` shows Milwaukee roll-up, Milwaukee Outbound, Milwaukee Inventory, Milwaukee Inbound / Returns, Milwaukee 2nd Shift, Milwaukee Special Projects / B2B, Salt Lake City Operations
- `/dashboard` shows placeholder sections for ClickUp, Slack, Email, and CPO / labor / out-of-SLA
- `/execute-recap` or equivalent review route renders executive recap review surface

**Step 2: Run targeted tests to verify failure**
Run:
`python3 -m pytest tests/test_pages.py::test_dashboard_page_renders_leadership_home_base tests/test_pages.py::test_execute_recap_review_page_renders_executive_sections -q`

Expected: FAIL because the current dashboard/review routes do not contain the new structure.

**Step 3: Commit**
`git add tests/test_pages.py && git commit -m "test: define leadership dashboard surface"`

---

## Task 2: Add report-priority capture tests

**Objective:** Make EOD capture explicit top-3-priority content for later section roll-ups.

**Files:**
- Modify: `tests/test_pages.py`
- Modify: `tests/test_repository.py`

**Step 1: Write failing tests**
Add tests proving:
- report form includes a top-3-priorities prompt for relevant submitters
- submitted report stores that content
- dashboard/review aggregators can surface that content in section cards

**Step 2: Run targeted tests to verify failure**
Run:
`python3 -m pytest tests/test_pages.py::test_report_form_includes_top_three_priorities_prompt tests/test_repository.py::test_saved_report_preserves_top_three_priorities_answer -q`

Expected: FAIL before model and aggregator changes exist.

**Step 3: Commit**
`git add tests/test_pages.py tests/test_repository.py && git commit -m "test: require top-three-priority capture"`

---

## Task 3: Update org/domain model for real leadership sections

**Objective:** Add the section ownership data and updated org roster needed by the new dashboard.

**Files:**
- Modify: `app/models.py`
- Modify: `tests/test_repository.py`

**Step 1: Write/adjust tests first**
Add expectations for:
- Ricardo = Milwaukee operations
- Norman = Salt Lake City operations
- Kody = Milwaukee outbound
- Hugh = Milwaukee 2nd shift
- Luis = Milwaukee inventory
- Adam = Milwaukee special projects / B2B
- Emily = Milwaukee inbound / returns

**Step 2: Implement minimal model changes**
In `app/models.py`:
- update `PERSON_DEFS` and person roles/teams to reflect approved org shape
- add Hugh as a real person
- add a new dataclass for leadership sections, e.g. `LeadershipSection`
- define section metadata mapping dashboard section id -> owner -> location -> label
- extend default questions to include a top-3-priorities question

**Step 3: Run targeted tests**
Run:
`python3 -m pytest tests/test_repository.py::test_leadership_sections_match_approved_org tests/test_pages.py::test_root_route_renders_real_org_roster_markers -q`

Expected: PASS.

**Step 4: Commit**
`git add app/models.py tests/test_repository.py tests/test_pages.py && git commit -m "feat: add leadership section metadata and org updates"`

---

## Task 4: Build dashboard aggregation helpers

**Objective:** Compute KPI, roll-up, priorities, missing flags, placeholder integrations, and section cards in Python instead of scattering logic into templates.

**Files:**
- Create: `app/dashboard.py`
- Modify: `app/recap.py`
- Modify: `tests/test_repository.py` or create `tests/test_dashboard.py`

**Step 1: Write failing aggregator tests**
Add tests proving dashboard builder can:
- compute KPI counts
- identify missing submissions
- build Milwaukee roll-up
- build section cards with reported priorities and AI priorities
- return placeholder cards for ClickUp / Slack / Email / CPO

**Step 2: Implement minimal dashboard builder**
Create dataclasses for:
- KPI strip
- AI executive brief bullets
- city roll-up
- section card
- status cards
- integration placeholder cards

Use deterministic placeholder AI bullets initially:
- derive from saved summaries / risks / assigned answers
- return stable fake integration summaries for now

**Step 3: Run targeted tests**
Run:
`python3 -m pytest tests/test_dashboard.py -q`
or if kept in repository tests:
`python3 -m pytest tests/test_repository.py::test_build_dashboard_returns_milwaukee_rollup_and_placeholders -q`

Expected: PASS.

**Step 4: Commit**
`git add app/dashboard.py app/recap.py tests/test_dashboard.py tests/test_repository.py && git commit -m "feat: add executive dashboard view models"`

---

## Task 5: Wire dashboard route to the new builder

**Objective:** Replace the current simplistic dashboard route with a dashboard view-model route.

**Files:**
- Modify: `app/main.py`
- Modify: `tests/test_pages.py`

**Step 1: Keep failing route tests red if needed**
Verify the dashboard page tests still fail against the old route.

**Step 2: Minimal implementation**
In `app/main.py`:
- import the dashboard builder
- replace raw `report_items` context with a richer `dashboard` context
- add an `execute recap` review route, preferably `GET /execute-recap`

**Step 3: Run targeted route tests**
Run:
`python3 -m pytest tests/test_pages.py::test_dashboard_page_renders_leadership_home_base tests/test_pages.py::test_execute_recap_review_page_renders_executive_sections -q`

Expected: PASS.

**Step 4: Commit**
`git add app/main.py tests/test_pages.py && git commit -m "feat: wire leadership dashboard and execute recap route"`

---

## Task 6: Redesign dashboard template and shared styling

**Objective:** Make the dashboard visually strong, sectioned, and easy to scan.

**Files:**
- Modify: `templates/dashboard.html`
- Modify: `templates/base.html`

**Step 1: Implement one archetype**
Use a dashboard/cockpit archetype:
- top KPI strip on left
- AI brief on right
- Milwaukee roll-up band
- section cards under it
- integrations and CPO placeholders lower on page

**Step 2: Add token-driven styles**
In `base.html`, extend shared styles for:
- KPI cards
- executive brief panel
- section headers with health pills
- split priority columns
- status grids
- muted placeholder cards
- stronger typography hierarchy

**Step 3: Run route tests**
Run:
`python3 -m pytest tests/test_pages.py::test_dashboard_page_renders_leadership_home_base -q`

Expected: PASS while improving readability.

**Step 4: Commit**
`git add templates/dashboard.html templates/base.html && git commit -m "feat: redesign dashboard as executive cockpit"`

---

## Task 7: Build the Execute Recap review screen

**Objective:** Add the in-app review-first recap screen chosen by the user.

**Files:**
- Create: `templates/execute_recap.html`
- Modify: `app/recap.py`
- Modify: `app/main.py`
- Modify: `tests/test_pages.py`

**Step 1: Write/keep failing route test**
The review page test should assert:
- quick top summary
- Milwaukee summary
- Salt Lake City summary
- functional sections
- missing input flags
- CPO / labor / out-of-SLA section
- AI summaries from employee reports and placeholder Slack/ClickUp/Gmail blocks

**Step 2: Implement minimal review builder**
Either extend `build_recap(...)` or create a review-specific builder returning:
- short summary block
- section summaries
- missing-input list
- integration placeholder summaries

**Step 3: Render review template**
Make the screen readable enough to feel like a pre-email executive memo.

**Step 4: Run targeted tests**
Run:
`python3 -m pytest tests/test_pages.py::test_execute_recap_review_page_renders_executive_sections -q`

Expected: PASS.

**Step 5: Commit**
`git add templates/execute_recap.html app/recap.py app/main.py tests/test_pages.py && git commit -m "feat: add execute recap review screen"`

---

## Task 8: Improve submitted-report detail readability

**Objective:** Make individual report pages easier to skim and aligned with the new product style.

**Files:**
- Modify: `templates/report_submitted.html`
- Modify: `tests/test_pages.py`

**Step 1: Add or update tests**
Assert the report detail page highlights:
- summary
- top priorities
- watchouts
- assigned answers
with stronger visual grouping.

**Step 2: Implement minimal template changes**
Rework report detail into grouped cards instead of one flat stack of equal-weight answers.

**Step 3: Run targeted tests**
Run:
`python3 -m pytest tests/test_pages.py::test_submit_report_route_redirects_to_confirmation_page -q`

Expected: PASS.

**Step 4: Commit**
`git add templates/report_submitted.html tests/test_pages.py && git commit -m "feat: improve report detail readability"`

---

## Task 9: Improve recap page readability

**Objective:** Make `/recap` feel like a deeper executive read, not a raw dump.

**Files:**
- Modify: `templates/recap.html`
- Modify: `app/recap.py`
- Modify: `tests/test_pages.py`

**Step 1: Keep or add recap page assertions**
The page should show stronger hierarchy and grouped sections, not flat same-weight content.

**Step 2: Implement minimal template improvements**
Add:
- top summary band
- clearer missing-input emphasis
- grouped functional/roll-up sections if feasible from current data

**Step 3: Run targeted tests**
Run:
`python3 -m pytest tests/test_pages.py::test_recap_page_groups_submissions_missing_people_and_assigned_answers -q`

Expected: PASS.

**Step 4: Commit**
`git add templates/recap.html app/recap.py tests/test_pages.py && git commit -m "feat: polish executive recap page"`

---

## Task 10: Full verification and live rollout

**Objective:** Verify everything, restart the live service, and confirm local/public behavior.

**Files:**
- Modify as needed from prior tasks

**Step 1: Run full test suite**
Run:
`python3 -m pytest tests/ -q`
`node --test test/*.test.mjs`

Expected: all pass.

**Step 2: Restart service**
Run:
`systemctl --user restart operations-report.service && systemctl --user status operations-report.service --no-pager -n 30`

Expected: service active on `127.0.0.1:8789`.

**Step 3: Verify local routes**
Check:
- `/`
- `/dashboard`
- `/recap`
- `/execute-recap`
- one report detail route

**Step 4: Verify public routes**
Check:
- `https://operations-report.odinsfabric.com/dashboard`
- `https://operations-report.odinsfabric.com/recap`
- `https://operations-report.odinsfabric.com/execute-recap`

**Step 5: Commit final implementation**
`git add app templates tests docs/plans && git commit -m "feat: ship leadership dashboard redesign"`

---

## Notes for implementation
- Keep external integrations as placeholders with fake but believable data in V1.
- Do not try to fully solve email sending in this pass.
- Use deterministic placeholder AI summaries first so tests stay stable.
- Preserve existing routes where possible; add new routes rather than breaking old user flow abruptly.
- Keep the live URL stable and verify content markers publicly before claiming success.
