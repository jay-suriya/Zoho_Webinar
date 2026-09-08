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
2. **Who Can Participate From CRM**: the list of CRM modules a webinar invite may be sent to. It drives
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
| Who Can Participate From CRM | Integration | Which modules a webinar invite can be sent to |
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

- 2026-09-08 — **The gallery is the Zoho Webinar path only; other modules keep the module
  picker** (branch `templates-flow`). Sending every `+ New Template` to the gallery removed
  the module picker altogether, so an ordinary CRM template — Contacts, Potentials — could
  no longer be created. `tplPageNewTemplate` now branches: filter on **Zoho Webinar** opens
  the Email Notification gallery, anything else (including All Modules, which hasn't named
  a module yet) opens the Create Email Template dialog as before. The dialog also stopped
  offering **Zoho Webinar** as a module, and `openCreateTemplateModal` no longer defaults
  to it — otherwise there were two different UIs for creating the same webinar template.
  Why: the user pointed out the missing module picker.
- 2026-09-08 — **Creating a template now starts from the Email Notification gallery**
  (branch `templates-flow`). `+ New Template` opened a Create Email Template dialog asking
  for module + Email Type, then the six Basic layouts. It now opens branch 2's use-case
  gallery — the rail of 8 lifecycle emails, each with its Default (Quick), its Customs and
  the Basic layouts — ported over along with the `cancellation` type it needs. The rail
  picks the use case, which stamps the type, so the module + type dialog is out of this
  path (`openCreateTemplateModal` remains for the create-webinar slot and Send Invite
  entries). **Only creation changed.** Editing is untouched: click a template in the list →
  preview → pencil → editor, no gallery involved. Merge fields, allowed links and required
  links are unchanged because they were always driven by `_tplTypeName`, which the gallery
  sets exactly as the old dialog did. The list view keeps its Email Type column, and a
  template created in the gallery now carries `row.etype` so its chip and the column's
  filter are right — a custom name like "Day-before nudge" cannot be looked up through
  `TPL_KEY_BY_NAME`. Two adaptations were needed on the way in: the ported functions wrote
  the editor's name/subject with `.textContent`, which does nothing on this branch's input
  fields, so they go through `tplSetHeader` now; and this branch's name-required plus
  Save To folder rules apply to gallery saves rather than branch 2's auto-suggested name.
  Why: the user asked for branch 2's creation flow, with everything else left alone.
- 2026-09-08 — **"Sync past webinars" now appears on the enabled page too** (both
  branches). It never had it: `postRenderSyncPastData` looks for `post-sync-yes-state`
  and siblings, and that markup has never existed — not on `master`, not at the branch
  point — so the function was a permanent no-op and the field was simply absent after
  enabling. Added as a row in the enabled page's connection block with the same Yes/No
  radios as the setup page; `setupActivateIntegration` carries the setup answer across,
  and `postSyncPastSet` updates `_syncPast` / `_syncImportScope` and marks the page dirty.
  `postRenderSyncPastData` is still dead code — it wants a richer imported-count display
  that has no markup; left alone rather than half-wired.
  Why: the user reported the field missing after Enable Integration.
- 2026-09-08 — **Only person-shaped modules are listed** (both branches). After the locked
  Leads and Contacts, the picker held Accounts, Potentials, Cases, Campaigns and Meetings
  — a company, a deal, a ticket, a campaign, an event. None is a person, so none can
  participate, which is the only question this section asks. They are replaced by the
  modules a business builds to hold people, named for who they hold: Vendors, Donors,
  Volunteers, Members, Students, Alumni, Partners, Speakers, Referrals, Patients,
  Subscribers. Placeholder names went too. Side effect worth knowing: the React
  `INVITE_MODULES` for Send Invite is still `["Leads","Contacts","Vendors","Custom Module
  1"]`, and `inviteModulesEnabled()` intersects it with this list — so Custom Module 1 can
  no longer be switched on, and the Send Invite dropdown offers Leads and Contacts until
  Vendors is turned on. Why: the user asked for individuals only.
