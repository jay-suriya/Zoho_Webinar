---
name: prd
description: Write the developer-facing PRD for a Zoho CRM ⇌ <product> integration by walking the HTML mock flow by flow (webinar.html, mock-reference.html, or any single-file prototype). Produces an indexed, screenshot-led document delivered as .docx through Zoho Writer — why the integration exists, the integration settings page, the full creation flow with every field, and each record state (scheduled live / on-demand, completed, list pages). Use whenever the user asks for a PRD, product requirements, a requirements doc, a spec, or developer documentation for something built in the mock.
---

# PRD — the developer's primary build document

This PRD is what a developer keeps open while building the feature. If they have to open
the mock to answer a question, the PRD has failed.

**It is written by analysing the mock, flow by flow, in the browser.** The mock is the
specification. `.claude/CLAUDE.md` gives you basic context only — persona, vocabulary, a
few decisions — never the requirements themselves. Anything you cannot see in the mock is
an open question, not a sentence you write from memory.

The structure is a **framework**: the same skeleton serves Zoho Webinar today and any
future integration (Survey, Backstage, Bookings…). Only the product name and the record
states change.

---

## 1. Deliverable

A **.docx**, produced through **Zoho Writer**, plus the sources that made it:

```
docs/prd/<integration-slug>/
  prd.md              ← authored source (also the Writer import file)
  prd.html            ← optional: same content with screenshots embedded, for image-safe import
  screens/            ← every screenshot, numbered in reading order
    01-marketplace-zoho.png
    02-integration-intro.png
```

Two ways to get the .docx — try them in this order:

**A. Zoho Writer MCP (preferred when connected).** Create the document in Writer directly,
apply Heading 1/2/3 styles, insert the table of contents, insert the screenshots, then
download as DOCX. Check the connection first — if the server is listed but says *Needs
authentication*, ask the user to run `/mcp` and authenticate, and fall back to B meanwhile.

**B. Import route (always works).** Author `prd.md`, then in Writer:
`File > Import > From Computer` → pick the file → `Insert > Table of Contents` →
`File > Download as > DOCX`. Markdown is a supported import format, and `#/##/###` map to
Heading 1/2/3, which is what the TOC is built from.

Never hand over only a markdown file when a .docx was asked for. Say which route produced
it, and hand back the Writer link plus the downloaded .docx path.

---

## 2. Zoho Writer facts that shape how you write

Confirmed from Zoho Writer help:

- **Import formats**: DOCX, DOC, DOCM, DOT, DOTX, DOTM, ODT, TXT, HTML, HTM, TEX, PDF, **MD**.
  **Export formats**: DOCX, password-protected DOCX, PDF, password-protected PDF, ODT, RTF,
  TXT, EPUB, ZIP, MD. (`File > Import > From Computer`, `File > Download as`.)
- **Table of contents**: `Insert > Table of Contents`. It is built from **Heading styles**,
  so headings must be real headings, not bold text. After edits, click the TOC and
  **Refresh** → *Update entire table*.
- **Captions**: `Insert > References > Captions > Insert a Caption` — object type (Figure,
  Table), numbering, label position; `Auto Caption` for bulk. Use it so figure numbers
  renumber themselves.
- **Cross-references**: `Insert > References > Cross Reference` — to a Heading, bookmark,
  numbered item or captioned object; refresh with *Update Field*.
- **Bookmarks**: `Insert > Bookmark` (manage under Advanced options).

Consequences for what you author:

- Use `#` for the document title, `##` for heading indexes, `###` for sub-indexes, `####`
  at most for a field group. **Never** fake a heading with bold text — it will not reach
  the TOC.
- Plain pipe tables only. No merged cells, no nested tables, no raw HTML inside markdown,
  no footnotes, no nested blockquotes — they either drop or arrive malformed.
- Keep the authored index at the top as a plain nested list *and* insert Writer's own TOC
  after import. The list survives any conversion; the TOC gives real page numbers.
