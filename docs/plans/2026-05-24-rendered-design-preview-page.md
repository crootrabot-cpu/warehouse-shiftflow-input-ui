# Rendered Design Preview Page Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Add a real server-rendered preview page inside the FastAPI app so the aggressive redesign proposal can be reviewed as a live route instead of only as a standalone HTML artifact.

**Architecture:** Add one new FastAPI GET route that renders a dedicated Jinja template containing static preview content shaped from the approved aggressive-pass design spec. Keep it intentionally presentation-only: no new persistence, no new data model, no competing frontend system. Verify with a route test that the page renders, exposes the live preview link from the intake surface, and contains the key executive/repo-cleanup markers.

**Tech Stack:** FastAPI, Jinja2 templates, pytest with FastAPI TestClient, existing shared base template/CSS tokens.

---

### Task 1: Add failing route test for the rendered preview page

**Objective:** Prove the app does not yet expose the new rendered preview surface.

**Files:**
- Modify: `tests/test_pages.py`

**Step 1: Write failing test**

Add this test near the other route tests:

```python
def test_design_preview_route_renders_aggressive_pass_markers():
    response = client.get('/design-preview')

    assert response.status_code == 200
    assert 'Aggressive redesign + cleanup preview' in response.text
    assert 'Daily operating picture with the dead weight stripped out.' in response.text
    assert 'Milwaukee control band' in response.text
    assert 'Canonical structure' in response.text
    assert 'FastAPI is canonical' in response.text
```

**Step 2: Run test to verify failure**

Run:
```bash
python3 -m pytest tests/test_pages.py::test_design_preview_route_renders_aggressive_pass_markers -v
```

Expected: FAIL with `404 == 200` because `/design-preview` does not exist yet.

**Step 3: Do not implement yet**

Wait for the route failure before writing production code.

**Step 4: Commit**

Do not commit after red. Move straight to Task 2.

---

### Task 2: Add a preview-link assertion on an existing reachable surface

**Objective:** Make the rendered preview discoverable from the live app instead of being an orphan route.

**Files:**
- Modify: `tests/test_pages.py`

**Step 1: Write failing test**

Extend the existing intake-page test with one assertion:

```python
assert '/design-preview' in response.text
```

Use `test_root_route_returns_operations_report_intake_markers` because it already validates the home page navigation surface.

**Step 2: Run test to verify failure**

Run:
```bash
python3 -m pytest tests/test_pages.py::test_root_route_returns_operations_report_intake_markers -v
```

Expected: FAIL because the intake page does not yet link to `/design-preview`.

**Step 3: Do not implement yet**

Wait for the link assertion to fail before touching templates.

**Step 4: Commit**

Do not commit after red. Move straight to Task 3.

---

### Task 3: Add the FastAPI route for the rendered preview page

**Objective:** Expose a dedicated live route that serves the preview template.

**Files:**
- Modify: `app/main.py`

**Step 1: Write minimal implementation**

Add this route near the other read-only page routes, ideally after `/dashboard` or before `/execute-recap`:

```python
@app.get('/design-preview', response_class=HTMLResponse)
def design_preview_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='design_preview.html',
        context={},
    )
```

**Step 2: Run the first failing test**

Run:
```bash
python3 -m pytest tests/test_pages.py::test_design_preview_route_renders_aggressive_pass_markers -v
```

Expected: FAIL again, but now because `design_preview.html` does not exist instead of 404.

**Step 3: Commit**

Do not commit yet. The route still cannot render.

---

### Task 4: Create the Jinja template for the rendered preview page

**Objective:** Convert the standalone HTML artifact into a server-rendered page that uses the live product shell.

**Files:**
- Create: `templates/design_preview.html`
- Reference: `docs/mockups/2026-05-24-ops-report-aggressive-pass-preview.html`
- Reference: `docs/superpowers/specs/2026-05-24-operations-report-aggressive-redesign-cleanup-design.md`

**Step 1: Create the template**