- 2026-09-08 — **"Sync past webinars?" is a Yes/No radio pair, not a dropdown** (both
  branches). A picklist for a binary question hid one of the two answers behind a click.
  The radios are the control now, with **Yes** preselected; a hidden input keeps the id
  `setup-sync-past-select` and its `yes`/`no` value so the three existing read/write sites
  need no change, and `setupSyncPastSet()` keeps radios and hidden value in step when the
  answer is set programmatically. Note: this field was never removed — it only *looked*
  removed in verification screenshots, because forcing the integration panel visible
  squashes that row into a ~116px column where the dropdown collapses to a sliver. Give
  the panel real width before judging that section by screenshot.
  Why: the user asked for radios.
- 2026-09-08 — **Who Can Participate From CRM is now the standard CRM module picker**
  (both branches). The chips + search + grouped-grid picker is replaced by the reference
  pattern: one card, a Search field, a flat scrollable checkbox list. Heading and subline
  kept, everything below them new. **Leads and Contacts are mandatory** — checked, red
  asterisk, muted label, no hover or pointer, and `imToggle()` returns early for anything
  in `IM_LOCKED`, so they cannot be turned off. Everything else starts unchecked, so
  `INVITE_ENABLED_MODULES` defaults to just those two and the Send Invite module dropdown
  narrows to match. Gone with the old UI: "Select all", "Clear", the selected-count chips,
  the "modules without an email field" footnote, plus `IM_GROUPS` and `imSelectAll`.
  Why: the user supplied the reference and asked for the two locked modules.
- 2026-09-08 — **"Modules You Can Invite" renamed to "Who Can Participate From CRM"**
  (branch `templates-flow`), on the setup page, the enabled page and the two code comments
  that named it. The old name described the data structure; the new one describes the
  decision — who is in the room, and that they come from CRM. The heading and subline
  swapped jobs: the heading carries the intent, the subline the mechanism — "Choose which
  CRM modules your participants can come from. Turn a module off and its records can no
  longer be added to a webinar." The word "invite" is deliberately absent from both, at
  the user's instruction. Worth knowing if you touch this copy: mechanically the setting
  gates who can be *invited*, not who can *attend* — anyone with the public registration
  link can still join — so "participate" here reads as intent rather than a literal
  description of what the toggle controls. Why: the user picked the name from a slate and
  then asked for the subline without "invite".
- 2026-09-08 — **Integration intro page: the action is "Setup", and Case 2 is the demo
  default** (branch `templates-flow`). The introduction page's top-right action said
  "Enable Integration", but it doesn't enable anything — it opens the setup form, and
  enabling happens on the button at the end of that form. It now reads **Setup** in both
  states: before setup it opens the form, after setup it opens the enabled settings panel.
  A `window._webinarIntegEnabled` flag set by `setupActivateIntegration()` drives that,
  and also flips the badge from "NOT ENABLED" to a green **ENABLED** so the page stops
  contradicting itself when you come back to it from Marketplace. Separately,
  `window._selectedCase` now defaults to **2 (single org)** with the demo switcher
  preselected to match — case 2 goes straight to the setup page, so the walkthrough
  doesn't detour through the create-account modal. Why: the user asked for both.
- 2026-09-08 — **Templates list: an Email Type column, only under Zoho Webinar**
  (branch `templates-flow`). A new column between Template Name and Modified By showing
  each lifecycle email's type as a chip, with a caret on the header that opens a filter —
  All email types, Invitation, Confirmation, 1st/2nd/3rd Reminder, Attendees Follow-up,
  Absentees Follow-up. It appears only while the Zoho Webinar module is selected, since
  those are the only templates that carry a type, and switching module hides it and clears
  the filter. The header label becomes the chosen type in pink so an active filter is
  visible, the empty state reads "No <type> templates yet.", and its colspan widens with
  the column. Types come from `TPL_KEY_BY_NAME` → `TPLPAGE_ETYPE_BY_KEY`, so the column
  cannot drift from the type each template actually has.
  Why: the user asked for a filterable Email Type column scoped to Zoho Webinar.
- 2026-09-08 — **Create Webinar: the timezone picklist got a label and its own row**
  (branch `templates-flow`). It was stacked under the date+time box inside the same
  `.form-group`, so it had no label at all and the "Webinar Date & Time" label floated
  vertically centred between the two controls. The timezone is now a **Webinar Timezone**
  row of its own directly below, with an empty right-hand `.form-group` so the label
  column keeps the width every other row uses — labels right-align together, both fields
  share one left edge, and row spacing is the standard 14px again.
  Why: the user pointed out the unlabelled picklist and the spacing.