- Markdown image links do **not** carry local files into Writer. Either (a) author
  `prd.html` with the screenshots embedded as base64 `data:` URIs and import that, or
  (b) import the markdown and insert the PNGs from `screens/` at the marked figure
  placeholders. State which you did.
- Caption every screenshot as **Figure N — <what to look at>**; if the document is
  finished inside Writer, apply the captions with `Insert > References > Captions`.

---

## 3. How to analyse the mock (this is the actual work)

1. **Serve and open it.** `python3 -m http.server 8090` in the repo, then
   `http://localhost:8090/<mock>.html?v=1` — always cache-bust with `?v=N`; these mocks
   send no cache headers and Chrome serves stale copies.
2. **Walk every flow like a user**, with the browser tools — click through, don't read
   source and guess. For each flow, record the click path that reaches it.
3. **Exhaust the states.** For every screen: empty, filled, error, validation-blocked,
   permission-denied, enabled/disabled, before/after save. Trigger each one and screenshot
   it. States are where developers lose days.
4. **Open every dialog and dropdown.** Expand every picklist and write down its values in
   the order shown.
5. **Use source only to confirm what you saw**, and to find things the UI hides:

```bash
grep -n 'id="[a-z0-9-]*\(page\|panel\|modal\|overlay\|list\)"' <mock>.html
grep -n '<option' <mock>.html                     # picklist values, verbatim
grep -n 'function [a-zA-Z]*\(open\|show\|render\|save\|send\|create\)' <mock>.html
grep -n 'function [A-Z][A-Za-z]*(' <mock>.html    # React components
```

6. **Read `.claude/CLAUDE.md` and `git log` for context only** — vocabulary, persona, and
   the *why* behind a decision worth quoting. Never let them substitute for looking.
7. **Confirm the index with the user before writing the body** — show the outline, get a
   yes. Ask at most three further questions, and only where the answer changes the
   document.

---

## 4. The index — required shape

The document opens with an **Index** listing every heading index and its sub-indexes.
Worked example — Zoho Webinar. Reuse the shape; swap the product and its record states:

```
Index
  Why CRM–Webinar integration
    What is Zoho Webinar
    Who uses it and for what
    What Zoho Webinar lacks on its own
    How CRM solves it
  Integration
    Where it lives and who can set it up
    Introduction page (before enabling)
    Setup page (Enable Integration)
      Connection details
      Invite modules
      Deal attribution
    Enabled state and re-configuration
  Create webinar
    Entry points
    Webinar details
    Registration setup
    Preferences
    Reminders
    Follow-ups
    Validation and save behaviour
  Scheduled webinar — live
    List page
    Detail page
    Send invite flow
    Registrants and attendance
  Scheduled webinar — on demand
  Completed webinar
  Completed webinar — on demand
  Appendices
    Screen inventory
    Field reference
    Open questions and assumptions
```

Under each heading index, one line saying what that section is for, then its sub-indexes.

---

## 5. What each part must contain

### Part 1 — Why this integration

For a developer who has never used the product:

- **What <product> is**, in two or three plain sentences.
- **Who uses it and for what** — the kinds of businesses and the jobs (SaaS demand-gen
  running product webinars, training companies running paid sessions, B2B teams
  qualifying leads). Concrete, not generic.
- **What it lacks on its own** — registrants living outside the CRM, no link between
  attendance and pipeline, manual exports, no follow-up against CRM records.
- **How CRM solves it** — before/after, tied to what the mock actually does.
- **Where it shows up inside CRM** — modules, pages, entry points.

### Part 2 — Integration (settings)

In the order a user meets it: entry point (exact navigation path) → every state the page
has (not enabled, mid-setup, enabled, disabled again, and the demo cases the mock models:
no account, single org, multiple orgs, not an admin, trial expired) → every section and
control, with what it does, its default, and **why it exists** → downstream effects (e.g.
invite modules decide which modules the invite picker offers). Screenshot every state.

### Part 3 — Creation flow

The most implementation-heavy part: entry points and what pre-fills → the flow step by
step, one screenshot per step and per branch → **every field in a table** (§6), none
skipped, including read-only and derived → conditional logic (which value reveals or hides
what) → validation, what blocks save, exact messages → save behaviour: what is created,
what it is called, where the user lands.

