# ShiftFlow Input Prototype

A premium conversational input prototype for warehouse end-of-day reporting.

## What this is

This is the **first UI wedge** for the broader warehouse reporting tool:
- choose your name
- get greeted personally
- answer assigned questions **one at a time**
- finish with a clean closeout

It is intentionally built as a **beautiful front-end prototype first** so the interaction can be pressure-tested before wiring it into Apps Script.

## Product stance

This should become:
- **GitHub-managed source of truth** for the UI
- **Apps Script-backed operational workflow** for assignments, answer persistence, and reporting

That means:
- GitHub = versioned UI code, prototype iteration, design system, reviewable changes
- Apps Script = employee roster, assigned questions, persistence, daily runs, and later dashboard generation

## Current prototype features

- Premium name picker with search
- Personalized greeting
- One-question-at-a-time transcript flow
- Quick replies for yes/no and choices
- Text / textarea / number answer modes
- Progress rail
- Completion state
- Mobile-friendly layout

## Local preview

```bash
cd /home/fabric-02-rabot/Desktop/warehouse-input-ui-prototype
python3 -m http.server 8044
```

Open:

```text
http://127.0.0.1:8044
```

## Files

- `index.html` — app shell and UI structure
- `assets/style.css` — premium visual system
- `assets/app.js` — prototype interaction logic and seeded employee/questions data
- `data/notes.md` — next integration notes

## Next step after UI approval

Wire this into Apps Script with this split:

1. **Apps Script / Google Sheets**
   - employees
   - assigned questions
   - answer capture
   - session timestamps

2. **Web app frontend**
   - fetch roster + assigned questions
   - render this conversational flow
   - post answers back to Apps Script endpoints

3. **Later dashboard layer**
   - manager tie-out
   - AI summary
   - KPI stitching

## Notes

This is a front-end prototype. It does **not** persist answers yet.