- 2026-09-07 — **Create Email Template: "Template Type" is now "Email Type", and "None"
  is gone** (branch `templates-flow`). The field names which lifecycle email the template
  is, so "Email Type" says it directly; "Template Type" restated the noun already in the
  dialog title. Dropping None means every template created here is one of the seven
  webinar emails and always carries a required link — nothing can be saved as an untyped
  template from this dialog any more. `TPL_TYPE_LINKS['None']` is left in place as a
  harmless fallback, since it is no longer reachable from the UI.
  Why: the user asked for both.
- 2026-09-07 — **"Zoho Webinar Invite Modules" renamed to "Modules You Can Invite"**
  (both branches), on the setup page and the enabled page, plus the two code comments that
  named it. The old label repeated the product name on a page you can only reach inside
  the Zoho Webinar integration, and "Invite Modules" read as a category rather than a
  choice. The subline changed from restating the heading to naming the consequence:
  "Records from these modules can be invited to a webinar. Turn one off and it disappears
  from the module list in Send Invite." Why: the user asked for a better name and picked
  this one from a slate.
- 2026-09-07 — **Save Template asks which folder** (both branches). The dialog said
  "Saved to <module> Templates" — a statement, not a choice. It now has Template Name plus
  a **Save To** dropdown listing the CRM template folders (`TPLPAGE_CATEGORIES.slice(5)` —
  the first five entries are views, not folders), each with the shared-folder icon where
  it applies, and a separated **+ New Folder** row that takes a name inline and selects
  it. A folder is required: saving without one is refused with the field outlined and an
  inline message, matching the name guard. The chosen folder is stored on the template
  (and on its Templates-list row) and is what the Send Invite picker's second column
  shows, so `TPL_FOLDER` is now only a fallback for the shipped defaults.
  Why: the user supplied the real dialog as reference.
- 2026-09-06 — **Send Invite picker's second column is the template folder.** It was
  printing the module ("Zoho Webinar", "Leads Templates"); in CRM's Select Template that
  column is the folder the template sits in — Public Email Templates, Managerial
  templates, Zoho Sign. Every row in this picker is a webinar invitation template
  already, so the module said nothing. Same change on `template-flow-fixes`, where rows
  read "Zoho Webinar · Send Invite". Why: the user pointed at the real dialog.
- 2026-09-06 — **A template you create now always shows in Send Invite** (branch
  `templates-flow`). The picker filtered `MODULE_TEMPLATES` to `t.module === module`, so a
  template saved under Zoho Webinar — or under any module other than the one being
  invited — was dropped with no explanation. It now lists every created template, all
  plainly selectable. (A first pass dimmed non-matching modules behind a "<Module> only"
  chip, on the merge-fields-resolve-against-the-module rule; the user asked for it gone —
  it was solving an edge case they had not raised and was the only thing on the row that
  is not in the reference dialog.) Why: the user created a template and could not find it
  in the picker.
- 2026-09-06 — **New templates start blank and actually land in the list** (branch
  `templates-flow`). Creating from Setup ▸ Templates used to open the editor with the
  template *type* as the name and "One column · Leads" as the subtitle, then prefill the
  Save dialog with "Webinar Invite - <module>" — three defaults the user never chose. The
  header's name and subject are now real inputs (`tplSetHeader` / `tplHeaderName` /
  `tplHeaderSubject`), blank for a new template with "Untitled template" and "Add a
  subject" placeholders, and the Save dialog carries whatever was typed instead of
  inventing a name. Saving with no name is refused inline in the dialog (the editor's
  toast sits behind that modal's scrim, so the error had to live in the dialog). Saving
  now also pushes a row into `TPLPAGE_CREATED`, concatenated ahead of `TPLPAGE_ROWS` in
  `tplPageRows()`, so the template appears at the top of Setup ▸ Templates with its module
  and subject — previously it only went into `MODULE_TEMPLATES` and vanished. The body's
  "Write the … email here" prompt became a real CSS placeholder (`:empty:before`) rather
  than grey content that typing merged into and that saved into the email.
  Why: the user asked for an empty, typable name and subject, and for the save to show up.
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
