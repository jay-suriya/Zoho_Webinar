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

- 2026-09-15 — **Co-Organizer is now a plain copy of Organizer.** Same `.cs-btn` shell,
  same 160x32 box, the same `.co-search` box inside the dropdown and the same `csSelect`
  behaviour — the only differences are the default value (**None**) and the extra None
  option. Everything built for it over the previous four turns is deleted: the chips, the
  multi-select, the CRM / Zoho Webinar source switch, the invite-by-email row, the Manage
  label, the modal, and all the `.coorg-*` CSS and `coOrg*` functions except `coOrgFilter`,
  which Webinar Owner and Organizer share. `coOrgGroup` / `coOrgGroup2` remain, since those
  ids are how the live and on-demand variants are swapped. Verified the two fields now
  report identical shape — class, width, height, search present — and that search narrows to
  Morrison Troy and picking writes the value and closes. **Worth reading before changing
  this field again:** the brief was "a picklist with search, like Organizer" and it took
  four rounds — a tabbed dropdown, then a modal, then a box, then this — because each
  instruction was treated as an addition rather than as a correction of the previous
  reading. When a request names an existing control to copy, copy it and stop.
  Why: the user asked for an exact replica of the Organizer field.
- 2026-09-15 — **Co-Organizer is an inline dropdown with search, not a modal.** I had built
  the Add Co-organisers panel as a dialog; the ask was a dropdown like Organizer's, so the
  modal is gone and the field opens its own `.cs-dd` in place. Inside: a **CRM / Zoho
  Webinar** source picklist and a **search** on one row, the people below as checkbox rows
  showing name and email, and an **Invite by email address** row (Name + Email + Invite) at
  the foot. It is multi-select, so there is no OK to press — toggling a row updates the box
  immediately, the way a picklist shows its value: "Jayasuriya, Morrison Troy", then
  "+2" past two with the full list on the `title`. An invited address belongs to neither
  directory, so it is appended to whichever list is showing rather than disappearing once
  added. Everything inside the dropdown stops propagation, or the first click or keystroke
  closes it. Removed with the modal: `coOrgOpen`, `coOrgDone`, `coOrgModal` and its markup.
  Checked: search narrows to Morrison Troy, two picks from CRM plus one from Zoho Webinar
  plus one email invite reads "Jayasuriya, Morrison Troy +2", and an invite without a name
  is still refused. Why: the user clarified they wanted a dropdown with search, like the
  Organizer field.
- 2026-09-15 — **Co-Organizer looks like Organizer again.** The blue "+ Add co-organisers"
  link stood out against a form of picklists, so the field is a box using the same `.cs-btn`
  shell — same border, height, 160px min-width and caret as Organizer — that opens the Add
  Co-organisers panel instead of an inline list. It shows its value the way a picklist does:
  **Add co-organisers** in placeholder grey when empty, the names when not, and
  "Jayasuriya, Morrison Troy +2" past two, with the full list on the `title` so nothing is
  lost. The chips stayed but are hidden — they remain the store the panel reads on reopen and
  writes on Done, which keeps the panel as the only place selection is edited. Checked:
  empty state, two names, four names collapsing to +2, and clearing back to the placeholder.
  Div depth over the row re-checked at 0 before looking at anything. Why: the user asked for
  it to be similar to the Organizer field.
- 2026-09-14 — **Fixed the layout the co-organiser field broke.** Swapping the picklist for
  the chips-and-action markup left **one `</div>` too many** in each of the two fields. The
  stray close ended `#repeatRow` early, so `coOrgGroup2` and every row after it fell out of
  their row: the form rendered a **519px hole** between Repeat Webinar and Webinar Cost, and
  `repeatRow` held 2 children instead of 3. Removing one close from each field restored it —
  rows now run 349 → 394 → 440 contiguously and `repeatRow` has all three groups.
  **How to catch this quickly:** walking `<div>`/`</div>` with a running depth over the
  affected block prints exactly where depth crosses zero, which named the culprit in one
  pass after eyeballing the markup twice had missed it. An unbalanced div does not throw —
  it silently reparents everything after it, so check depth after any markup swap, and
  compare `.getBoundingClientRect().top` of consecutive rows for gaps. Same failure mode as
  the blank intro page earlier this session. Why: the user reported the layout breaking.