Use `base.html` and preserve the approved content structure. Start from this shell:

```html
{% extends 'base.html' %}

{% block title %}Aggressive redesign preview • Operations Report{% endblock %}

{% block body %}
  <main class="shell">
    <div class="app-frame">
      <header class="app-topbar">
        <div class="brand-lockup">
          <span class="brand-lockup__meta">Operations report</span>
          <span class="brand-lockup__title">Aggressive redesign + cleanup preview</span>
        </div>
        <div class="topbar-meta">
          <a class="button-link button-link--small" href="/dashboard">Back to dashboard</a>
          <span class="meta-chip meta-chip--accent">Linear × Stripe cockpit</span>
          <span class="meta-chip meta-chip--good">FastAPI is canonical</span>
        </div>
      </header>

      <!-- port the approved preview sections here using existing base tokens -->
    </div>
  </main>
{% endblock %}
```

Required content markers to preserve in the template body:
- `Daily operating picture with the dead weight stripped out.`
- `Milwaukee control band`
- `Canonical structure`
- `Keep active`
- `Quarantine`
- `FastAPI is canonical`

**Step 2: Keep scope tight**

Rules:
- reuse existing `base.html` classes where possible
- add only the minimum inline structure/classes needed for this preview page
- do not create a new CSS file for this one route
- do not wire any dynamic backend data for the preview

**Step 3: Run the route test to verify pass**

Run:
```bash
python3 -m pytest tests/test_pages.py::test_design_preview_route_renders_aggressive_pass_markers -v
```

Expected: PASS.

**Step 4: Commit**

Do not commit yet. The intake link test still needs to go green.

---

### Task 5: Add the preview link to the live intake surface

**Objective:** Make the preview route visible from an existing page in the app.

**Files:**
- Modify: `templates/intake.html`

**Step 1: Add a minimal navigation affordance**

Add one visible link in the intake page action area or top utility/navigation cluster:

```html
<a class="button-link button-link--small" href="/design-preview">Design preview</a>
```

Use the existing button-link styling so the affordance feels native.

**Step 2: Run the intake test to verify pass**

Run:
```bash
python3 -m pytest tests/test_pages.py::test_root_route_returns_operations_report_intake_markers -v
```

Expected: PASS.

**Step 3: Spot-check for accidental wording drift**

The existing assertions in that test cover important navigation and org markers. Do not weaken them.

**Step 4: Commit**

Do not commit yet. Run the focused and full verification first.

---

### Task 6: Run focused verification and full regression suite

**Objective:** Prove the new route works and does not break the existing app.

**Files:**
- No file changes

**Step 1: Run focused page tests**

Run:
```bash
python3 -m pytest tests/test_pages.py -q
```

Expected: all page tests pass.

**Step 2: Run full Python suite**

Run:
```bash
python3 -m pytest tests/ -q
```

Expected: full suite passes with zero failures.

**Step 3: Optional Node suite if any shared frontend surface changed indirectly**

Run:
```bash
node --test test/*.test.mjs
```

Expected: existing JS tests remain green.

**Step 4: Review the diff before commit**

Run:
```bash
git diff -- app/main.py templates/design_preview.html templates/intake.html tests/test_pages.py
```

Expected: only the new route, new template, intake link, and test changes appear.

**Step 5: Commit**

```bash
git add app/main.py templates/design_preview.html templates/intake.html tests/test_pages.py
git commit -m "feat: add rendered design preview page"
```

---

### Task 7: Push the implementation branch update

**Objective:** Make the rendered preview page available from the branch for remote review.

**Files:**
- No file changes

**Step 1: Push**

Run:
```bash
git push origin feature/ops-report-linear-stripe-ui
```

**Step 2: Record the review URL**

Use the existing branch URL pattern and share both:
- the GitHub blob link to `templates/design_preview.html`
- the local route path `/design-preview` for work-computer preview after running the app

**Step 3: Verification note**

Do not claim success without the fresh pytest outputs from Task 6.
