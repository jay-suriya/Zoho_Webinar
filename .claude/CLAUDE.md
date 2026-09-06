# Product Knowledge: Zoho CRM ⇌ Zoho Webinar Integration

This file gives Claude the product context needed to work on this codebase. It is
knowledge, not engineering convention — see `.claude/rules/design-rules.md` for the
Zoho CRM design tokens every screen must follow.

## What this product is

A Zoho Webinar experience embedded inside Zoho CRM, letting a CRM user create a webinar,
invite the CRM records they already work with, and read registration, attendance and
revenue impact back on the record — without leaving CRM. The whole product is one static
mock: `webinar.html` (~1.4 MB, single file, no build step). Most pages are hand-written
HTML + vanilla JS; the webinar list and webinar detail pages are React (compiled
`React.createElement` calls, no JSX, no bundler), so edits there are made against the
compiled form.

## Company context

Zoho sells a suite of apps that talk to each other (CRM, Webinar, Survey, Campaigns,
Books, Desk…). The bet behind this project is the cross-product story: instead of running
a webinar in one tool, exporting registrants, and re-importing them into the CRM, the two
apps share data directly. Zoho Webinar's own feature set already exists — the job here is
re-flowing those features so they work naturally *from inside* Zoho CRM.

## Primary persona

**Jay — Sales Rep / Account Executive**, who is also the CRM admin for this integration.
- Lives in Zoho CRM; has never used standalone Zoho Webinar and doesn't want to learn it
  as a separate product.
- **Creates** a webinar from the CRM module, **invites** Leads/Contacts/custom-module
  records he already works with, and **reads results** (registrations, attendance,
  no-shows, influenced revenue) on the record and in reporting.
- Comfortable with CRM concepts (modules, records, fields, templates, workflows); no
  interest in webinar-specific jargon beyond what he needs.
- Frustration trigger: any step that feels like operating a second product.
- He also configures the integration (Marketplace → Zoho → Zoho Webinar), so admin
  screens are designed for the same person.

## Zoho CRM concepts used here

- **Module**: an object type — standard (Leads, Contacts, Accounts, Potentials, Vendors)
  or custom. Zoho Webinar is itself a module once the integration is enabled.
- **Record / Layout / Field**: as in CRM. Invites are sent to records of a module.
- **Email Template**: templates are *module-scoped* — their merge fields resolve against
  that module's record, so a template's module must match the recipient's module.
- **Setup**: Settings → Setup Home → Customization ▸ Templates, Modules and Fields,
  Marketplace ▸ Zoho, etc.
- **Mass Email**: the compose step used when sending an invite to many records.

## Zoho Webinar concepts used here

- **Webinar**: title, date/time, duration, organiser, type (Live / On-Demand /
  Recurrent), registration setup, preferences, reminders, follow-ups.
- **Registration Form**: what a registrant fills in; can push registrants into CRM.
- **Registrant / Attendee / Absentee**: a registrant is created on sign-up; after the
  session they are an attendee or an absentee, which decides which follow-up they get.
- **Lifecycle emails**: Invitation → Confirmation → 1st/2nd/3rd Reminder → Attendees
  Follow-up / Absentees Follow-up (plus a cancellation email).

## How the two connect (the actual integration surface)

1. **Marketplace → Zoho → Zoho Webinar**
   - **Introduction page first** (what the integration makes possible: hero, How it
     works, Why teams enable it, what enabling does) with **Enable Integration** at the
     top right.
   - **Setup page** after that: Email + Organisation, sync past webinars, **Zoho Webinar
     Invite Modules**, and **Webinar Deal Attribution** (Linear selected by default).
   - **Enabled page**: the same connection details, invite modules and attribution, with
     a dirty-state Save bar.
2. **Invite Modules**: the list of CRM modules a webinar invite may be sent to. It drives
   the module picker in Send Invite — turn a module off here and it disappears there.
3. **Send Invite** (from a scheduled webinar): record picker (module dropdown → records)
   → Next → **Mass Email**, whose Invitation Template is chosen through **Select
   Template**.
4. **Templates**: the webinar's default set lives in **Modules and Fields ▸ Zoho Webinar
   ▸ Preferences**; Setup ▸ Templates lists them under the **Zoho Webinar** module.
   Creating one goes Create Email Template (module + type) → **Template Gallery** (Basic
   layouts) → editor → Save.
5. **Template types** decide what a template may link to, and what it must carry:

   | Type | May link to | Must contain |
   |---|---|---|
   | Webinar Invitation | Web URL, Email, Registration Link, all Add To Calendar | Registration Link |
   | Confirmation Email | Web URL, Join URL, Cancel Registration, calendars | Join URL |
   | 1st / 2nd / 3rd Reminder | Web URL, Join URL, Cancel Registration, calendars | Join URL |
   | Attendees / Absentees Follow-up | Web URL, Join URL, Recording Link, calendars | Recording Link |
   | None | all of the above | nothing |

6. **Merge fields** (`#` in the editor): **Webinar Details, Users, Organization** on the
   invitation; every later email adds **Registrations** above Webinar Details, because it
   goes to a registrant rather than a CRM record.
7. **Attribution**: webinar attendance is tied to the deals it influenced — First / Last
   Interaction, Linear (default), Increasing / Decreasing Time Decay, Position-Based.

## Terminology quick-reference