- 2026-09-14 — **Co-organisers move into a panel; the action becomes Manage.** The inline
  dropdown is replaced by an **Add Co-organisers** dialog: a source picklist reading **CRM /
  Zoho Webinar** (renamed from "CRM Users / Webinar Users"), a search, a checkbox list of
  people showing name and email, an **Invite by email address** row, and a **Selected (n)**
  strip of chips, with Cancel and **Done**. Done writes the chips onto the field and flips
  its action from **+ Add co-organisers** to **Manage co-organisers**, because once somebody
  is on it there is something to manage rather than add; removing the last chip flips it
  back. The panel is shared by both fields — `_coOrgField` remembers which one opened it —
  and the selection is only committed on Done, so Cancel genuinely discards. **Invite by
  email takes a name as well as an address**, which is the "best UI" part: a bare address is
  not recognisable in a chip list six weeks later, so an invite without a name is refused
  with "Enter a name, so the co-organiser is recognisable later", the address is validated,
  and the chip shows the name with the address and "invited" underneath it. Removed with the
  old dropdown: `coOrgTab`, `coOrgPick`, `coOrgAdd`, `.co-dd`, `.co-tabs`, `.co-list`,
  `.co-addbox`. **Careful:** `coOrgFilter` was deleted with that block and had to be put
  back, because Webinar Owner and Organizer still use it for their own search — check those
  two whenever co-organiser code is touched. Verified end to end: picking two from CRM, one
  from Zoho Webinar and one email invite gives four chips, the trigger reads "Manage
  co-organisers", and the panel closes. **Built from the description, not the screenshots** —
  both references were drag-temp files macOS had already deleted. Why: the user asked for
  this panel, the Manage label, the CRM / Zoho Webinar naming and a name on email invites.
- 2026-09-14 — **Co-Organizer is an add action, not a picklist box.** The field no longer
  renders a `.cs-btn` reading "None". It shows **+ Add co-organisers**, and each pick becomes
  a removable chip above the action, which stays put so more can be added — a webinar can
  have several, which the old single-value box could not express. `None` left the CRM list
  (meaningless once the field holds chips) and the options call `coOrgPick` instead of
  `csSelect`, since selecting must append rather than overwrite a button label. Both fields
  updated, live and on-demand. **The inline add replaced `window.prompt`**: a prompt blocks
  the whole renderer until dismissed, the same trap that froze a tab earlier in this session,
  so + Add New Co-Organiser now swaps the footer for a text field with Add / Cancel, and
  Enter and Escape work. Verified: picking one from each directory gives chips Jayasuriya
  and Suriya, the trigger still reads "+ Add co-organisers", an inline add appends
  priya@northline.com, and the chip × removes just that one. Why: the user asked for
  "+ Add co-organisers" in place of the picklist box.
- 2026-09-14 — **On-demand: Allow video play/pause moves under Video File.** It had a row of
  its own below Webinar Owner / Organizer, so the on-demand form read Video File, then
  Organizer, then the toggle — the setting sat two rows away from the file it governs. It
  now occupies the empty right-hand cell of the **Webinar Timezone** row, which puts the
  right column in the order the setting belongs in: **Video File → Allow video play/pause →
  Organizer**. The standalone `playPauseRow` is gone and `playPauseGroup` carries its own
  visibility, so `onWebinarTypeChange` toggles one element instead of two. Live is unchanged
  — checked both: live reads Date & Time | Duration, Timezone, Owner | Organizer, Repeat |
  Co-Organizer; on-demand reads Date & Time | Video File, Timezone | Allow video play/pause,
  Owner | Organizer. Why: the user asked for that position.
- 2026-09-14 — **Webinar Owner and Organizer get a search box too** — search only, no tabs
  and no add action, since those two pick from one directory. `coOrgFilter` was written for
  the tabbed co-organiser list, so it now resolves its dropdown with `closest('.cs-dd')` and
  falls back to the dropdown itself when there is no `.co-list`, which makes it work for any
  plain picklist. The search row is sticky at the top of the dropdown, and
  `.cs-dd:has(.co-search)` sets `min-width:230px` — without it the Owner dropdown inherits
  the narrow width of its button and the search field is clipped to "Search u…". Checked:
  "ma" narrows Owner to Mark Acme, an unmatched term shows the empty state, and selecting
  still writes the name back to the field. Why: the user asked for search on those two.
- 2026-09-14 — **Co-Organizer picker gains a search box.** Sits under the tabs, filters the
  directory that is showing, and shows **No users found** when nothing matches. Switching
  tabs clears it, since the search belongs to whichever directory is open, and adding a name
  clears it too so the new entry is not hidden by a filter that no longer matches it. The
  input stops click and keydown from propagating — without that, typing in it reaches the
  `.cs-btn` behind and closes the dropdown. Checked: "mor" narrows CRM Users to Morrison
  Troy, "zzz" empties the list and shows the empty state, switching to Webinar Users resets
  the box and shows Suriya / Mark Acme. Why: the user pointed out there was no search.
