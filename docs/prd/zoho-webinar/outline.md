# Zoho Webinar ⇌ Zoho CRM Integration — PRD outline (for approval)

Target: six Zoho Writer documents — links in the STATUS section below.
Source of truth: `webinar.html` walked at http://localhost:8090/webinar.html

## Index

1. **Why CRM–Webinar integration**
   - What Zoho Webinar is
   - Who uses it and for what
   - What Zoho Webinar lacks on its own
   - How CRM solves it
   - Where it shows up inside CRM
2. **Integration**
   - Where it lives and who sets it up (Setup ▸ Marketplace ▸ Zoho ▸ Zoho Meetings ▸ For webinars)
   - Introduction page, before enabling (hero · How it works ×4 · Why teams enable it ×4 · what enabling does)
   - Account states the mock models — Case 1 no account · Case 2 single org · Case 3 multiple orgs · Case 4 not an admin · Case 5 trial expired
   - Setup page: Email · Organisation · Sync past webinars
   - Zoho Webinar Invite Modules (chips + search + Standard/Custom groups; drives the Send Invite module picker)
   - Webinar Deal Attribution (toggle on by default; First / Last Interaction, **Linear = default**, Increasing / Decreasing Time Decay, Position-Based)
   - Enabled state, re-configuration and Save bar
3. **Create webinar**
   - Entry points and layout switcher (Standard ▾ · Edit Page Layout · Cancel / Save & New / Save)
   - Webinar Details — every field, type, default, picklist values
   - Registration Setup — With/Without Registration and everything it reveals or hides
   - Preferences
   - Reminders (1st–3rd + their templates)
   - Follow-Ups (attendees / absentees + recording inclusion)
   - Validation and save behaviour (title required)
4. **Scheduled webinar — live**
   - List page (views, columns, filters, Create Webinar)
   - Detail page (header actions, Overview/Timeline, related lists, registration & attendance summary)
   - Send Invite flow: module picker → record picker → selection bar → Mass Email → Select Template
   - Registrants and attendance
5. **Scheduled webinar — on demand** (what differs)
6. **Completed webinar** (what differs)
7. **Completed webinar — on demand** (what differs)
8. **Supporting flows**
   - Email templates: Setup ▸ Templates, the Zoho Webinar module, the 7 defaults
   - Create Email Template → Template Gallery → editor → Save
   - Template type → allowed links → required link (save-time validation)
   - Merge fields (Webinar Details / Users / Organization; Registrations on every post-invite email)
9. **Appendices** — screen inventory · field reference · open questions and assumptions

## STATUS — delivered (2026-09-05)

All flows walked, **57 screens** captured, body written to `body.md` (74,666 chars).

**The PRD lives in Zoho Writer as six sequential documents.** A single document was not
possible through the MCP: `Create_Document` rejects a payload that size
(`MORE_THAN_MAX_LENGTH`, cap sits somewhere above ~15 KB), the server exposes no append,
insert-content or file-upload tool, and `Combine_*` handles PDFs only and needs publicly
reachable URLs. So the body was split at section boundaries and pushed part by part.

| Part | Contents | Writer link |
|---|---|---|
| 1 | Why CRM–Webinar integration; Integration settings (§1–2) | https://writer.zoho.com/writer/open/uksfwd5cb362cbd1545c7aada7351d64b1488 |
| 2 | Create webinar (§3) | https://writer.zoho.com/writer/open/uksfwbe1307b4c9ae4af8921736040ff2bc43 |
| 3 | Scheduled webinar — live (§4) | https://writer.zoho.com/writer/open/uksfw7ac7cb2c6dbd483cad42e3a164c6c367 |
| 4 | On-demand, completed, completed on-demand (§5–7) | https://writer.zoho.com/writer/open/uksfwac5dcfee2698417eb1186be5406a31c1 |
| 5 | Templates, merge fields, registration forms (§8) | https://writer.zoho.com/writer/open/uksfwe198e62ed7724106a18c009477a7b838 |
| 6 | Appendices: screen inventory, field reference, open questions (§9) | https://writer.zoho.com/writer/open/uksfw86dbba14bc7043f5a8b73a35c725d19a |

Part 1 carries the full index across all six parts. Figure placeholders are in place; the
57 images in `screens/` still need inserting (Insert > Image, then Insert > References >
Captions). If a single unified document with one TOC is ever wanted, `File > Import >
From Computer` on `body.md` produces it in one step — Writer maps Markdown headings to
Heading 1/2/3.

## Screens captured in the first pass (13)

| # | File | Screen |
|---|---|---|
| 1 | 01-webinar-list.jpg | Zoho Webinar module list, 6 records, all views |
| 2 | 02-scheduled-live-detail.jpg | Scheduled live webinar detail — header actions + registration summary |
| 3 | 03-send-invite-record-picker.jpg | Send Invite — module dropdown + view dropdown + record table |
| 4 | 04-send-invite-records-selected.jpg | Send Invite — 2 records selected, Remove ALL / Next |
| 5 | 05-mass-email.jpg | Mass Email — To, Select Template, From, warnings, Send Options |
| 6 | 06-select-template.jpg | Select Template — All Templates, search, + Create Template |
| 7 | 07-create-webinar-details-registration.jpg | Create Webinar — Webinar Details + Registration Setup |
| 8 | 08-create-webinar-preferences-reminders-followups.jpg | Create Webinar — Preferences, Reminders, Follow-Ups |
| 9 | 09-marketplace-zoho.jpg | Marketplace ▸ Zoho, Zoho Meetings card, DEMO case switcher |
| 10 | 10-integration-intro.jpg | Integration introduction page, NOT ENABLED |
| 11 | 11-integration-case1-no-account.jpg | Case 1 — Select Organization, no account found |
| 12 | 12-integration-setup-connection-invite-modules.jpg | Setup — Email/Org/Sync + Invite Modules |
| 13 | 13-integration-setup-attribution.jpg | Setup — Deal Attribution, Linear pre-selected |

Still to capture: on-demand + completed detail pages, Templates page and the 7 defaults,
Create Email Template → gallery → editor → required-link error, merge-field panel,
enabled-state integration page, Cases 3–5.

## Field data already extracted

`create-fields.md` — every Create Webinar label, control type, default and picklist values,
parsed from the markup. Needs a pass in the browser to fix two parser artefacts (section
attribution lags one row; the Duration row absorbs nested dropdowns).

---

## Rewritten as a single readable document (2026-09-05, later)

The six-part Writer set was rejected: the user wants **one** document, and the
spec-style original was "nearly impossible for a dev to read and understand".

Reference style supplied by the user: the *Messages Workflow Doc*
(https://writer.zohopublic.in/writer/published/dt5lhf99aa4b27a26476f8efc0986cd06cba0) —
narrative prose that explains the flow, a screenshot directly under the sentence that
describes it, "Sample use case" blocks, a linked table of contents, and almost no tables.

Rewritten to match:

- `prd-source.md` — the narrative source (~7,650 words, a ~30-minute read).
- `build_prd.py` — converts it to a single self-contained HTML, embedding each screenshot
  as base64 and auto-numbering figures.
- `prd.html` — **the deliverable.** 2.6 MB, 49 figures, 12 tables (down from 40+),
  21 callouts. Imports into Writer in one action.
- `screens-web/` — the screenshots re-encoded at 1100px / q45 for embedding (2.3 MB total).

Tables were cut back to the places they genuinely help — the attribution models, the
template-type link rules, the state comparison, and the appendix. Everything else became
prose with a screenshot.

`body.md` is kept as the earlier spec-style version. It is no longer the deliverable.