| Term | Belongs to | Meaning |
|---|---|---|
| Module | CRM | Object type (Leads, Contacts, custom, Zoho Webinar) |
| Invite Modules | Integration | Which modules a webinar invite can be sent to |
| Registrant | Webinar | Someone who signed up; becomes attendee or absentee |
| Template Type | Integration | Which lifecycle email a template is for |
| Join URL / Registration Link / Recording Link | Webinar | Per-registrant links a template can carry |
| Attribution Model | Integration | How deal revenue is split across webinars |

## Working agreement

- After every meaningful edit, open/refresh the mock in the browser (claude-in-chrome)
  at `http://localhost:8090/webinar.html` so the change can be seen live. Serve it with
  `python3 -m http.server 8090` from this folder. **Cache-bust the URL** (`?v=2`) —
  `http.server` sends no cache headers and Chrome will happily serve a stale copy.
- Every edit to `webinar.html` gets committed, and the Mock Edit Log below gets an entry
  in the same commit saying what changed and why.
- **Push after every commit** — `git push` to `origin` (github.com/jay-suriya/Zoho_Webinar,
  private) as soon as the commit is made, so GitHub always matches the working copy. This
  applies to any file in the repo, not just the mock: `.claude/`, skills, docs. If a push
  fails or is rejected, say so rather than silently leaving commits local.
- Work happens on a branch (currently `templates-flow`); `master` is the pre-session
  baseline.
- The React portions are compiled `React.createElement` code: keep parentheses balanced,
  and re-check the page after every structural edit — an unbalanced paren blanks the
  whole detail page.

## Mock Edit Log

Reverse-chronological. Each entry: date, one-line summary, why.

- 2026-09-06 — **Send Invite's Select Template now has a real source, different per
  branch.** It used to be a hardcoded `[{name:'Webinar Invitation Template'}]` in
  `SelectTemplateModal`, which is why a template created anywhere never showed up in it.
  On `template-flow-fixes` it reads `TPL_UC_STATE.sendInvite` — the module's Send Invite
  Default (Quick) card plus the customs saved under it, marking the one Preferences has
  live as **In use**; a template created from the
  picker now lands in those customs too, so the two screens cannot disagree. On
  `templates-flow` it instead derives from Setup ▸ Templates: the Zoho Webinar rows whose
  type is invitation, plus anything created there (`WEBINAR_CREATED`) and the module
  templates saved for the records being invited (`MODULE_TEMPLATES`), de-duplicated.
  Why: the user wanted the two branches to demo the two sources of truth side by side.
- 2026-09-06 — **Webinar emails moved to the module** (branch `template-flow-fixes`): the
  lifecycle set no longer lives in Setup ▸ Templates — Zoho Webinar is gone from that
  page's module filter and its seven rows are removed, so the Preferences line "managed
  here, not under Setup › Templates" is finally true. All 8 rows in **Modules and Fields ▸
  Zoho Webinar ▸ Preferences** now open a new full-screen **Email Notification gallery**
  (`#tpl-uc-gallery`): a left rail of the 8 use cases, and per use case **Quick Templates**
  (the shipped Default), **Custom Templates** (what's saved under it) and **Basic** (the 6
  layouts). Clicking a Default/Custom card makes it live immediately; a Basic layout opens
  the editor stamped with that use case's type, so the allowed link types and merge-field
  categories are the ones that use case permits — Send Invite keeps Registration Link and
  no Registrations fields, everything after it gets Join URL / Recording Link plus
  Registrations. Also: the cancellation email became a real type (`cancellation`, renamed
  from "Meetings Cancelled" to "Webinar Cancelled", carrying no webinar links since the
  session is off), the Basic layouts now seed real starter content instead of a blank box,
  and saving refuses a name already used under that use case. Why: the user wanted the
  standalone Zoho Webinar chooser (three reference screenshots) to be the one place these
  emails are managed, instead of the Setup ▸ Templates list.
- 2026-09-05 — Added `.claude/` (this file + the CRM design rules) so the webinar mock
  carries its own product context, matching the Zoho Survey repo.
- 2026-09-04 — **Integration flow rebuilt**: choosing Zoho Webinar now opens an
  **introduction panel** (hero, How it works, Why teams enable it, what enabling does)
  with Enable Integration top-right; the setup page that follows is Email + Organisation
  → **Zoho Webinar Invite Modules** → **Webinar Deal Attribution with Linear
  pre-selected**. Invite Modules is a chips + search + grouped-list picker (not the wall
  of checkboxes the Survey integration uses) and feeds the Send Invite module dropdown.
  Panels were made full-width with capped content so the scrollbar sits at the window
  edge instead of mid-page. Why: the user wanted the integration to introduce itself
  before asking for anything, and the module choice to live with the rest of the config.
- 2026-09-04 — **Template system**: Setup ▸ Templates lists the whole Zoho Webinar
  default set; Create Email Template asks module + type (None, Webinar Invitation,
  Confirmation Email, 1st–3rd Reminder, Attendees/Absentees Follow-up) then opens the
  **Template Gallery** (Basic layouts only); from a create-webinar step or Send Invite the
  dialog is skipped because the step already implies the type. Saving names the template
  after its type, returns to the list it came from ("Refresh to see the changes"), and
  refuses if the template is missing the link its type depends on. Insert Link / Insert
  Button offer only that type's links; merge fields are Webinar Details, Users,
  Organization, plus Registrations on every email after the invite.
- 2026-09-03 — **Send Invite**: module chooser step removed — the record picker opens
  directly with a module dropdown before the view filter. Mass Email lost the "Sent later,
  automatically" section and uses a Select Template button with the chosen template as a
  preview link.
- 2026-09-01 — Branch `templates-flow` created from `master` for all of the above.