- 2026-09-14 — **Co-Organizer is a two-source picker with an add action.** It was a flat
  picklist of three names. It now opens a dropdown with **CRM Users / Webinar Users** tabs —
  a co-organiser can be either, and the two directories are not the same people — and a
  **+ Add New Co-Organiser** action pinned under the list, which prompts for a name or email,
  appends it to whichever tab is showing and selects it. Both copies of the field are
  updated: `coOrgGroup` (live) and `coOrgGroup2` (on-demand). Two things this needed:
  `coOrgTab` calls `stopPropagation`, or the click bubbles to the `.cs-btn` above and closes
  the dropdown as you switch tabs; and `csSelect` now finds its dropdown with
  `opt.closest('.cs-dd')` rather than `opt.parentElement`, because options now sit one level
  deeper inside `.co-list` — without that, selecting a name would not write it back to the
  button. Verified: tabs read CRM Users / Webinar Users, CRM holds None / Jayasuriya /
  Morrison Troy / Rao Priya, Webinar holds Suriya / Mark Acme, switching swaps the list, and
  picking from the second tab writes "Suriya" to the field and closes the dropdown.
  **Built from a description, not the screenshot** — the reference was a drag-temp file that
  macOS had already deleted, so the layout is my reading of "toggle options CRM users and
  webinar users, and at the bottom add new co-organiser". Why: the user asked for it.
- 2026-09-14 — **Sending an invite creates an Email source-tracking link.** Completing Send
  Invite now adds an **Email** row to the list in **View Registration Link** and switches
  **Enable Source Tracking** on, so the channel CRM invites arrive through is tracked the
  same way a LinkedIn or Twitter link would be. `RegistrationLinkModal` had `sources` as
  local state starting `[]`, so anything created died when the modal closed; it now takes
  `initialSources` and seeds both the list and the tracking toggle from it, while
  `WebinarDetailApp` owns `linkSources` and `handleSent` appends the Email entry (guarded
  against duplicates on a second send). Checked end to end in Chrome: before sending, the
  modal shows the default link with tracking off and no table; after sending, tracking is on
  and the table holds one row — Email, created by Jay, 0 visited, 0 registered, enabled.
  This is what the previous entry was reaching for and missed: the ask was a source in the
  registration-link list, not the source chart. That earlier change stands — a webinar with
  no channels charts nothing and gains an Email bar on first invite — and the two now agree,
  but it was not what was asked for and can be reverted on its own if it is unwanted.
  Why: the user clarified that the entry belongs in View Registration Link.
- 2026-09-14 — **A webinar with no channels has no sources; Send Invite creates Email.**
  `sourceData` in `OverviewTab` was a hardcoded four-channel array, so a brand-new webinar
  that nobody had been invited to still charted Twitter, LinkedIn and Direct registrations.
  Now `startedWithoutSources` (`!(hasInvited || isCompletedInit)`) marks a webinar that
  opened with nothing in it: its source list is **empty**, and completing the Send Invite
  flow sets `emailSourceCreated` in `handleSent`, which adds a single **Email** source.
  A webinar that already had invites, or has run, keeps its real channel mix — checked all
  three states. Second half of the fix: `VisitedVsRegisteredBar` drew its own fixed
  `["Email","LinkedIn","Twitter","Direct"]` labels and ignored `sourceData` entirely, so the
  chart still showed four bars after the first change; it now derives its labels from
  `sourceData` and falls back to the four only when there are none. Verified by walking the
  real flow in Chrome: blank webinar → no source chart at all → Send Invite → Registration
  by Source is one Email bar. **Known inconsistency left alone:** the sample registrants
  list that appears after sending still carries rows sourced LinkedIn / Twitter / Direct,
  which contradicts a webinar whose only channel is Email. It is pre-existing sample data
  and changing it would disturb the screens the PRD documents. Why: the user asked that an
  empty source list gain an Email source when Send Invite completes.
