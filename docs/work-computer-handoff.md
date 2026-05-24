# Operations Report — Work Computer Handoff

**Date:** 2026-05-24
**Repo:** `https://github.com/crootrabot-cpu/warehouse-shiftflow-input-ui`
**UI branch:** `feature/ops-report-linear-stripe-ui`

## Goal
Use GitHub as the source of truth so work on the Operations Report app can move out of Telegram and onto the work computer cleanly.

## What branch to use
For the current redesign work, use:

```bash
feature/ops-report-linear-stripe-ui
```

Do **not** edit random local-only files on the server and expect that to stay sane.
Use the branch.

## Clone on the work computer
If the repo is not already on the machine:

```bash
git clone https://github.com/crootrabot-cpu/warehouse-shiftflow-input-ui.git
cd warehouse-shiftflow-input-ui
git checkout feature/ops-report-linear-stripe-ui
```

If the repo is already there:

```bash
cd warehouse-shiftflow-input-ui
git fetch origin
git checkout feature/ops-report-linear-stripe-ui
git pull
```

## Python setup
Create a virtual environment and install the app dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run locally
Start the app with uvicorn:

```bash
source .venv/bin/activate
python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8789
```

Open locally:

```text
http://127.0.0.1:8789/dashboard
```

Other useful routes:

```text
http://127.0.0.1:8789/
http://127.0.0.1:8789/recap
http://127.0.0.1:8789/execute-recap
```

## Run tests
Python tests:

```bash
source .venv/bin/activate
python3 -m pytest tests/ -q
```

Node tests:

```bash
node --test test/*.test.mjs
```

## Current design direction
The current UI redesign direction is locked here:

```text
docs/superpowers/specs/2026-05-24-operations-report-linear-stripe-executive-cockpit-ui.md
```

That is the visual source of truth for the next pass.

## Working rules
- GitHub is the source of truth.
- Keep redesign work on `feature/ops-report-linear-stripe-ui` until it is ready to merge.
- Commit in clean slices.
- Run tests before pushing.
- Use pull requests if you want reviewable checkpoints.

## Useful Git loop
```bash
git status
git add <files>
git commit -m "feat: improve leadership cockpit ui"
git push origin feature/ops-report-linear-stripe-ui
```

## Important repo reality
This repository still contains older prototype surfaces and some unrelated local-only changes on the VPS worktree.
That is exactly why branch discipline matters.

For the Operations Report app, stay focused on:
- `app/`
- `templates/`
- `tests/`
- `requirements.txt`
- relevant docs under `docs/`

## Recommended next sequence
1. Pull `feature/ops-report-linear-stripe-ui`
2. Run the app locally
3. Review dashboard / recap / execute recap surfaces
4. Keep pushing UI improvements to the same branch
5. Merge to `main` once the redesign is actually sharp
