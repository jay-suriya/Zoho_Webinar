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
   - **Setup page** after that: Email + Organisation, sync past webinars, **Modules You Can
     Invite**, and **Webinar Deal Attribution** (Linear selected by default).
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

- 2026-09-09 — **Editing a listed default leaves CRM for Zoho Webinar** (branch
  `template-flow-fixes` only). Preview a Default row and hit the pencil and it no longer
  opens CRM's editor: `tplPreviewEdit` checks `zwCanEditElsewhere(_tplPreviewKey)` and, for
  any lifecycle email but the invitation, opens **Zoho Webinar's own template editor in a
  new browser tab** — `window.open` plus `document.write(zwEditorDoc(key))`, so no second
  file or route is needed. The document reproduces the reference: Zoho Meeting's dark header
  ("Enter a template name" over the real subject), the **Registrations** chip,
  Attachments / Cancel / Preview / Save, the **ALL COMPONENTS** rail (TEXT, IMAGE, SPACER,
  IMAGE+TEXT, BUTTON, COLUMNS, TABLE, BACKGROUND) with the HINT at its foot, the rich-text
  toolbar, and the body in `${...}` merge syntax ending in the four-colour bar. Bodies per
  email come from `ZW_EDIT`. **The tab draws its own address bar** showing
  `meeting.zoho.com/meeting/556217208/886748000000019001/settings/templates?step=create&templateName=Default&module=Registrations&selectedTemplate=<key>`
  — a mock cannot occupy that domain, and the point of the screenshot was that the URL is
  visible, so the browser frame is part of the page. The invitation is unaffected: checked
  that its pencil still opens the CRM editor in place and opens no tab. Two things to know:
  the popup needs a real click (a `window.open` from a devtools/eval context can be
  blocked — there is an alert asking for pop-ups if it returns null), and the tab's actual
  location is `about:blank`, so it cannot be screenshotted by the Chrome tooling — verify
  its look by rendering `zwEditorDoc(key)` into a tab instead. Why: the user asked for this
  hand-off, with the screenshot including its address.
- 2026-09-09 — **The listed emails are named "Default", with their real subjects** (branch
  `template-flow-fixes` only). Replaces yesterday's Default chip: the six emails CRM only
  lists are now *named* **Default**, and their subject column carries the subject that
  actually goes out — `Registration Confirmation for ${Campaigns.Title}`, `Reminder to join
  - ${Campaigns.Title}` for all three reminders, `Thank you for attending
  ${Campaigns.Title}`, `We missed you at ${Campaigns.Title}`. The Email Type in the subline
  is what tells six identically-named rows apart. The invitation keeps its own name and its
  pencil — it is the one CRM owns. Consequence that needed handling: `tplPageETypeOf` looks
  the type up from the template *name*, which no longer works for a row named "Default", and
  losing the type would have silently taken the type text, the read-only rule and the
  preview routing with it — so `stampWebinarRowTypes()` sets `row.etype` on each shipped row
  by position instead. Checked: the Attendees row still previews the right body
  (`_tplPreviewKey === 'attendeesFollowup'`) under the title "Default". Why: the user asked
  for the name itself to be Default and gave the four subjects.
- 2026-09-09 — **CRM lists Zoho Webinar's templates; only the invitation is CRM's to edit**
  (branch `template-flow-fixes` only). This is the model the locked Email Type implies, now
  carried into the list. Every lifecycle email except the invitation carries a **Default**
  chip after its name and has **no hover pencil** — it is Zoho Webinar's own template,
  listed here so it can be seen and previewed, not edited from CRM. The invitation keeps its
  pencil and stays the one template CRM owns and customises, which is why it is also the
  only Email Type `+ New Template` offers. **Webinar Cancelled Template is removed from the
  list** — it is not part of what CRM lists; the use case stays in the Email Notifications
  rail, so Preferences still manages it. Clicking any row, Default included, still opens the
  preview (checked: 2nd Reminder Template). The list is 7 rows now. `isWebinarDefault` is
  `module === 'Zoho Webinar' && etype && etype !== 'Invitation'`, so a template someone
  creates for a non-invitation email would also read as Default — not reachable today,
  since the dialog only creates invitations. Why: the user said CRM is just listing Zoho
  Webinar's templates, everything but the invitation is a default, and the cancellation
  email should not be listed.