- 2026-09-10 — **New PRD over the current master flow, plus a screenshot pipeline**, at
  `docs/prd/current/`. Nine sections in the order the user asked for: Introduction (what
  Zoho Webinar is / who uses it / the problem / how the integration solves it), Turning the
  integration on, Creating a webinar, Fields in the create flow, Before the webinar, The
  webinar list, After the webinar, Open questions. 36 figures, all captured from `master`.
  The **field tables list every picklist's actual options**, not option counts — a first
  pass wrote "Picklist (29 options)" and the user rightly asked why the options were
  missing; they are now pulled from the DOM (`.cs-opt` text) so they cannot drift from the
  mock. The interesting facts it records: the 2nd and 3rd reminders add **None** to the same
  eleven intervals the 1st offers, so a webinar can send fewer than three; `Webinar Cost` on
  the create form is what the completed webinar's ROI divides by; and Push Registrants to
  CRM is the setting that removes the re-import step from the introduction's problem.
  **`shoot.mjs` is the reusable part**: headless Chrome over the DevTools protocol, driven
  by `Runtime.evaluate`, writing real PNGs — no npm packages, since Node 22+ has a global
  `WebSocket`. Shots are `{file, steps[]}` where each step is JS run in the page, plus
  injected helpers (`__click`, `__clickRelated`, `__scrollDetail`, `__scrollForm`, `__pick`).
  `node shoot.mjs --eval "expr"` is how the entry points were found. Four traps are written
  up in `docs/prd/current/README.md` and cost real time here: a `\s` regex inside the
  injected template literal collapses to `s`; the detail page and create form scroll inner
  elements so `window.scrollTo` does nothing; the create form's five sections share one
  770px scroll so Preferences/Reminders/Follow-Ups land in a single screenful; and
  **Webinar Revenue is collapsed by default**, so a naive shot captures the panel beneath
  it. Identical file sizes across a batch is the tell that a step silently failed — compare
  md5s. The old PRD at `docs/prd/zoho-webinar/` is untouched and still describes the
  pre-session mock. Why: the user asked for a new PRD over the current flow.
- 2026-09-10 — **PRD Introduction rewritten as four questions, and the business changed.**
  `docs/prd/zoho-webinar/prd-source.md` now opens with **What Zoho Webinar is** / **Who uses
  it** / **The problem** / **How the CRM integration solves it**, then the module screenshot;
  rebuilt with `python3 build_prd.py` (2.58 MB, 49 figures). The business is no longer the
  fitness coach from `demo.txt`: it is a company selling **training courses to other
  businesses**, with Jay as its account executive. The reason is in demo.txt's own prep
  notes — the mock's Deals Won table carries Account names ("Jayas Co", "Suriya Ltd"), which
  contradicts a coach selling to individuals and forced a workaround in the demo. A B2B
  training company fits the mock's data as it stands, and puts webinars at the centre rather
  than alongside: the free masterclass is how leads arrive and the paid course sessions are
  the product, so a session is channel, pitch and deliverable at once. The three questions
  that framing produces — who registered, who turned up, which of them paid — are used to
  structure the problem and then answered one by one by the four capabilities.
  Two things to know: `demo.txt` **still uses the fitness coach**, so the PRD and the demo
  script now disagree on the business; and the PRD's other nine sections still describe the
  mock as it was before this session's template-flow, intro-page and Case 4 work.
  Why: the user asked for that introduction and a business where webinars are central.
- 2026-09-10 — **The blocking cases are answered at the marketplace card, not on the intro
  page.** `integWebinarCardSetup()` — what the Zoho Meetings card's **For webinars &rsaquo;
  Set up** calls — now checks `window._selectedCase` first: **1** opens the no-account
  modal, **4** the not-an-admin modal, **5** the trial-expired modal, and it returns without
  showing anything else. Only **2** and **3** reach the introduction page. Before this the
  card always opened the intro and the check happened on that page's Setup button, so a user
  with no Webinar account was sold the integration before being told they could not have it.
  `integWebinarSetupProceed()` keeps its own copy of the branch, which is now a second guard
  rather than the only one — it still fires if the DEMO case is switched while the intro page
  is open. The meetings path (`mpSetupMeeting` → `ommOpenProviders`) is untouched: it is a
  different product flow with its own provider chooser. Verified from the card: case 1 →
  case1 modal, 2 → intro page, 3 → intro page, 4 → case4 modal, 5 → case5 modal, with
  nothing else on screen in the blocking cases. Why: the user asked for the exceptions to be
  thrown at the setup card rather than on the marketing page.
- 2026-09-10 — **Case 4 loses its "Notify Super Admin" button.** The not-an-admin modal
  offered to email the Webinar Super Admin; only **Cancel** is left. It was also the last
  `alert()` inside a modal this session's work touches — those freeze the renderer until
  dismissed by hand, which had already cost a stuck tab. The modal still explains the
  situation and what to do about it; the difference is that CRM no longer implies it can
  send that mail. Worth knowing while testing: **the case exceptions were never removed** —
  `integWebinarSetupProceed()` still branches on `window._selectedCase`, and all five were
  re-verified (1 → create-account modal, 2 and 3 → setup form, 4 → not-an-admin, 5 → trial
  expired). What changed earlier in the session is *when* they fire: the introduction page
  now comes first, so the check runs on that page's Setup button rather than on the
  marketplace card, and Case 2 being the demo default means you see none of them until the
  DEMO switcher is moved. Why: the user asked for the button to go.