### Part 4 — Record states

One heading index per state — scheduled live, scheduled on demand, completed, completed on
demand. For each: **list page** (columns, views, filters, row and bulk actions, empty
state) → **detail page** (header, status, action buttons, tabs, related lists, panels) →
**what differs from the other states**, called out rather than repeated → the flows
reachable from that state (invite, start, cancel, re-invite, recording, follow-up), each
with its own screenshots and field tables.

### Part 5 — Supporting flows

Whatever the states depend on: email templates and their types, merge fields, link types,
attribution models, push-to-CRM rules. Where a rule set exists, write it as a table (e.g.
template type → allowed links → required link).

### Appendices

**Screen inventory** (figure number, screen, how it is reached, what it demonstrates) ·
**field reference** (every field in one searchable table) · **open questions and
assumptions**, each with an owner.

---

## 6. Field documentation format

| Field | Type | Mandatory | Default | Options / range | Visibility & dependency | Validation | Notes for the developer |
|---|---|---|---|---|---|---|---|
| Webinar title | Single-line text | Yes | Empty | — | Always | Blocks save when empty | Becomes the record name |
| Webinar type | Picklist | Yes | Live Webinar | Live Webinar, On-Demand Webinar, Recurrent Webinar | Always | — | Drives which sections render below |
| Registration type | Picklist | Yes | With Registration | With Registration, Without Registration | Always | — | "Without Registration" hides the registration form and swaps confirmation for a thank-you email |

- Picklist values **verbatim and in UI order** (`grep '<option'` to confirm).
- Mandatory exactly as the UI enforces it, plus what happens when empty.
- The default the mock ships with — defaults are the most commonly mis-built thing.
- Name the fields a field controls in the dependency column.

---

## 7. Screenshots — required, not decorative

- Every flow, every screen, every state that changes the UI, every dialog.
- Captured from the running mock; saved as `screens/NN-short-name.png`, numbered in
  reading order.
- Referenced at the point being described, with a caption that says what to look at:
  `![Figure 7 — Create Webinar, Registration Setup with "Without Registration" selected](screens/07-create-without-registration.png)`
- A screenshot never replaces the words: the field table and rules still get written.
- If a screen cannot be reached in the mock, say so rather than substituting a lookalike.

---

## 8. Rules of evidence

- **The mock is the source of truth**; `.claude/CLAUDE.md` is background. Every statement
  traces to something you saw — name the anchor where it helps (`#integ-intro-panel`,
  `openSlotTemplatePicker()`, `MassEmailModal`).
- **Never invent** metrics, dates, adoption numbers, research or API contracts. Unknowns
  are open questions with owners, or `TBD`.
- **Separate fact from assumption.** Behaviour the mock implies but does not show is an
  assumption in the appendix, not a requirement in the body.
- **Flag divergence** where the mock simplifies or differs from the real Zoho product, so
  nobody builds the shortcut.
- Write for a developer: behaviour, states, data, edge cases. No marketing language.

---

## 9. Reusing this for the next integration

1. Keep the index shape from §4; swap the product name and replace the record states with
   that product's states.
2. Parts 1–3 are unchanged: orientation, settings, creation flow.
3. Part 4 gets one heading index per state of that product's record.
4. Part 5 covers that integration's dependencies.
5. Keep the same field-table columns, screenshot rules and Writer formatting rules, so
   every PRD in the set reads and imports identically.

---

## 10. Before handing it over

- The index matches the headings in the body, in order, and the Writer TOC is inserted and
  refreshed.
- Every flow in scope has screenshots; every screenshot is in the inventory and captioned.
- Every field in every form is tabled with type, mandatory, default and options.
- Each control's purpose is stated, or listed as an open question.
- Record states are differentiated, not duplicated.
- Nothing invented; assumptions in the appendix with owners.
- The .docx opens cleanly: heading styles intact, tables not broken, images present.

Finish by giving the user: the Writer link, the .docx path, the screenshot count, and the
open questions that need their answer.