- 2026-09-09 — **Email Type is locked to Webinar Invitation** (branch `template-flow-fixes`
  only). The field now holds a single option, **Webinar Invitation**, preselected and
  `disabled` with the design's disabled treatment (`#F5F6F8` fill, `#D2D9F1` border,
  not-allowed cursor) and a tooltip pointing at where the other emails are set. The
  reasoning it encodes: the invitation is the one lifecycle email a CRM user sends by hand,
  so it is the only one worth creating from Setup ▸ Templates; the rest are set per webinar
  in Zoho Webinar ▸ Preferences. `_ctUsecase` is pinned to `'sendInvite'` when the dialog
  opens, so `_ctType` / `_tplTypeName` and therefore the required Registration Link and the
  invitation's merge-field set follow from it. The Template Gallery chip now reads whatever
  the Email Type field said (the option's own text, not `TPLPAGE_ETYPE_BY_KEY`), so the
  dialog and the gallery cannot disagree — both say "Webinar Invitation". The other seven
  options are no longer rendered rather than merely hidden; restoring them means putting
  `TPL_USECASES.map` back and dropping the `disabled` flag. The caret is suppressed too
  (`appearance: none`), so the field reads as a stated value rather than a picker that
  refuses to open. Why: the user asked for the type
  to default to Webinar Invitation, not be changeable, and to lose the dropdown symbol.
- 2026-09-09 — **Creation goes through the six Basic layouts, and a list click previews**
  (branch `template-flow-fixes` only). Where branch 1 sends `+ New Template` into the
  use-case gallery, this branch keeps the classic path: Create Email Template (module +
  **Email Type** when the module is Zoho Webinar) → **Next** → the **Template Gallery** with
  its category rail (All / Basic / Celebration / Invitation / Followup / Product Promotion /
  Notification) and **Basic (6)** — Blank, One/Two/Three column, Two column with image 1
  and 2 — headed by the module dropdown reading **Zoho Webinar** with the chosen Email Type
  as the chip beside it (`_ctETypeLabel`, so it shows "2nd Reminder" rather than the
  internal type name). Link and merge-field rules are untouched because they still come
  from `_ctType` → `_tplTypeName`: a 2nd Reminder still refuses to save without a Join URL.
  **Clicking a template in the list opens the preview**, not the create screen —
  `openTemplatePreview(key, displayName)` now takes the row's own name so a custom shows its
  own title, and the panel gained the reference's **Preview / Analytics** tabs alongside the
  folder chip, subject, Mail data with Masking and Desktop/Mobile it already had.
  **A saved template joins the list with its name, its subject and its Email Type** —
  "Day-before nudge · Starting tomorrow: #Webinar Title · 2nd Reminder template" — for both
  the Basic-layout path and a gallery save. Because created templates are listed in their
  own right here, `ucSelect` no longer rewrites rows and the branch-1 helpers that did
  (`ucSyncListRow`, `ucUseCaseRow`, `ucListRowName`, `ucRowEType`, `UC_DEFAULT_ROW_NAME`,
  `UC_ROW_SUBJECT`) were removed: selecting a card changes which template is live, not what
  is listed. Why: the user asked for this creation and preview flow on branch 2 only, with
  the Template Gallery and preview screenshots as reference.
- 2026-09-09 — **The whole template flow ported from branch 1** (branch
  `template-flow-fixes`). 26 of the 39 diff hunks between the two files were taken from
  `templates-flow`; 13 were held back. **Taken:** the editor header's name/subject as real
  blank inputs (`tplSetHeader` / `tplHeaderName` / `tplHeaderSubject`) with the body prompt
  as a CSS placeholder; Create Email Template asking module first with an **Email Type** row
  that appears only for Zoho Webinar and carries the choice into the gallery
  (`ctModuleChanged`, `_ctUsecase`, `ctNext`); the Email Notifications header's standing
  intro line with the duplicated chip and type text gone; the Default card offered under
  Custom Templates as well as Quick; Setup ▸ Templates listing the eight lifecycle emails
  with **Webinar Cancelled last**, the email type as text on the row's subline rather than a
  column, the hover pencil before it, a name click opening that email's gallery, and
  `ucSyncListRow` keeping one row per email so selecting a custom renames that row instead
  of adding another. **Held back, deliberately:** Preferences ▸ Customise Template still
  opens the gallery (branch 1 opens a preview) — this branch's whole premise; the Send
  Invite picker still reads `TPL_UC_STATE.sendInvite` with its "In use" chip rather than the
  Setup ▸ Templates rows, per the user's original split; and the branch-1-only asks that
  were never meant for here — the intro page's "Setup" CTA and enabled badge, Case 2 as the
  demo default, and the Webinar Timezone label and row. Note the one design reversal: the
  comment saying the lifecycle emails are *not* listed under Setup ▸ Templates is no longer
  true — they are listed there now, in addition to living in Preferences, so this branch is
  a superset rather than the either/or it started as. Why: the user asked for the template
  flow on branch 2 as well.
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
  (both branches now), on the setup page, the enabled page and the two code comments that
  named it. The old name described the data structure; the new one describes the decision —
  who is in the room, and that they come from CRM. Subline: "Choose which CRM modules your
  participants can come from. Turn a module off and its records can no longer be added to
  a webinar." The word "invite" is deliberately absent from both, at the user's
  instruction. Worth knowing if you touch this copy: mechanically the setting gates who
  can be *invited*, not who can *attend* — anyone with the public registration link can
  still join — so "participate" reads as intent rather than a literal description of the
  toggle. Why: the user picked the name from a slate, then asked for the subline without
  "invite", then asked for both on this branch too.
- 2026-09-07 — **"Zoho Webinar Invite Modules" renamed to "Modules You Can Invite"**
  (both branches), on the setup page and the enabled page, plus the two code comments that
  named it. The old label repeated the product name on a page you can only reach inside
  the Zoho Webinar integration, and "Invite Modules" read as a category rather than a
  choice — it could as easily have meant modules belonging to invites. The subline changed
  from restating the heading to naming the consequence: "Records from these modules can be
  invited to a webinar. Turn one off and it disappears from the module list in Send
  Invite." Why: the user asked for a better name and picked this one from a slate.
- 2026-09-07 — **Save Template asks which folder** (both branches). The dialog said
  "Saved to <module> Templates" — a statement, not a choice. It now has Template Name plus
  a **Save To** dropdown listing the CRM template folders (`TPLPAGE_CATEGORIES.slice(5)` —
  the first five entries are views, not folders), each with the shared-folder icon where
  it applies, and a separated **+ New Folder** row that takes a name inline and selects
  it. A folder is required: saving without one is refused with the field outlined and an
  inline message, matching the name guard. The chosen folder is stored on the template and
  is what the Send Invite picker's second column shows, so `TPL_FOLDER` is now only a
  fallback for the shipped defaults. Why: the user supplied the real dialog as reference.
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