- 2026-09-10 — **Intro page: design and motion, and one feature dropped** (branch 1). The
  stripped-back version below read as documentation, not marketing, so it got a visual pass
  while keeping its shape (no CTAs in the body — the header's Setup button is still the only
  action). Added: a hero on a **drifting gradient** (two blurred radial orbs on slow
  `ixDriftA` / `ixDriftB` loops), a status pill with a **pulsing dot**, the second line of
  the headline in a **blue-to-pink gradient**; the five features as **cards with gradient
  icon tiles** that lift on hover and grow a gradient top rule; and "What it solves" as four
  rows where the old way **strikes itself out** (`ixStrike`, a scaleX on an `:after` rule) as
  the row arrives, answered by a line with a gradient left bar. Everything fades up on scroll
  via one IntersectionObserver with staggered `animation-delay`, and the whole thing goes
  static under `prefers-reduced-motion`. **"The lifecycle emails, handled" was removed** at
  the user's request, leaving five features.
  Two things learned building it: the observer was first given `root: panel`, and it **never
  fired at all** — every block stayed at `opacity: 0`, i.e. a blank-looking page — so it uses
  the viewport now, plus a 1.2s fallback that reveals anything still hidden and on screen,
  because invisible content is a worse failure than no animation. And `ixReveal()` is
  re-run from `integShowPanel()` on every open, clearing `.ix-in` first, or the animation
  would only ever play once per page load. Why: the user said it did not read as a marketing
  page and asked for animation and design, minus that feature.
- 2026-09-10 — **Intro page stripped back to features and problems** (branch 1). The
  marketing-page pass below went too far the other way: it had a hero CTA that turned into
  **"Open settings"** once enabled, a second Setup button in a closing band, and a fake
  record card with an invented **$48,000** influenced-pipeline figure. All of it is gone.
  The page is now one 820px column: a short intro, **What you get** (six features as a
  definition list — the module, webinars created in CRM, invites to your own records, the
  lifecycle emails, registrants as records, revenue attribution) and **What it solves**
  (four problems struck through, each answered by a line underneath). No buttons in the body
  at all — the only action is the **Setup** button in the header, which is why
  `integ-intro-cta2` and its state handling were removed from `integIntroRenderHeader()`.
  The old `.ix-shot` / `.ix-flow` / `.ix-why` / `.ix-close` / `.ix-facts` styles went with
  their markup. The panel is ~7.2 KB, down from ~15.3 KB. Why: the user asked why there was
  an "Open settings" button at all, and for the page to simply explain what the integration
  offers and what it solves, simply and minimally.
