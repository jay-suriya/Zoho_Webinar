---
name: prd
description: Write the developer-facing PRD for a Zoho CRM ⇌ <product> integration from its HTML mock (webinar.html, mock-reference.html, or any single-file prototype). Produces an indexed, screenshot-led document — why the integration exists, the integration settings page, the full creation flow with every field, and each record state (scheduled live / on-demand, completed, list pages) — formatted for upload to Zoho Writer. Use whenever the user asks for a PRD, product requirements, a requirements doc, a spec, or developer documentation for something built in the mock.
---

# PRD — the developer's primary build document

This PRD is what a developer keeps open while building the feature. It is not a pitch and
not a summary: if a developer has to open the mock to answer a question, the PRD has
failed. It is written from the mock, illustrated with screenshots of the mock, and
uploaded to **Zoho Writer**, so it must survive that import cleanly.

The structure is a **framework** — the same skeleton serves Zoho Webinar today and any
future integration (Survey, Backstage, Bookings…). Only the product name and the record
states change.

---

## 1. Output

```
docs/prd/<integration-slug>/
  prd.md              ← the document
  screens/            ← every screenshot, numbered in reading order
    01-marketplace-zoho.png
    02-integration-intro.png
    …
```

- One markdown file. Headings only from `#` to `####`; simple pipe tables; no raw HTML,
  no footnotes, no nested blockquotes — Zoho Writer handles those badly.
- Screenshots as separate PNGs referenced with a relative path *and* a figure number
  (`![Figure 4 — Send Invite, record picker](screens/04-send-invite-records.png)`), so
  that after import the figure references still read correctly even if an image needs to
  be re-inserted by hand.
- Tell the user the path when done, and offer once to also produce an artifact or an
  HTML version for a cleaner Writer import.

---

## 2. Before writing: ground yourself

1. `.claude/CLAUDE.md` — persona, product concepts, integration surface, and the **Mock
   Edit Log**, which records what changed and *why*. The "why" belongs in the PRD.
2. `README.md` and `.claude/rules/*.md` (design tokens/constraints).
3. `git log --oneline -40`, then `git log -20 --format='%s%n%b'` — commit bodies in these
   repos carry decisions and rejected alternatives. Quote them where they explain a
   choice.
4. Anything the user has said in this session about intent, and any screenshots they
   shared.

Then **run the mock** — do not document from source alone:

```bash
cd <repo> && python3 -m http.server 8090     # then http://localhost:8090/<mock>.html?v=1
```

Cache-bust with `?v=N` on every reload — these mocks send no cache headers and Chrome
will serve a stale copy.

Map the surface before describing it:

```bash
grep -n 'id="[a-z0-9-]*\(page\|panel\|modal\|overlay\|list\)"' <mock>.html
grep -n '<!-- ═\|<!-- ===\|SECTION [0-9]' <mock>.html
grep -n 'function [a-zA-Z]*\(open\|show\|render\|save\|send\|create\)' <mock>.html
grep -n 'function [A-Z][A-Za-z]*(' <mock>.html          # React components
grep -n '<option\|<select' <mock>.html                  # picklist values
```

---

## 3. Confirm the index before writing the body

Draft the index (§4 shape), show it to the user, and get a yes. Writing 15 pages against
the wrong outline wastes everyone's time. Ask at most three other questions, and only if
the answer changes the document: scope (whole integration or one flow), release target,
and whether real metric baselines exist.

---

## 4. The index — required shape

The document opens with an **Index** listing every heading index and its sub-indexes.
Heading indexes are `##`; sub-indexes are `###`; anything deeper is `####`.

Worked example — Zoho Webinar. Reuse the shape, swap the product and its record states:

```
Index
  Why CRM–Webinar integration
    What is Zoho Webinar
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

Every heading index carries a one-line "what this section is for" under it, then its
sub-indexes.

---

## 5. What each part must contain

### Part 1 — Why this integration (the orientation the developer needs first)

Written for someone who has never used the product:

- **What <product> is** — in two or three sentences, in plain language.
- **Who uses it and why** — the kinds of businesses and the jobs they use it for
  (e.g. SaaS demand-gen running product webinars, training companies running paid
  sessions, B2B teams qualifying leads). Concrete, not generic.
- **What it lacks on its own** — the real gap: registrant lists that live outside the
  CRM, no link between attendance and pipeline, manual exports, no follow-up automation
  against CRM records.
- **How CRM solves it** — what the integration changes, expressed as before/after.
- **Where it is used inside CRM** — the modules, pages and entry points touched.

Keep this factual. If the mock or `.claude/CLAUDE.md` does not support a claim, do not
make it.

### Part 2 — Integration (settings)

Walk the developer through the settings surface in the order a user meets it:

- **Entry point** — the exact navigation path (e.g. Setup → Marketplace → Zoho → the
  product card → Set up), with a screenshot.
- **Each state** the page has — not enabled, mid-setup, enabled, disabled again, and any
  demo/edge cases the mock models (no account, multiple orgs, not an admin, trial
  expired). Screenshot each state.
- **Every section and control**: what it is, what it does, its default, and **why it is
  there** — the product reason, not the mechanic. A control whose purpose you cannot
  explain is an open question, not a sentence to invent.
- **Downstream effects** — where a setting shows up later (e.g. invite modules decide
  which modules the invite recipient picker offers).

### Part 3 — Creation flow

The most implementation-heavy part. For the whole flow:

- The **entry points** and what pre-fills.
- The flow itself, step by step, with a screenshot per step and per branch.
- **Every field, in a table** (see §6). No field is skipped, including read-only and
  derived ones.
- **Conditional logic** — which field reveals or hides which, and on what value.
- **Validation and errors** — what is mandatory, what blocks save, the exact message.
- **Save behaviour** — what is created, what it is called afterwards, where the user
  lands.

### Part 4 — Record states

One heading index per state the record can be in — for Webinar: scheduled live, scheduled
on demand, completed, completed on demand. For each:

- **List page** — columns, filters, views, row actions, bulk actions, empty state.
- **Detail page** — header, status, action buttons, tabs, related lists, and what each
  panel shows.
- **What differs from the other states** — this is the part developers get wrong; call
  out the differences explicitly rather than repeating the shared bits.
- **The flows reachable from that state** — invite, start, cancel, re-invite, recording,
  follow-up — each with its own screenshots and field tables.

### Part 5 — Supporting flows

Anything the states depend on: email templates and their types, merge fields, link types,
attribution models, push-to-CRM rules. Document the rules as tables where a rule set
exists (e.g. template type → allowed links → required link).

### Appendices

- **Screen inventory** — every screenshot: number, screen, how it is reached, what it
  demonstrates.
- **Field reference** — one merged table of every field in the document, for search.
- **Open questions and assumptions** — with owners.

---

## 6. Field documentation format

Every field table uses these columns. Fill each cell; `—` when genuinely not applicable.

| Field | Type | Mandatory | Default | Options / range | Visibility & dependency | Validation | Notes for the developer |
|---|---|---|---|---|---|---|---|
| Webinar title | Single-line text | Yes | Empty | — | Always | Blocks save when empty | Becomes the record name |
| Webinar type | Picklist | Yes | Live Webinar | Live Webinar, On-Demand Webinar, Recurrent Webinar | Always | — | Drives which sections render below |
| Registration type | Picklist | Yes | With Registration | With Registration, Without Registration | Always | — | "Without Registration" hides the registration form and swaps the confirmation email for a thank-you email |

Rules:

- **List every picklist value verbatim** from the mock (`grep '<option'`), in the order
  shown.
- Mark mandatory fields exactly as the UI does, and say what happens when they are empty.
- State the default the mock ships with — developers build defaults wrong more often than
  anything else.
- Where a field controls other fields, name them in the dependency column.

---

## 7. Screenshots — required, not decorative

- **Every flow gets screenshots**: every screen, every state that changes the UI (empty,
  filled, error, permission-denied, enabled/disabled), and every dialog.
- Capture with the browser tools against the running mock; save as
  `screens/NN-short-name.png`, numbered in reading order.
- Reference inline at the point being described, with a caption that says what to look
  at: `![Figure 7 — Create Webinar, Registration Setup with "Without Registration" selected](screens/07-create-without-registration.png)`.
- A screenshot never replaces the text. The field table and the rules still get written.
- If a screen cannot be reached in the mock, say so in the text rather than substituting a
  similar one.

---

## 8. Rules of evidence

- **The mock is the source of truth.** Every statement traces to something in it — a
  screen, a control, a picklist, a function. Where useful, name the anchor
  (`#integ-intro-panel`, `openSlotTemplatePicker()`, `MassEmailModal`).
- **Do not invent** metrics, dates, adoption numbers, research findings or API contracts.
  Anything unknown is an open question with an owner, or `TBD`.
- **Separate fact from assumption.** If the mock implies behaviour it does not show,
  write it as an assumption in the appendix, not as a requirement.
- **Flag divergence.** Where the mock simplifies or differs from the real Zoho product,
  say so in a note so the developer does not build the shortcut.
- **Explain the why once, then stop.** Product reasoning belongs in Part 1 and in the
  "why it is there" line of each control — not repeated in every paragraph.
- Write for a developer: behaviour, states, data, edge cases. Skip marketing language.

---

## 9. Reusing this for a new integration

1. Copy the index shape from §4; replace "Webinar" with the product and replace the
   record states with that product's states (a Survey integration might be: survey
   created, sent, collecting responses, closed).
2. Parts 1, 2 and 3 stay as they are — orientation, settings, creation flow.
3. Part 4 gets one heading index per state of that product's record.
4. Part 5 covers whatever that integration depends on.
5. Keep the same field-table columns and the same screenshot rules, so every PRD in the
   set reads the same way.

---

## 10. Before handing it over

- The index at the top matches the headings in the body, in order.
- Every flow in scope has screenshots; every screenshot is in the inventory.
- Every field in every form appears in a field table with type, mandatory, default and
  options filled in.
- Each control's purpose is stated, or listed as an open question.
- Record states are differentiated, not duplicated.
- No invented data anywhere; assumptions are in the appendix with owners.
- The file renders correctly as plain markdown (headings, tables, images) so the Writer
  import is clean.

Finish by telling the user the file path, the number of screenshots captured, and the
list of open questions that need their answer.