- 2026-09-10 — **The integration intro page is a marketing page now** (branch 1). What was
  there: a hero, then **three stacked four-across card grids** — "How it works" (4 steps),
  "Why teams enable it" (4 benefits) and "When you enable, this integration will" (4 ticks)
  — twelve boxes of small grey text, with the last two grids largely restating each other.
  Rebuilt as four beats: a **hero** with one claim ("Run your webinars without leaving
  CRM."), a lede, the **Setup button next to it** and a "See how it works" jump link, plus a
  fake-record product shot (a Lead with Attended / Registered / No-show pills and influenced
  pipeline) so the payoff is shown rather than described; **three steps** as a left-to-right
  flow with arrows instead of four cards; **three** benefit cards instead of four; and a
  closing band that folds the old "what enabling does" list into one sentence beside a
  second Setup button. The fact strip under the hero is deliberately factual, not invented
  stats — Leads/Contacts and person modules, 7 lifecycle emails, 6 attribution models.
  New `.ix-*` styles live with the panel's existing `.iw-*` ones; a `@media (max-width:1080px)`
  block stacks the hero, the flow and the cards. `integ-intro-status` and `integ-intro-cta`
  keep their ids so `integIntroRenderHeader()` still drives them, and it now also sets the
  hero button (`integ-intro-cta2`), which reads **Open settings** once enabled while the
  header stays "Setup". Checked: badge flips to ENABLED, both buttons reach the setup panel.
  **Mistake worth remembering:** the first pass dropped the `</div>` that closed
  `#integ-intro-panel`, and the page went **completely blank** — an unbalanced div swallows
  every panel after it, exactly like the unbalanced-paren failure mode noted for the React
  parts. Count `<div>` against `</div>` across a replaced block before reloading.
  Why: the user asked for the page to be simpler and to read like a marketing page.
- 2026-09-09 — **`index.html` redirects with a cache-buster.** Slate serves the mock with
  `cache-control: public, max-age=31536000` — a year — so a browser that had opened the page
  once kept showing that copy after every redeploy, which reads exactly like "the deploy
  didn't work". (It cost a round of confusion: the file on the server was current, `curl`
  and a fresh tab both proved it, while the user's cached tab was not.) The root redirect
  now appends `?v=<Date.now()>`, so `/` always pulls a fresh copy. Opening `/webinar.html`
  directly still hits the cached copy — hard-reload there. The cost is re-fetching 1.4 MB
  each visit, which is the right trade for a demo. Also worth recording: there are **two
  Slate apps**. `zoho-webinar-eqbkvmwc.onslate.com` is a dead upload from the morning;
  `zoho-webinar-aqxbqcax.onslate.com` is the live one, git-connected to `master` with Auto
  Deploy, and it is the URL to use. Slate labels the build with its own commit id
  (`bbfc4e0`), which is not a commit in this repo — match deployments by content, not by
  that id. Why: the user reported the deployment not reflecting changes.
- 2026-09-09 — **Creating a template from a create-webinar slot happens in Zoho Webinar**
  (branch 1). `+ Create Template` inside a slot's Select Template dialog no longer opens
  CRM's Template Gallery. It opens a **new tab on meeting.zoho.com** — with its own address
  bar, since a mock cannot occupy that domain — showing Zoho Meeting's **Email
  customization** screen: the rail of six lifecycle emails with the slot's own email in
  bold, Quick Templates' Default, the customs already saved for that email (or "No custom
  templates available."), and **Basic (6)**. Picking a layout swaps in the editor — template
  name field, the email's real subject, Registrations chip, ALL COMPONENTS rail, toolbar and
  a `${...}` body. **Save hands the template back and closes the tab**:
  `window.opener.zwSlotTemplateSaved(name, slot)` pushes it into `WEBINAR_CREATED`, adds a
  Setup ▸ Templates row with its Email Type, selects it for the slot (chip updated) and
  reopens the picker on it, then the tab calls `window.close()`. The child is same-origin
  (`about:blank` inherits the opener's origin), which is what makes the callback possible.
  Also: the Select Template dialog's **"All Templates" dropdown is now a static "Zoho
  Webinar"** label with no caret — every template it lists is a webinar template, so there
  was nothing to filter.
  **Hazard learned the hard way:** the blocked-pop-up path used `alert()`, and a modal
  dialog freezes the whole renderer until someone dismisses it by hand — it cost a frozen
  tab and a dead `Runtime.evaluate`. Both pop-up-blocked messages are now a toast
  (`zwPopupBlockedToast`). Five `alert()` calls remain in the mock from before this session
  (Visit Webinar module, Notify Super Admin, Notify Suriya, Add Meeting, Search CRM users);
  they are click stubs, but avoid clicking them while driving the page with automation.
  Why: the user asked for this hand-off, for the tab to close on save with the template
  available here, and for the folder dropdown to become Zoho Webinar.
- 2026-09-09 — **Branch 1 takes branch 2's template and Send Invite flow.** The reverse of
  yesterday's port: 14 of the 23 hunks between the two files came across from
  `template-flow-fixes`, 9 were held back. **Taken — the whole template flow:** creation is
  Create Email Template (module, plus **Email Type locked to Webinar Invitation**, one
  option, `disabled`, no caret) → **Next** → the **Template Gallery** with its category rail
  and the six Basic layouts, headed by "Zoho Webinar" and the type chip; the Templates list
  holds the invitation plus six rows **named "Default"** carrying the real subjects
  (`Registration Confirmation for ${Campaigns.Title}` and the rest), read-only with no
  pencil, cancellation row gone, types stamped by `stampWebinarRowTypes()`; a row click
  **previews** (with the Preview/Analytics tabs) instead of opening the gallery, and the
  pencil on a Default opens **Zoho Webinar's editor in a new tab** with its own
  meeting.zoho.com address bar; a created template lists with name, subject and Email Type.
  **Send Invite's Select Template** now lists only the Invitation-type rows from the
  Templates list. `ucSyncListRow` and its helpers are gone — selecting a card changes what
  is live, not what is listed. **Held back — branch 1's own features:** the intro page's
  "Setup" CTA and enabled badge, Case 2 as the demo default, and the Webinar Timezone label
  and row; all three re-checked after the port (`_selectedCase === 2`, the CTA reads
  "Setup", the label is present). One fix made on the way in: branch 2's Send-Invite create
  path pushed only into `WEBINAR_CREATED` and `TPL_UC_STATE`, so with the picker now reading
  the Templates list a template created inside Send Invite would not have been selectable in
  the step that created it — it now also calls `tplPageAddCreatedRow(..., 'Invitation')`.
  Why: the user asked for both flows on branch 1, ahead of taking them to master.
- 2026-09-09 — **Added `index.html`, a redirect to the mock.** Deploying the repo to a
  static host answered **404 at the root**: the mock is `webinar.html`, and Catalyst (like
  `http.server` and GitHub Pages) serves `index.html` for `/`, so there was nothing at `/`
  to serve — `/webinar.html` was live and fine the whole time. `index.html` is a redirect
  (meta refresh plus `location.replace`, carrying any query string and hash through, with a
  visible link as the fallback) rather than a copy, so there is only one 1.4 MB file to keep
  in step. Worth knowing for the next deploy: the copy on
  `zoho-webinar-eqbkvmwc.onslate.com` was byte-identical to `master`
  (md5 `dc1f18c0045034b72177a58a1b0dd164`), i.e. the pre-session baseline with none of the
  template-flow work — deploy from `templates-flow` or `template-flow-fixes` to demo it.
  Why: the user hit the 404.
- 2026-09-09 — **Webinar Cancelled Template is a shipped row, listed last** (branch 1). It
  had no row of its own, so it only appeared once you selected something for that use case
  — and then arrived at the *top*, because `tplPageAddCreatedRow` unshifts. It is now the
  eighth entry in `TPLPAGE_WEBINAR_ROWS`, after Absentees Follow-up, matching the order of
  the gallery's rail: the list shows all eight lifecycle emails from the start and the
  cancellation email sits at the end, where it belongs — it only goes out if the webinar is
  called off. `ucSyncListRow` now finds and renames it like any other, so nothing is added
  on selection any more. Why: the user asked for it last.
- 2026-09-09 — **One row per lifecycle email: selecting a template renames it, never adds
  a second** (branch 1). Selecting a custom in the gallery had been *adding* a row, so the
  Templates list showed both "Webinar Invitation Template" and the custom you had just
  chosen — two rows for one email. `ucEnsureListRow` is replaced by `ucSyncListRow`, which
  finds the row that stands for the use case (`ucUseCaseRow`: the shipped
  `TPLPAGE_WEBINAR_ROWS` entry if there is one, else the first created row with that
  Email Type), drops any other Zoho Webinar row carrying the same type, and renames the
  survivor to the live template. So picking "Long-form invite" turns the Invitation row
  into *Long-form invite · Invitation template*, and picking Default back turns it into
  *Webinar Invitation Template* again — the count stays 7. Saving a new custom from the
  gallery goes through the same call instead of `tplPageAddCreatedRow`, so a save replaces
  its email's row too. Webinar Cancelled has no shipped row, so its first selection adds
  one and later ones rename it. The row keeps its use case in `row.etype`, and the pencil's
  key now falls back to that use case (`key || ucKey`), so a renamed row still opens the
  right editor rather than the generic module one. Consequence to know: a custom that is
  saved but not live has no row of its own — the list is a view of what each email is
  currently set to, and the customs themselves live in the gallery. Why: the user pointed
  out the selected template was listed alongside the one it replaced.
- 2026-09-09 — **Default is back in Custom Templates; the Email Type text stays** (branch
  1). Half of the entry below was reverted at the user's request: the Default card again
  leads the Custom Templates group in the gallery (count `customs.length + 1`, both cards
  showing "In use" together), and the "No custom templates available." empty state is
  unreachable again and gone. The Email Type change was explicitly kept — it stays a text
  segment on the row's subline, not a column. Why: the user asked to revert the previous
  change except for the email type.
- 2026-09-09 — **[customs half reverted, see above] Email Type moved out of the
  column and into the row** (branch 1). Two changes at the time. (1) The
  Default no longer appeared under Custom Templates — that group listed what had actually
  been saved for the use case, and when nothing had, it said "No custom templates
  available." **This half was reverted the same day.** (2) The
  **Email Type column is gone.** A column that only exists for one module leaves a hole in
  the table for every other module, so the type now reads as the tail of the row's own
  subline: *Zoho Webinar · Sent when you invite CRM records to a webinar · Invitation
  template*. Non-webinar rows simply have no third segment. The table is back to five
  columns for every module (plus the hover-edit spacer). **Removed with the column: its
  caret filter** — `TPLPAGE_ETYPES`, `tplPageEType`, `tplPageETypeColumnOn`,
  `tplPageRenderETypeHead`, `tplPageRenderETypeMenu`, `tplPageToggleETypeMenu`,
  `tplPagePickEType`, the outside-click listener and the `<th>` — so **there is no longer
  any way to filter the list by email type**, and the "No <type> templates yet." empty
  state went with it. `TPLPAGE_ETYPE_BY_KEY`, `tplPageETypeOf` and `TPLPAGE_KEY_BY_ETYPE`
  stay: they write the subline and still route a row's name click to the right use case.
  Why: the user asked for both.
- 2026-09-08 — **Email Notifications header trimmed, Default offered in both groups**
  (branch 1). The header repeated itself three times: the rail already names the use case,
  and next to the title sat a blue pill with that same label plus the type name in grey.
  Both are gone; the line under the title is now one standing sentence about what the screen
  is for ("You can customize the email that will be sent to your attendees…"), static in the
  markup, so `ucRender` no longer writes a header at all. The per-use-case note went with
  the chip — worth knowing, because that note was where the link rule was spelled out
  ("It must carry the Recording Link"); the rule is still enforced on save, just no longer
  stated here. **Custom Templates now leads with the Default card** as well as Quick
  Templates: it is a choice for the use case like any other, both cards select `'quick'` and
  show "In use" together, and the count badge is `customs.length + 1`. The "Nothing saved
  yet…" empty state is therefore unreachable and was removed — the group always has at
  least the Default. Why: the user asked for the Default in both groups, for that
  paragraph, and for the two duplicated header texts to go.
- 2026-09-08 — **Create Email Template asks for the module, and Email Type with it**
  (branch 1). `+ New Template` went straight to the gallery whenever the list was filtered
  to Zoho Webinar, so the module was never actually chosen. It now always opens the dialog:
  **Select Module** first, with **Zoho Webinar** back in the list, and an **Email Type** row
  that appears only when Zoho Webinar is the module (`ctModuleChanged`) — the type means
  nothing for an ordinary CRM module. Its options are the eight lifecycle emails, labelled
  the way the Templates list labels them (Invitation, Confirmation, 1st–3rd Reminder,
  Attendees/Absentees Follow-up, Webinar Cancelled) but valued by use-case key, built from
  `TPL_USECASES` so the dialog cannot drift from the gallery's rail. Next carries the choice
  through: `openUsecaseGallery(_ctUsecase)` opens the gallery on that use case — rail entry,
  chip and note — and `_ctType` / `_tplTypeName` are stamped from it, so the required link
  and allowed link types are the chosen email's from the start. A non-webinar module still
  gets `_ctType = 'None'` and the old Template Gallery. Why: the user asked for the module
  box, Email Type under Zoho Webinar, and the chosen type to be what the next page shows.
- 2026-09-08 — **Selecting a template in the gallery lists it under Templates** (branch 1).
  Picking a card in the Email Notifications gallery only flipped the "In use" badge — the
  use case's seeded customs ("Long-form invite", "twsd") existed in `TPL_UC_STATE` and
  nowhere else, so a template you had just chosen could not be found in Setup ▸ Templates.
  `ucSelect` now calls `ucEnsureListRow`, which adds a Zoho Webinar row carrying the use
  case's Email Type unless that name is already listed. `UC_DEFAULT_ROW_NAME` maps each
  use case's Default to the row it already has in `TPLPAGE_WEBINAR_ROWS`, so selecting
  Default matches instead of adding a second row — note the Default's editor label
  ("Send Invite Template") is not its list name ("Webinar Invitation Template"), which is
  why the map is needed. Re-selecting adds nothing. Worth knowing: **Webinar Cancelled**
  has no shipped row, so selecting its Default is the one case where choosing a Default
  creates a row — and its type is not in `TPLPAGE_ETYPES`, so the chip shows but the Email
  Type filter has no entry for it. Why: the user asked that whatever template is selected
  show up in the template list.
- 2026-09-08 — **Email Type removed from Create Email Template** (branch `templates-flow`).
  With Zoho Webinar out of that dialog's module list, Email Type had nothing left to
  describe — it named a webinar lifecycle email, and those are created in the gallery now.
  The dialog is a single **Select Module** row. `ctNext` sets `_ctType = 'None'`, the
  untyped type that already existed: no required link, every link type available. The
  Template Gallery's type chip is suppressed when the type is None, so it no longer shows
  a "None" pill. Known gap left alone: `tplMergeModules` still leads with Registrations
  for anything that isn't a Webinar Invitation, so a plain Contacts template offers
  registrant merge fields rather than the module's own — pre-existing, and outside what
  was asked. Why: the user asked for it once Zoho Webinar was gone from the dialog.
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
- 2026-09-08 — **Templates list row actions (branch 1)**: a pencil **edit icon** now appears
  on row hover in the column just before **Email Type** and opens that template in the
  editor; clicking the **template name** opens the **Email Notifications** use-case gallery
  at that email's use case instead of the read-only preview. Why: the user wanted editing to
  be one hover away, and a click on a template to land on the create-template page where the
  available templates for that use case are shown.
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
