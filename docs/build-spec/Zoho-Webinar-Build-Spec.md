# Build: Zoho Webinar as a module inside Zoho CRM

*Single-file edition. Nine sections, ~15.4k words. Everything the build needs is in this document.*

## Contents

- [Read this first](#read-this-first)
- [1. The module, its entities and every derived value](#1-the-module-its-entities-and-every-derived-value)
- [2. The integration: marketplace, the gate, the wizard](#2-the-integration-marketplace-the-gate-the-wizard)
- [3. Create Webinar: the form and everything inside it](#3-create-webinar-the-form-and-everything-inside-it)
- [4. The scheduled webinar record](#4-the-scheduled-webinar-record)
- [5. The completed webinar record](#5-the-completed-webinar-record)
- [6. Lifecycle emails and their templates](#6-lifecycle-emails-and-their-templates)
- [7. What is genuinely undecided](#7-what-is-genuinely-undecided)
- [8. Decisions already made, and what was rejected](#8-decisions-already-made-and-what-was-rejected)

---

## Read this first

You are working in the Zoho CRM codebase. This document covers **one feature, end to end**:
a new **Zoho Webinar module** in CRM, its settings, its record pages, and every operation a
user performs on it.

**Everything you need is in this document. There is nothing else to read.** There is no
mock, no Figma and no running prototype available to you — every field, option, rule and
error string you need is written out here verbatim. Where a value is a placeholder rather
than a specification, it says so.

### What you are building

A CRM module called **Zoho Webinar**, plus:

1. A **Marketplace integration** that turns the module on and carries two settings that change
   how the rest of the feature behaves.
2. A **create form** with 63 fields across five sections, restructured by two picklists.
3. A **record page** with two distinct states — scheduled and completed — that differ in their
   header actions, their summary band, and one whole extra section.
4. **Send Invite**, which is the flow that connects the webinar to CRM's own records.
5. A **lifecycle email system** of eight template types with per-type link rules.

### Scope fence

**In scope:** everything in sections 1–8 below.

**Out of scope — do not touch:**

- CRM's existing **Mass Email** compose step. Send Invite hands off to it. It already works and
  must keep working exactly as it does today; you supply the recipient list and the template,
  and nothing more.
- CRM's **email template editor** itself. You add template *types* and the rules that govern
  them (section 6), not a new editor.
- CRM's **list view shell**, filters, sort and column chooser. The Webinar module uses the
  standard one; you define its columns, not the mechanism.
- The **Zoho Webinar product's own surfaces** — the session runtime, the broadcast UI, the
  recording pipeline. CRM links to them and reads from them. It does not reimplement them.
- Standard CRM record actions (Clone, Share, Delete, Print Preview, Add Related List,
  Create Button, Create Client Script, View Followers). They come free with being a module.
  Only **Cancel Webinar** is yours (section 4).

### The one idea behind the whole feature

Zoho Webinar on its own cannot see CRM, and that costs four things. Every decision below traces back to removing one of them:

1. **The audience has to be rebuilt.** The people you want at the webinar are already Leads and
   Contacts. Without this, you export to CSV and re-import into a separate tool, and the list
   starts drifting from CRM the moment it is made.
   → *Who Can Participate From CRM* (section 2) and *Send Invite* (section 4).
2. **The results have to be carried back by hand.** Registrations and attendance land in the
   webinar tool; getting them onto the CRM record is another export and import.
   → *Push Webinar Registrants to CRM* (section 3) and the *Invited* related list (section 5).
3. **Nobody can answer "did it make money?"** The cost sits in one system and the deals in
   another, and no one joins them.
   → *Webinar Cost* (section 3), *attribution* (section 2) and *Webinar Revenue* (section 5).
4. **It is a second product to operate.** Different UI, different login, different conventions.
   → The whole thing being a CRM module rather than an embedded app.

If a decision you have to make is not covered here, resolve it in favour of whichever option
removes one of those four costs. That is the tie-breaker.

### Rules of engagement

**Build it as a real module, not a page.** Zoho Webinar gets a module record, a list view, a
record detail page, related lists, an owner, layouts and templates — the same furniture as
Leads. Anything you are tempted to special-case is probably something the module system
already does; use the module system.

**Derived values are derived, never stored.** Attendance rate, ROI, absentee counts, seats
left — all of these are computed from their inputs at read time. section 7 gives every formula.
Storing them creates two sources of truth that drift.

**"Not yet known" is not zero.** A webinar that has not happened has *no* attendance, which is
a different state from an attendance of zero. The list view renders an em dash for it. Do not
collapse the two into `0` anywhere — not in the model, not in the UI.

**Visibility means not rendered.** Throughout this document, a field that is not visible in
a given configuration is **absent from the DOM**, not present-and-disabled. This matters: the
create form has 63 fields and only 42 render in the default configuration.

**Quote the product's own words.** Every label, option and error string in this document is
verbatim. Do not improve the wording. If a label reads awkwardly, section 8 is where that gets
raised — several of them are awkward on purpose, because the same words appear elsewhere in
CRM and consistency beats elegance.

---

## 1. The module, its entities and every derived value

Read this before anything else. The rest of the set assumes these names and these formulas.

---

### Zoho Webinar is a CRM module

Not an embedded app, not a page — a module, with everything that implies: records, an owner,
a list view, a record detail page, related lists, layouts, email templates, and standard
record actions. It appears in the left rail alongside Leads, Contacts and Meetings once the
integration is enabled (section 2), and not before.

**Nothing in the module is reachable until the integration is enabled.** That is the only gate.

#### Webinar Category — the field that drives everything

Every webinar record carries **Webinar Category**, a picklist with three values:

| Value | Meaning |
|---|---|
| `Scheduled Webinar` | Created, not yet run |
| `Completed Webinar` | Has run |
| `On-Demand Webinar` | A recorded session, played on demand |

**Which record page a webinar shows follows from this field, not from comparing its date to
now.** A scheduled record shows Start Webinar / Send Invite / View Registration Link in its
header and gains none of the revenue reporting. A completed record loses all three of those
buttons and gains the Webinar Revenue band. section 4 and 05 cover the two states.

Do not compute the state from the date. A webinar whose time has passed but which was never
run is not automatically completed — the category is what says so.

---

### Entities

#### Webinar

The module record. Its full field list is section 3 — 63 fields, because the create form *is*
the record's field set. The ones other entities depend on:

| Field | Type | Used by |
|---|---|---|
| Webinar Title | Text, **the only required field** | everywhere |
| Webinar Category | Picklist (above) | which record page renders |
| Webinar Type | Picklist — `Live Webinar` / `OnDemand Webinar` | form shape, duration vs video |
| Webinar Date & Time | Date + time | reminders, the window, the list view |
| Webinar Duration | Compound picklist, hours + minutes | live only |
| Webinar Owner | User lookup | CRM record ownership, sharing, "My Webinars" |
| Organizer | User picklist | the session's host — **not the same as Owner** |
| Webinar Cost | Currency-ish text | every ROI figure in section 5 |
| Registration Type | Picklist — `With Registration` / `Without Registration` | whether registrants exist at all |
| Set Registration Limit | Number | seats-left arithmetic |

#### Registrant

Created when somebody signs up. Holds their name, email, the **source** they arrived through,
their registered date, and — after the session — whether they attended.

A registrant **may or may not** correspond to a CRM record. One who came through the public
link is not in CRM unless *Push Webinar Registrants to CRM* was on (section 3). A registrant
with no CRM record shows an em dash in the Module column.

**After the session every registrant is exactly one of: attendee or absentee.** That partition
is what decides which follow-up email they receive (section 6).

#### Invitee

Distinct from Registrant, and the distinction is load-bearing. An **invitee** is a CRM record
that was sent an invitation through Send Invite (section 4). It carries:

| Field | Values |
|---|---|
| Module | the CRM module the record came from |
| All Invite Status | `Registered` / `Not Registered` |
| Webinar Status | `Attended` / `Not Attended` |
| Invite Sent on | user + timestamp |

**Two separate status fields, tracking two different questions.** *All Invite Status* asks
whether they acted on the invitation. *Webinar Status* asks whether they turned up. A record
can be Registered and Not Attended — that is the no-show, and it is precisely the population
the Absentees follow-up exists for.

> **Invitees and registrants are not subsets of one another.** Somebody invited from CRM who
> never registered is an invitee and not a registrant. Somebody who found the public link is a
> registrant and never an invitee. Do not model either as a filter over the other.

#### Registration Source

A tracked channel a registration can arrive through. Holds source name, created-by, visited
count, registered count, enabled flag.

**A new webinar has no sources at all** — the list is empty, not seeded with defaults. The
first one is created by completing Send Invite, which creates a source named `Email` and
switches *Enable Source Tracking* on. A second Send Invite does **not** create a second row;
the creation is guarded against duplicates. One channel, one row.

#### Poll

Written before the session, answered during it. A poll has a question, a set of options, and a
type: `Multiple choice`, `Short answer` or `Checkbox`. After the session it carries per-option
vote counts and a respondent list.

#### Q&A entry

A question asked during the session: asker, timestamp, their CRM module as a tag, the question
text, and optionally a nested host answer with the responder's name. **Not every question has
an answer**, and that is real behaviour rather than missing data — an unanswered question is a
follow-up somebody still owes.

#### Session File

An attachment: file name, size, date added. Separate from **Recordings**, which is its own
related list. A recording uploaded as a session file is not the same object as the automatic
session recording produced by the Preferences toggle.

---

### Derived values — compute these, never store them

#### Attendance

```
Total Registration  = count(registrants)
Total Attendees     = count(registrants where attended)
Total Absentees     = Total Registration − Total Attendees
Attendance Rate     = Total Attendees / Total Registration        (as a percentage)
```

**Before the webinar has run, attendance does not exist.** Total Attendees, Total Absentees,
Attendance Rate and the two attendance charts are absent — not zero. The list view renders
`—` for Attendance Count and Attend. Rate on any webinar that has not happened.

#### Seats

```
Seats Left = Set Registration Limit − Total Registration
```

Only meaningful when a limit is set. With no limit there is nothing to count down from, and
the seats-left line is absent rather than showing a large number or infinity.

#### Webinar ROI

Six tiles on the completed record (section 5). The arithmetic:

```
Cost                = Webinar Cost                    (from the create form)
Revenue (Won)       = Σ amount of Deals Won
In Pipeline         = Σ amount of open influenced deals
ROI                 = (Revenue − Cost) / Cost          expressed as a signed percentage
Cost / Attendee     = Cost / Total Attendees
Revenue / Attendee  = Revenue / Total Attendees
```

Worked through, so you can check your implementation against known-good numbers:

| Input | Value |
|---|---|
| Webinar Cost | 2,500 |
| Deals Won | 1000 + 1500 + 2000 + 3200 + 2800 + 1800 + 4500 |
| Total Attendees | 15 |

| Output | Expected |
|---|---|
| Cost | `$2,500` |
| Revenue (Won) | `$16,800` |
| ROI | `+572%` |
| Cost / Attendee | `$167` |
| Revenue / Attendee | `$1,120` |

`(16800 − 2500) / 2500 = 5.72`. `2500 / 15 = 166.67`, displayed `$167`. `16800 / 15 = 1120`.

**Guard the divisions.** Total Attendees is zero on a webinar nobody attended, and Cost is zero
or empty on a free one. Neither per-attendee tile nor ROI has a defined value then; render the
tile empty rather than `∞`, `NaN` or `0`.

#### Which deals count

Decided by the **attribution model** set in the integration (section 2). A contact usually
attends several webinars before a deal closes, and the model decides how that deal's revenue
is divided across them.

> **This is unresolved and blocks the revenue panel.** Whether the Deals Won table shows each
> deal's *full* amount or its *attributed share* is not specified anywhere, and the two give
> answers that differ by a factor of the number of webinars involved. See section 7. Do not
> guess — the ROI figure is the headline number of the whole feature.

---

### State: what exists when

A compact map of which things are present in which state. "—" means absent from the DOM, not
disabled.

| | Scheduled | Completed |
|---|---|---|
| Start Webinar / Send Invite / View Registration Link | yes | — |
| Edit, Actions | yes | yes |
| Cancel Webinar in the Actions menu | yes | — |
| Registration Overview | registration only | registration + attendees + absentees |
| Registration by Module / by Source | yes | yes |
| Attendance by Module / by Source | — | yes |
| Daily Registration Trend | yes | yes |
| Attendees and Registrants list | — | yes, six tabs |
| Webinar Revenue band | — | yes |
| Polls | written, unanswered | answered, with results |
| Q&A | — | yes |
| Invited related list | yes, once invites are sent | yes |

The related-list rail is identical in both states:

```
Notes · Invited · Polls · Q&A · Recordings · Session Files · Open Activities · Closed Activities
```

**Webinar Revenue is not in that rail.** It is a collapsible band in the record body, collapsed
by default, reachable only by scrolling. That is deliberate — it is reporting, not a related
list — but it means there is no rail shortcut to the feature's headline numbers. section 7 raises
whether that is right.

---

### The list view

Standard CRM list view. The module's columns, in order:

| # | Column | Notes |
|---|---|---|
| 1 | *(checkbox)* | row select |
| 2 | Webinar Name | carries the view selector |
| 3 | Webinar Category | the three values above |
| 4 | Webinar Date & Time | e.g. `Mon, Aug 11, 2025 11:00 AM IST` |
| 5 | Registration Count | integer |
| 6 | Attendance Count | **`—` until the webinar has happened** |
| 7 | Attend. Rate | **`—` until the webinar has happened**, else e.g. `77%` |
| 8 | Webinar Duration | e.g. `1 hr 30 mins` |
| 9 | Organiser | user |
| 10 | Webinar Type | `Live Webinar` / `On-Demand Webinar` |

Page actions: `▿ Filter`, `⇅ Sort`, **Create Webinar**, and a `⋮` overflow.

**A recurring webinar appears as one row per occurrence**, each with its own registration
count — not one row with a count of occurrences.

---

### Naming

These names are used consistently across every file in this set, and several of them are
easy to confuse. Getting them wrong produces code that reads plausibly and means the wrong
thing.

| Term | Is **not** | Difference |
|---|---|---|
| Webinar **Owner** | Organizer | Owner is the CRM record owner — sharing, assignment, "My Webinars". Organizer is the person who runs the session. Separate fields, separate option lists. |
| **Registrant** | Invitee | Registrant signed up. Invitee was sent an invitation from CRM. Neither contains the other. |
| **Registration Form** | Customize Registration Page | The form is *which fields are collected*. The page is *how the public page looks*. Two adjacent picklists. |
| **Session Files** | Recordings | Separate related lists. An uploaded recording is not the automatic session recording. |
| **All Invite Status** | Webinar Status | Did they act on the invite / did they turn up. |

section 8 covers the naming decisions that were made and rejected, and why.

---

## 2. The integration: marketplace, the gate, the wizard

Turning the feature on. Done once, by an admin. **Nothing in the Zoho Webinar module exists
until this completes** — the module is not in the left rail, the list view is unreachable, and
no webinar can be created.

Two of the four wizard steps set values that change how the rest of the product behaves, which
is why they get their own sections below.

---

### Where it starts

`Setup → Marketplace → Zoho → the Zoho Meetings card → For webinars › Set up`

The Zoho Meetings card carries two halves — **For webinars** and **For online meetings** —
each with its own `Set up` button, and a note reading *"One Zoho Meetings login connects both.
Set up one or both independently."* You are building the webinars half only. The meetings half
already exists; leave it alone.

---

### The account gate — this comes first

**The card checks the user's account situation before showing anything about the integration.**
Three situations stop the flow dead, each with its own modal:

| Situation | Result |
|---|---|
| No Zoho Webinar account | Modal offering to create one. Flow stops. |
| User is not an admin | Modal saying so. Flow stops. |
| Trial expired | Modal saying so. Flow stops. |

Only a valid account reaches the introduction page.

**The check belongs at the card, not on the introduction page.** This was got wrong once and
corrected: originally the card always opened the introduction page and the check ran on *that*
page's Setup button, which meant a user who could not have the integration was shown a page
selling it to them first. Run the check before anything is rendered.

Keep a second copy of the same branch on the introduction page's Setup button as a guard — the
account situation can change while the page is open.

> The not-an-admin modal's only button is **Cancel**. It previously offered to notify the
> Webinar Super Admin, and that was removed: CRM cannot actually send that mail, so the button
> promised something the product does not do. Do not reintroduce it.

---

### The introduction page

A marketing page explaining what the integration makes possible: what it is, what you get,
what it solves. Its only action is a **Setup** button, top right.

Two things about that button:

- **It reads `Setup`, not `Enable Integration`.** It does not enable anything — it opens the
  wizard, and enabling happens at the end of that. It previously read "Enable Integration" and
  was misleading.
- **After the integration is enabled it still reads `Setup`**, but opens the enabled settings
  panel instead of the wizard. The page's status badge flips from `NOT ENABLED` to a green
  `ENABLED` at the same time, so the page stops contradicting itself when a user returns to it
  from Marketplace.

---

### The wizard

**Setup** opens a four-step wizard. Each step has **Cancel** and **Next**.

| Step | Asks | Control | Default |
|---|---|---|---|
| 1 | Email + Organisation | Text / picklist | the signed-in user's |
| 2 | Sync past webinars? | **Radio pair, Yes / No** | **Yes** |
| 3 | Who Can Participate From CRM | Checkbox list | Leads + Contacts, locked on |
| 4 | Webinar Deal Attribution | Card select, six models | **Linear** |

**Step 4's Next button reads `Enable Integration`**, because it is the last one. Pressing it
turns the integration on and lands on the enabled page.

#### The steps accumulate

**An answered step stays on screen.** Next reveals the following step below it; it does not
replace what came before. You scroll up through the connection, the sync answer and the module
list while deciding attribution.

Only the step currently being answered shows its Cancel and Next — earlier footers are hidden,
because a pair of buttons under a settled section suggests it is still in play. A hairline rule
separates consecutive steps, and Next smooth-scrolls the newly revealed step to the top.

**Implementation note, learned the hard way:** the steps are shown and hidden in place, not
rendered as separate pages, because the final action reads every answer out of the DOM at the
end. Every earlier field has to still exist when `Enable Integration` is pressed. If you
rebuild this as a router with one step per route, you must carry the answers in state instead.

Step 3's module list **populates when the step is displayed**, not on wizard open.

**Cancel** abandons setup and returns to the introduction page — or to the enabled panel if
the integration is already on. Reopening the setup panel always resets to step 1; a second
visit does not resume mid-wizard.

#### Step 2 is radios, not a picklist

A binary question behind a click is a binary question with one answer hidden. It was a
dropdown; it is now a **Yes / No radio pair with Yes preselected**.

> Keep a hidden input carrying the `yes`/`no` value if your form serialisation wants one — and
> keep the radios and that value in step when the answer is set programmatically.

---

### Step 3 — Who Can Participate From CRM

**The single most load-bearing setting in the integration.** It is the list of CRM modules
whose records may be invited to a webinar, and it drives the module dropdown in Send Invite
(section 4). **Turn a module off here and it disappears there.** Nothing else in the product
surfaces that consequence, so treat this list as the source of truth for that dropdown.

The control is CRM's standard module picker: one card, a **Search** field, then a flat
scrollable checkbox list. Not a grid, not chips, not grouped.

Every module, verbatim, in list order:

| # | Module | Default |
|---|---|---|
| 1 | Leads | **locked on** |
| 2 | Contacts | **locked on** |
| 3 | Vendors | off |
| 4 | Donors | off |
| 5 | Volunteers | off |
| 6 | Members | off |
| 7 | Students | off |
| 8 | Alumni | off |
| 9 | Partners | off |
| 10 | Speakers | off |
| 11 | Referrals | off |
| 12 | Patients | off |
| 13 | Subscribers | off |

**Leads and Contacts cannot be switched off by any route.** They render ticked, with a red
asterisk and a muted label, no hover state and no pointer cursor, and the toggle handler
returns early for anything in the locked set. A freshly enabled integration can therefore
invite Leads and Contacts and nothing else.

#### Why this list and not CRM's full module list

**Every module here is a person** — someone who can hold an email address and occupy a seat.
Accounts, Potentials, Cases, Campaigns and Meetings were deliberately removed: a company, a
deal, a ticket, a campaign and an event cannot attend a webinar. Any module added here in
future must pass the same test.

The names are what a business calls the people it holds, which is why the list runs past the
standard modules into Donors, Volunteers, Students, Alumni, Patients and Subscribers — a
non-profit, a university, a clinic and a subscription business all build a module like that.

#### The heading is intent, not mechanism

Mechanically this gates who can be **invited**, not who can **attend** — anyone holding the
public registration link can still register. The section is called *Who Can Participate From
CRM* as a statement of intent. Its subline names the consequence rather than restating the
heading:

> Choose which CRM modules your participants can come from. Turn a module off and its records
> can no longer be added to a webinar.

**The word "invite" is deliberately absent from both.** Do not reintroduce it.

---

### Step 4 — Webinar Deal Attribution

A contact usually attends more than one webinar before a deal closes. This decides how that
deal's revenue is divided across them, and it is what makes the ROI figures in section 5 mean
anything.

Six models, presented as selectable cards. **Descriptions verbatim, in display order:**

| Model | Description |
|---|---|
| First Webinar Interaction | Attributes 100% of the deal revenue to the earliest webinar attended. |
| Last Webinar Interaction | Attributes 100% of the deal revenue to the most recent webinar attended. |
| **Linear** *(default)* | Distributes the deal revenue equally across all webinars attended. |
| Increasing Time Decay | Assigns more credit to earlier webinars and gradually less to later ones. |
| Decreasing Time Decay | Assigns more credit to the most recent webinars and gradually less to earlier ones. |
| Position-Based | Gives 40% to first, 40% to last, 20% split across in-between webinars. |

Each card has an info icon revealing a tooltip on hover.

**Linear is preselected.**

> **Two of these six cannot be built from what is written.** Only Position-Based states its
> split numerically. The Time Decay pair give a *direction* but no decay function and no
> half-life, so the actual weighting is unspecified — and their descriptions read inverted
> against the usual meaning of the term, since "Increasing Time Decay" gives *more* credit to
> *earlier* webinars. Both are in section 7 as blocking. Do not invent a curve.

---

### The enabled page

After `Enable Integration`, the same three settings again — connection details, sync past
webinars, Who Can Participate From CRM, and Webinar Deal Attribution — now with a
**dirty-state Save bar** that appears when anything changes.

The sync answer from step 2 carries across to this page.

> Historically this page was missing the sync field entirely: the code that populated it looked
> for markup that never existed, so the function was a permanent no-op and the field simply did
> not appear after enabling. Make sure every setting from the wizard has a real control here.

**The Save bar has no specified success or failure state.** See section 7.

---

## 3. Create Webinar: the form and everything inside it

**Where it starts:** the **Create Webinar** button on the list page.

Five sections in a single scroll — **Webinar Details**, **Registration Setup**,
**Preferences**, **Reminders**, **Follow-Ups**. **63 fields in total; 42 render in the default
configuration.** The rest are revealed by the branches below.

**Only one field is required: Webinar Title.** Saving without it is refused and the field is
marked. Nothing else blocks a save.

---

### The two branches that restructure the form

Everything else in this file hangs off these.

| Picklist | Values | Effect |
|---|---|---|
| **Webinar Type** | `Live Webinar` *(default)* / `OnDemand Webinar` | what the session *is* |
| **Registration Type** | `With Registration` *(default)* / `Without Registration` | whether registrants exist at all |

Remember: **not visible means not rendered.** Switching a branch removes fields from the DOM.

> Switching a branch must clear every dependent control belonging to the previous one, not
> merely hide the row it sat in. A value typed into a field that is then hidden must not
> silently survive into the saved record.

---

### Webinar Details

In flow order. `L` = Live + With Registration, `W` = Live + Without Registration,
`O` = On-Demand.

| Field | Type | Req | Default | L | W | O |
|---|---|---|---|---|---|---|
| Webinar Title | Text | **Yes** | placeholder `Enter webinar title` | ✓ | ✓ | ✓ |
| Webinar Type | Picklist | No | `Live Webinar` | ✓ | ✓ | ✓ |
| Webinar Date & Time | Date input + time picklist | No | today, `10:00 AM` | ✓ | ✓ | ✓ |
| Webinar Duration | Compound picklist, hours + minutes | No | `1 hr` + `00 min` | ✓ | ✓ | — |
| Video File | Picklist (source chooser) | No | — | — | — | ✓ |
| Webinar Timezone | Picklist | No | `(-6) Central` | ✓ | ✓ | ✓ |
| Allow video play/pause | Checkbox | No | checked | — | — | ✓ |
| Webinar Owner | Picklist w/ search + user-lookup button | No | `Rao Priya` | ✓ | ✓ | ✓ |
| Organizer | Picklist w/ search | No | `Jayasuriya` | ✓ | ✓ | ✓ |
| Repeat Webinar | Custom control → modal | No | off | ✓ | ✓ | — |
| Co-Organizer | Picklist w/ search | No | `None` | ✓ | ✓ | — |
| Webinar Cost | Text, `$` prefix, info icon | No | placeholder `0.00` | ✓ | ✓ | ✓ |
| Description | Textarea | No | empty | ✓ | ✓ | ✓ |

#### Options, verbatim

```
Webinar Type        Live Webinar · OnDemand Webinar
Webinar Date & Time 9:00 AM · 10:00 AM · 11:00 AM · 12:00 PM · 1:00 PM · 2:00 PM
Webinar Duration    hours: 1 hr … 24 hr        minutes: 00 min · 15 min · 30 min · 45 min
Video File          From Zoho Webinar Recordings · Upload Files / Documents ·
                    Zoho WorkDrive · Other Cloud Services
Webinar Timezone    (-5) Eastern · (-6) Central · (-7) Mountain · (-8) Pacific ·
                    (+0) UTC · (+5:30) IST
Webinar Owner       Rao Priya · Jay Acme · Mark Acme · Suriya
Organizer           Jayasuriya · Morrison Troy
```

> The Owner and Organizer option lists are placeholders standing in for real user directories.
> The *fact that they are two different directories* is the specification; the names are not.

#### Webinar Owner and Organizer are different things

**Owner is a CRM concept.** Every CRM record has one, and it drives record-level sharing,
assignment rules and "My Webinars" filters. **Organizer is the webinar's host** — the person
who actually runs the session. Separate fields, separate directories, and they must not be
collapsed into one.

Both use the same shell: a picklist whose dropdown has a **sticky search box** at the top
filtering the options, with an empty state when nothing matches. Owner additionally has a
user-lookup icon button beside the field.

> The search box must stop click and keydown from propagating. Without that, typing in it
> reaches the picklist trigger behind and closes the dropdown on the first keystroke.

> A dropdown containing a search box needs a minimum width of its own (~230px). Inheriting the
> narrow width of its trigger clips the search field to something like `Search u…`.

#### Webinar Cost

`$` prefix inside the field, an info icon at the right. Tooltip, verbatim:

> "This is the amount attendees will be charged to register for this webinar."

**This field is the denominator of every ROI figure in section 5.** A cost of `2500` produces
Cost `$2,500`, ROI `+572%`, Cost/Attendee `$167`, Revenue/Attendee `$1,120`.

> **The tooltip and the ROI panel contradict each other** — one says revenue charged to
> attendees, the other treats it as expenditure. This is blocking; see section 7. The `$` is
> hard-coded and the field has no numeric validation, which also needs resolving.

#### Repeat Webinar → modal

Opens its own modal. Fields:

| Field | Options |
|---|---|
| Repeat Type | *(recurrence pattern)* |
| Repeat Ends | `On` *(a date)* / `After` *n* `Webinars` |
| Registration Mode | `Register and attend each event individually` · `Register once and attend any event` |
| Open Registration for | `All Webinars` · `Only selected number of occurrences` → `1`–`6 occurrences` |

**Registration Mode is the one that matters downstream.** *Register once and attend any event*
means one registrant record spans every occurrence; *individually* means a registrant per
occurrence. That changes what the Invited and registrant lists contain for a recurring series.

A recurring webinar appears in the list view as **one row per occurrence**.

#### Co-Organizer

A plain picklist with search — **the same control as Organizer**, with two differences: the
default is `None`, and `None` is in the option list.

> **Read this before changing this field.** It has been rebuilt four times: as a tabbed
> dropdown, as a modal, as a chips-and-action control, and finally as a copy of Organizer. Each
> round treated the new instruction as an addition rather than a correction. The brief was "a
> picklist with search, like Organizer". **When a request names an existing control to copy,
> copy it and stop.**
>
> A richer multi-select panel — two source directories, invite-by-email with `+`/`−` rows,
> duplicate detection across both halves — was built and then deleted. If multi-select
> co-organisers come back as a requirement, that history is in the repo, but it is not what
> this spec asks for.

---

### Registration Setup — `With Registration`

| Field | Type | Req | Default | L | W | O |
|---|---|---|---|---|---|---|
| Registration Type | Picklist | No | `With Registration` | ✓ | ✓ | ✓ |
| Registration Form | Picklist | No | `Default Form` | ✓ | — | ✓ |
| Customize Registration Page | Picklist | No | `Standard Template` | ✓ | — | ✓ |
| Moderation Type | Picklist | No | `Automatic Moderation` | ✓ | — | ✓ |
| Set Registration Limit | Text | No | empty | ✓ | — | ✓ |
| Push Webinar Registrants to CRM | Checkbox + `Manage Config` | No | **unchecked** | ✓ | — | ✓ |
| Allow/deny registrants from specific countries | Picklist | No | `No Restrictions` | ✓ | ✓ | ✓ |
| Select Allowed Countries | Multi-select | No | — | *revealed* | *revealed* | *revealed* |
| Allow/Block Specific Domains | Picklist | No | `No Restriction` | ✓ | — | ✓ |
| Add Allowed Domains | Text | No | — | *revealed* | *revealed* | *revealed* |
| Post_Registration Custom Redirection | Text | No | placeholder `https://` | ✓ | — | ✓ |
| Post Redirection URL | Text | No | — | *revealed* | *revealed* | *revealed* |
| Allow access to join link only through mail | Checkbox | No | **checked** | ✓ | — | ✓ |
| Allow only authenticated Zoho Users with a Zoho account | Checkbox | No | unchecked | ✓ | ✓ | ✓ |
| Send Confirmation to Registrants | Checkbox | No | **checked** | ✓ | — | ✓ |
| Confirmation Email Template | Template picker | No | `Webinar Confirmation Template` | ✓ | — | ✓ |

*revealed* = rendered only once its parent field is set to a value that needs it.

```
Registration Type     With Registration · Without Registration
Registration Form     Default Form · Real Estate Form · Stock Trading Form · + Create New Form
Customize Reg. Page   Standard Template · Custom Created
Moderation Type       Automatic Moderation · Manual Moderation
Countries             No Restrictions · Allow registrants from Countries ·
                      Block registrants from Countries
Domains               No Restriction · Allow specific email domains ·
                      Block specific email domains
```

**Moderation Type matters downstream:** *Waiting for Approval* on the record's summary band
(section 4) only means anything under `Manual Moderation`.

#### Registration Form vs Customize Registration Page

Two adjacent picklists in the same column, and they are constantly confused:

- **Registration Form** — *which fields are collected* from a registrant.
- **Customize Registration Page** — *how the public page looks*.

**Registration Form.** Each option row reveals a **Preview** tag on hover, opening the form
builder's preview. `+ Create New Form` is the last option and **opens a form builder rather
than selecting anything** — a create action living inside a picklist.

**Customize Registration Page.** Each option reveals an **eye icon on hover** which opens a
full-screen preview of the public registration page. The eye must call `stopPropagation` — it
previews, it does not select the option.

The preview renders the page as a registrant sees it, and **reads the title, date and time
currently on the form**, so it reflects the webinar being created rather than fixed sample
text. It has a desktop/mobile toggle; mobile narrows the card to 420px and stacks its two
columns.

Field sets per option:

| | Standard Template | Custom Created |
|---|---|---|
| First Name | required | required |
| Last Name | required | required |
| Email Address | required | required |
| Phone Number | — | required |
| Company | — | optional |
| Portfolio Size | — | optional |

**The row follows Registration Form's visibility** — `Without Registration` removes it, since
there is no registration page to customize.

#### Push Webinar Registrants to CRM

Checkbox plus a **Manage Config** link beside the label. **Off by default.**

**This is the field that closes the loop.** Somebody who registers from the public link —
found the webinar on LinkedIn, was forwarded it, arrived from a tweet — does not exist in CRM.
Ticked, they are created as CRM records automatically and the re-import step disappears.

**Manage Config** opens the field mapping: which registration-form field lands in which CRM
field, and which module the new record is created in.

> It ships **unchecked**, which leaves the loop open unless somebody closes it. Given this is
> the single feature that most justifies the whole integration, that default is worth
> challenging — section 7.
>
> **Deduplication is not modelled at all.** When a registrant's email already matches a Lead or
> Contact, whether the existing record is updated, a duplicate created, or the registrant
> skipped is unspecified. Blocking; section 7.

---

### Registration Setup — `Without Registration`

Choosing it **removes the entire registration apparatus** — every field above except
Registration Type — and reveals three others:

| Revealed | Type | Options | Why |
|---|---|---|---|
| Who can Join | Picklist | `Anyone can Join` · `Only Authenticated Users can Join` | with no registrant list, access is decided here |
| Send thank you email to attendees | Picklist | `2 minutes after webinar ends` · `5 mins after webinar ends` · `10 mins after webinar ends` | replaces the confirmation/reminder chain |
| Thank You Email Template | Template picker | — | its template |

**It also removes the whole reminder and follow-up chain** — 1st/2nd/3rd Reminder and their
templates, both Follow-ups and their templates, and both Include Recording settings. Those
emails address a *registrant*, and there are none. Only the thank-you survives.

---

### Preferences, Reminders and Follow-Ups

| Field | Type | L | W | O |
|---|---|---|---|---|
| Allow attendees to ask questions | Checkbox | ✓ | ✓ | ✓ |
| Allow anonymous questions | Checkbox | ✓ | ✓ | — |
| Show questions to all | Checkbox | ✓ | ✓ | — |
| Auto Reply for questions | Checkbox | *revealed* | *revealed* | *revealed* |
| Automatic session recording | Checkbox | ✓ | ✓ | — |
| Video recording | Checkbox | ✓ | ✓ | — |
| Display attendee list to all | Checkbox | ✓ | ✓ | — |
| Use Emoji reactions | Checkbox | ✓ | ✓ | — |
| Post webinar Re-direction | Checkbox | ✓ | ✓ | ✓ |
| 1st Reminder | Picklist | ✓ | — | — |
| 1st Reminder Template | Template picker | ✓ | — | — |
| 2nd Reminder | Picklist | ✓ | — | — |
| 2nd Reminder Template | Template picker | *revealed* | — | — |
| 3rd Reminder | Picklist | ✓ | — | — |
| 3rd Reminder Template | Template picker | *revealed* | — | — |
| Send Follow-up Email to Attendees | Picklist | ✓ | — | — |
| Send Follow-up Email to Absentees | Picklist | ✓ | — | — |
| Attendees Follow-up Template | Template picker | ✓ | — | — |
| Absentees Follow-up Template | Template picker | ✓ | — | — |
| Include Recording for Attendees | Checkbox, unchecked | ✓ | — | — |
| Include Recording for Absentees | Checkbox, unchecked | ✓ | — | — |

*Auto Reply for questions* is revealed by *Allow attendees to ask questions*.

#### Reminder intervals — exact lists

**1st Reminder** — 11 options, default `15 mins before the webinar`, **no None**:

```
2 mins · 5 mins · 10 mins · 15 mins · 30 mins · 1 hour · 2 hours · 6 hours · 12 hours ·
1 day · 1 week      — all suffixed "before the webinar"
```

**2nd and 3rd Reminder** — 12 options: **`None`** plus the same eleven. **Both default to
`None`.**

**That is how a webinar sends fewer than three reminders.** There is no separate "number of
reminders" setting. And because the 1st has no `None`, **at least one reminder always goes out
on a registration webinar**.

#### Follow-up intervals

**Send Follow-up to Attendees / Absentees** — 9 options each, default
`2 mins after the webinar ends`:

```
None · 2 mins · 5 mins · 10 mins · 15 mins · 1 hour · 2 hours · 6 hours · 1 day
       — all suffixed "after the webinar ends"
```

Note the gaps: there is no 30 mins and no 12 hours here, unlike the reminder list. Use the
list as written.

#### Template slots

Every reminder and follow-up has its own template slot, chosen through a **Select Template**
dialog. The slot shows the chosen template's name as a preview link beside the button.

The dialog lists only templates of the matching type (section 6), and offers **+ Create
Template**, which hands off to Zoho Webinar's own editor rather than CRM's. section 6 covers
what comes back.

---

### Layout notes that were got wrong once

- **Webinar Timezone needs its own row with a label.** It was stacked under the date+time box
  inside the same form group, which left it with no label at all and floated the "Webinar Date
  & Time" label vertically between two controls. Give it a row, with an empty right-hand cell
  so the label column keeps the width every other row uses.
- **On-demand: `Allow video play/pause` belongs in the Timezone row's empty right cell**, so
  the right column reads **Video File → Allow video play/pause → Organizer**. It previously sat
  in a row of its own two rows below the file it governs.
- **Check row spacing after any structural change.** Comparing the top of consecutive rows is
  the quick test; a gap means something above closed early.

---

### Saving

**Webinar Title empty → refused**, field marked, nothing else happens. It is the only
validation on the form.

On success the record is created with `Webinar Category = Scheduled Webinar` and the user
lands on its record page (section 4).

> There is no Cancel or discard modelled on this form. section 7.

---

## 4. The scheduled webinar record

A record whose **Webinar Category** is `Scheduled Webinar`: created, not yet run. It answers
one question — *who is coming* — and it has no attendance data of any kind.

---

### The record page

**Header buttons, in order:** `Start Webinar` · `Send Invite` · `View Registration Link` ·
`Edit` · `Actions ⌄`

**Tabs:** `Overview` · `Timeline`

**Related-list rail:**
`Notes · Invited · Polls · Q&A · Recordings · Session Files · Open Activities · Closed Activities`

Rail entries carry a count badge where they have one — `Invited 100`, `Polls 2`.

**Details panel**, above the summary: Webinar Date & Time, Webinar Duration, Organiser,
Co-Organiser, Webinar Type — with a **Hide Details** toggle expanding the full *Webinar
Details* and *Registration Details* blocks (Registration Type, Registration Form, Moderation
Type, Set Registration Limit, Push to CRM, country restrictions).

> **The record page scrolls an inner element, not the window.** Its scroller caps out around
> 2820px on a scheduled record and 3812px on a completed one. Anything that scrolls this page
> programmatically must set `scrollTop` on that element, and cannot scroll past the maximum —
> content below the cap is reached through the related-list rail, not by scrolling further.

---

### Registration & Attendance Summary

A collapsible band below the Details panel. **It keeps this name in both record states**, even
though on a scheduled webinar there is no attendance in it at all.

| Block | Contents |
|---|---|
| **Registration Overview** | `10 / 200` Total Registration with a percentage ring; `190 seats left`; `5` **Waiting for Approval** with a `View →` link |
| **Registration by Module** | pie — e.g. Lead (7), Contact (2), Vendor (1) |
| **Registration by Source** | grouped bar, **Visited vs Registered** per channel |
| **Daily Registration Trend** | line — Total Registered, Peak Day, Avg / Day |

`190 seats left` is `Set Registration Limit − Total Registration`. **With no limit set there is
nothing to count down from** and the line is absent.

**Waiting for Approval only means something under `Moderation Type = Manual Moderation`.**

Each chart is clickable and opens a drill-down record list with columns
`Last Name · Created By · Created Time`.

**There is no attendance data here.** No Total Attendees, no Total Absentees, no Attendance by
Module or Source. Those four appear only after the session (section 5).

> Every drill-down currently returns "0 records" while the chart that opened it shows non-zero
> counts. The drill-downs are not wired to real data — wire them.

---

### Send Invite

The flow that connects the webinar to CRM's records. **This is the most important flow in the
feature.**

#### Step 1 — the record picker

Opens directly on a record picker: a **module dropdown** first, then a view filter, then the
records with checkboxes.

**The module dropdown is populated from *Who Can Participate From CRM*** (section 2). Only
enabled modules appear. Leads and Contacts are always there because they are locked on;
anything else appears only if an admin ticked it.

> There is no separate module-chooser step before this. It was removed — the picker opens with
> the module dropdown inside it.

#### Step 2 — the picker has two internal steps

**Tick the record rows → press `Add` → then press `Next`.**

`Add` **commits** the selection and moves to a selected-records list with a **Remove ALL**
action. Only then does `Next` do anything.

> **Pressing `Next` before `Add` does nothing at all — no error, no movement, no feedback.**
> This has cost real time twice: once building the flow, once automating it. **Fix it while you
> are here:** either disable `Next` until a selection is committed, or remove `Add` and let
> `Next` commit. Do not ship the silent version.

#### Step 3 — Mass Email

Hands off to **CRM's existing Mass Email compose step**. Out of scope to rebuild — you supply
recipients and a template.

The **Invitation Template** is chosen through a **Select Template** button, whose dialog lists
**only templates whose Email Type is `Webinar Invitation`** (section 6). The chosen template
shows as a preview link beside the button.

The dialog's second column is the **template folder** — Public Email Templates, Managerial
Templates and so on. It is not the module: every row in this picker is a webinar invitation
template already, so the module would say nothing.

> There is no "sent later, automatically" section in this compose step. It was removed.

#### Step 4 — what sending does

Two observable consequences, both of which you must implement:

1. **The invited records appear in the `Invited` related list**, each carrying All Invite
   Status and Webinar Status (section 1).
2. **An `Email` row is created in View Registration Link, and Enable Source Tracking switches
   on** (below).

---

### View Registration Link

Opens the public registration link and, beneath it, the list of tracked sources.

**A webinar nobody has been invited to has no sources at all.** The table is empty and
*Enable Source Tracking* is off. This is deliberate: a brand-new webinar should not chart
registrations from channels that do not exist yet.

Completing Send Invite creates the first source:

| Column | Value |
|---|---|
| Source | `Email` |
| Created by | the sending user |
| Visited | 0 |
| Registered | 0 |
| Status | enabled |

**Enable Source Tracking switches itself on** when the first source is created, because a
source with tracking off records nothing.

**A second Send Invite does not add a second `Email` row.** Guard the creation against
duplicates: one channel, one row.

> Implementation note: the source list must be owned by the record, not by the modal. Built as
> modal-local state it starts empty every time the modal opens, and anything created dies when
> it closes.

---

### Polls

Polls are **written before the session and answered during it**. On a scheduled webinar they
exist but have no results.

**Create Poll** opens the editor. A poll has a question, a set of answer options, and a type:

| Type | Behaviour |
|---|---|
| Multiple choice | one answer from a list |
| Short answer | free text |
| Checkbox | several answers from a list |

The Polls rail entry carries a count badge once polls exist. section 5 covers the answered state.

---

### Session Files

The webinar's attachments — slides, handouts, recordings, promotional assets.

| Column | Example |
|---|---|
| File Name | `Webinar_Slides_Q3.pdf` *(with a type icon)* |
| Size | `3.2 MB` |
| Date Added | `Sep 4, 2025` |

**Session Files is not Recordings.** Recordings is its own rail entry and reads
*"No recordings available."* in both record states. A recording uploaded as a session file is
a different object from the automatic session recording produced by the Preferences toggle.

> No upload control, size limit, permitted file types or delete action is modelled. The list is
> read-only. You will need all four — section 7.

---

### Actions

The overflow menu in the record header, beside Edit. **Thirteen items, in this order:**

| # | Item | Notes |
|---|---|---|
| 1 | **Cancel Webinar** | **in red.** Yours to build — see below |
| 2 | Clone | standard CRM |
| 3 | Share | standard CRM |
| 4 | Delete | standard CRM |
| 5 | Share via Cliq | standard CRM |
| 6 | Print Preview | standard CRM |
| 7 | Customize Business Card | standard CRM |
| 8 | Organize Campaign Details | standard CRM |
| 9 | Add Related List | standard CRM |
| 10 | Add Kiosk ✨ | standard CRM; ✨ marks a Zia/AI item |
| 11 | Create Button | standard CRM |
| 12 | Create Client Script ✨ | standard CRM |
| 13 | View Followers | standard CRM |

**Items 2–13 come free with being a module.** Do not reimplement them. Only item 1 is yours,
and only item 1 is conditional.

#### Cancel Webinar — the only conditional item

| Record | Label | Behaviour |
|---|---|---|
| One-off, not completed | `Cancel Webinar` | opens a confirm |
| **Recurrent**, not completed | `Cancel` | opens a **choice modal**: this occurrence / all future occurrences |
| **Completed** | **absent** | there is nothing left to cancel |

Cancelling sends the cancellation email to registrants (section 6).

> The menu is clipped at the right edge of the viewport when the record page is narrow. It is
> positioned `right: 0` against a container that does not account for its width. Fix the
> positioning; do not shorten the labels.

---

## 5. The completed webinar record

A record whose **Webinar Category** is `Completed Webinar`. It answers a different question
from the scheduled one: not *who is coming* but **what did we get**.

---

### What changes from scheduled

**Header:** `Start Webinar`, `Send Invite` and `View Registration Link` are **gone**. Only
`Edit` and `Actions ⌄` remain, and `Cancel Webinar` is absent from the Actions menu.

**Rail:** unchanged.

**Body:** the Registration & Attendance Summary fills in its attendance half, an **Attendees
and Registrants List** appears, and a **Webinar Revenue** band appears that a scheduled record
does not have.

---

### Registration & Attendance Summary

Same band as section 4, now complete.

**Registration Overview carries three figures instead of one:**

| Figure | Example |
|---|---|
| Total Registration | `30` |
| Total Attendees | `15 (50%)` |
| Total Absentees | `15 (50%)` |

Formulas in section 1. Attendees and absentees must sum to registrations; the percentages are of
Total Registration.

**Four charts, where a scheduled record had two.** Attendance is added *alongside* registration
rather than replacing it, so the same cut can be compared before and after:

| Chart | Example segments |
|---|---|
| Attendance by Module | Lead (10), Contact (3), Vendor (2) |
| Attendance by Source | Email (8), Twitter (4), LinkedIn (3) |
| Registration by Module | Lead (7), Contact (2), Vendor (1) |
| Registration by Source | Twitter (4), Email (3), LinkedIn (2), Direct (1) |

Plus Daily Registration Trend, as before.

---

### Attendees and Registrants List

**Six tabs, each with its own count:**

```
All Attendees · All Absentees · All Registrants ·
Approved Registrants · Unapproved Registrants · Denied Registrants
```

The last three only mean anything under `Moderation Type = Manual Moderation`.

**Columns:**

```
Last Name · Email · All Modules · All Sources · Polls · Q&A · Registered Date · Webinar Status
```

| Column | Values |
|---|---|
| Webinar Status | `Attended` / `Not Attended` |
| Polls | count of polls that person answered |
| Q&A | `Yes` / `—` |
| All Modules | the CRM module, or **`—` for somebody who came through the public link** |

**Polls and Q&A in this table turn it into an engagement ranking, not just an attendance
register.** Somebody who attended, answered three polls and asked a question is a different
prospect from somebody who attended silently, and this list is where that shows.

`All Modules` and `All Sources` are column-header filters.

> **The sample data in the mock does not reconcile and must not be copied.** Registration
> Overview says 30 / 15 / 15; the tabs say 13 attendees, 6 absentees, 14 registrants; the table
> paginates "1 – 10 of 11 records"; the module segments total 15 and 10. **Build the
> relationships** — attendees + absentees = registrants, segments sum to their total — not
> these numbers.

---

### Webinar Revenue

The band a completed record gains, and the reason **Webinar Cost** exists.

**Collapsed by default, and not in the related-list rail.** It is reachable only by scrolling
the record body and expanding it. That is deliberate — it is reporting, not a related list —
but it means the feature's headline numbers have no shortcut. section 7 asks whether that is
right.

#### Webinar ROI — six tiles

| Tile | Example | Derivation |
|---|---|---|
| Cost | `$2,500` | **Webinar Cost** from the create form |
| Revenue (Won) | `$16,800` | Σ amount of the Deals Won table |
| ROI | `+572%` | `(Revenue − Cost) / Cost` |
| In Pipeline | `$32,450` | Σ amount of open influenced deals |
| Cost / Attendee | `$167` | `Cost / Total Attendees` |
| Revenue / Attendee | `$1,120` | `Revenue / Total Attendees` |

The worked example and the division guards are in section 1. **Those formulas are the
specification** — the numbers above are a consistent set you can test against.

#### Two charts

| Chart | Segments |
|---|---|
| Pipeline by Stage | Proposal Sent (7), Negotiation (5), Closed Won (9), Closed Lost (3), Waiting for Manager (4) |
| Deals Won by Source | Twitter (4), Email (3), LinkedIn (2), Direct (1) |

#### Two tables

**Deals Won** and **Deals in Pipeline**, same shape:

```
Deal Name · Amount · Stage · Account Name · Contact Name
```

**Deal Name, Amount, Account Name and Contact Name all render as links into their CRM
records.** That is the point of having this panel inside CRM rather than in the webinar tool —
every figure is one click from the record behind it.

> **Which deals appear, and at what amount, is decided by the attribution model** (section 2).
> With Linear, a deal influenced by three webinars contributes a third of its amount to each.
> **Whether Amount shows the deal's full value or its attributed share is unspecified**, and
> the two produce ROI figures that differ by a factor of three in that example. Blocking —
> section 7.

---

### Invited related list

The record of who was invited from CRM and what became of them — the direct output of Send
Invite.

**Tabs, each with a count:**

```
All Modules · Invited · Registered · Not Registered · Attended · Not Attended
```

Six tabs makes the funnel readable in one line: how many were invited, how many registered,
how many turned up.

**Columns:**

| Column | Example |
|---|---|
| Name | the record's name |
| Email | the record's email |
| Module | `Leads` / `Contacts` / … |
| All Invite Status | `Registered` / `Not Registered` |
| Webinar Status | `Attended` / `Not Attended` |
| Invite Sent on | user + timestamp |

**The two status columns answer different questions** — see section 1. A row reading
`Registered` + `Not Attended` is a no-show, and that is exactly the population the Absentees
follow-up email addresses.

#### This list and the Attendees list are not the same population

**Invited** is the CRM half of the funnel. **Attendees and Registrants** is the webinar half.

- Somebody invited from CRM who never registered appears in **Invited** only.
- Somebody who found the public link appears in **Attendees and Registrants** with Module `—`
  and **never appears in Invited at all**, because they were never invited from CRM.

**Neither list is a superset of the other.** Do not implement one as a filtered view of the
other.

---

### Polls, answered

**Poll Answered by** tabs cut the results by who answered:

```
All Modules · Leads · Contacts · Vendors · Not in CRM
```

Each poll shows its question, every option with its vote count as a bar, then two summary
figures: **% Voted** and **Total Votes**.

Clicking through opens the respondent list — `Name · Email · Company · Phone · Owner`.

**That respondent list is what makes a poll answer actionable.** A five-star rating attached to
a named Lead is a follow-up; the same rating as an anonymous statistic is not.

**The `Not in CRM` tab is the important one.** Respondents who arrived through the public link
have no CRM record, so their answers cannot be attributed to anyone — *unless* **Push Webinar
Registrants to CRM** was ticked (section 3), in which case they will have been created as
records and the tab will be near-empty. The two features are connected; that tab is the visible
cost of leaving the push off.

> The mock's poll numbers do not add up — option counts do not sum to Total Votes and both
> polls report identical figures. Define the relationship between option counts, Total Votes
> and % Voted yourself; do not copy the sample.

---

### Q&A

The questions asked during the session and the host's answers.

**Tabs:** `Overall Q&A · Leads · Contacts · Not in CRM` — the same cut as Polls.

**A participation summary heads the section:** Participated in Q&A, then a breakdown by
Leads / Contacts / Not in CRM.

**The transcript is a threaded conversation, not a table.** Each entry carries:

- an avatar with the asker's initials
- the asker's name
- a timestamp
- **their CRM module as a tag**
- the question text

A host answer is **nested underneath**, marked `Host` with the responder's name.

```
JS  jonam suriya · 11:08 AM · Leads
    "What does the Enterprise plan cost per seat?"
    J  Host · 11:09 AM · Jay
       "Our Enterprise plan starts at $49/seat/month — we can share a detailed
        pricing deck after the session."
```

**Not every question has an answer, and that is real behaviour rather than missing data.** An
unanswered question is a follow-up somebody still owes. Render it as an unanswered question;
do not hide it and do not fabricate an answer row.

**The module tag is what justifies having this in CRM at all.** *"A Lead asked about Salesforce
integration"* is a sales signal attached to a record. The same sentence in a webinar transcript
is not.

> **There is no action on a question** — no convert-to-task, no assign, no mark-answered. Given
> the transcript deliberately contains unanswered questions, that is the obvious missing step.
> section 7.

> The mock's Q&A tab counts sum to 19 against a stated 21 participants. Build the relationship,
> not the numbers.

---

## 6. Lifecycle emails and their templates

Eight emails surround a webinar. Each is a **template type**, and the type decides two things:
which links the template may carry, and which link it **must** carry. Get those rules wrong and
you ship an invitation nobody can register from.

**Out of scope:** CRM's email template editor itself. You are adding template *types* and their
rules, not a new editor.

---

### The eight emails

| # | Email | When it goes out | To |
|---|---|---|---|
| 1 | **Webinar Invitation** | when you invite CRM records | CRM records — *before anyone has registered* |
| 2 | **Confirmation Email** | the moment somebody registers | the registrant |
| 3 | **1st Reminder** | at the interval set on the webinar | registrants |
| 4 | **2nd Reminder** | ditto | registrants |
| 5 | **3rd Reminder** | ditto | registrants |
| 6 | **Attendees Follow-up** | after the session | everyone who attended |
| 7 | **Absentees Follow-up** | after the session | registrants who did not turn up |
| 8 | **Webinar Cancelled** | if the webinar is called off | registrants |

**The invitation is the odd one out, and the reason matters.** It goes to a CRM record *before
that person is a registrant*, so it cannot merge registrant fields and cannot carry a Join URL
— there is no registration to join yet. Everything from the confirmation onwards addresses a
registrant and can.

**6 and 7 are a partition of the registrants**, decided by attendance. Every registrant gets
exactly one of them.

---

### Link rules — the part to get right

**`TPL_TYPE_LINKS` — which links a type may insert.** Insert Link and Insert Button offer only
these, per type:

| Type | Allowed links |
|---|---|
| **Webinar Invitation** | Web URL, Email, **Registration Link**, Add To Calendar, Add To Google Calendar, Add To Yahoo Calendar, Add To Outlook Calendar, Add To Zoho Calendar |
| **Confirmation Email** | Web URL, **Join URL**, Cancel Registration, + all five calendar links |
| **1st / 2nd / 3rd Reminder** | Web URL, **Join URL**, Cancel Registration, + all five calendar links |
| **Attendees Follow-up** | Web URL, Join URL, **Recording Link**, + all five calendar links |
| **Absentees Follow-up** | Web URL, Join URL, **Recording Link**, + all five calendar links |
| **Webinar Cancelled** | **Web URL, Email — and nothing else** |
| **None** | everything: Web URL, Email, Registration Link, Join URL, Cancel Registration, Recording Link, + all five calendar links |

The five calendar links are always: `Add To Calendar`, `Add To Google Calendar`,
`Add To Yahoo Calendar`, `Add To Outlook Calendar`, `Add To Zoho Calendar`.

**`TPL_REQUIRED_LINK` — what a type must contain, enforced on save:**

| Type | Required link |
|---|---|
| Webinar Invitation | **Registration Link** |
| Confirmation Email | **Join URL** |
| 1st Reminder | **Join URL** |
| 2nd Reminder | **Join URL** |
| 3rd Reminder | **Join URL** |
| Attendees Follow-up | **Recording Link** |
| Absentees Follow-up | **Recording Link** |
| Webinar Cancelled | *(none)* |
| None | *(none)* |

**Saving a template that lacks its required link is refused.** That is the only content
validation on a template.

#### Why the rules are shaped this way

- **The invitation gets Registration Link and not Join URL** because its reader has not
  registered. Offering a join link to somebody with no registration is a dead end.
- **Confirmation and reminders get Join URL and Cancel Registration** because their reader *has*
  registered — they can join, and they can change their mind.
- **Follow-ups get Recording Link** because the session is over; the only thing left to offer is
  the recording. They keep Join URL as an allowed link, but it is not what they are for.
- **Webinar Cancelled gets almost nothing.** There is nothing to join, register for or watch.
  Two links only.

---

### Merge fields

`#` in the editor opens the merge-field picker. Its **source list depends on the type**:

**Webinar Invitation** offers, in order:

```
Webinar Details · Users · Organization        (+ the recipient module's own fields)
```

**Every later email adds `Registrations` above Webinar Details**, because it addresses a
registrant rather than a CRM record:

```
Registrations · Webinar Details · Users · Organization
```

#### The sources, verbatim

**Webinar Details** — `Webinar Title`, `Webinar Date & Time`, `Webinar Organiser`,
`Webinar Duration`, `Description`

**Registrations** — `Registration Id`, `Country`, `Created By`, `Created Time`, `Email`,
`First Name`, `Modified By`, `Timezone`, `Add To Google Calendar`, `Add To Yahoo Calendar`,
`Add To Outlook Calendar`, `Add To Zoho Calendar`, `Add To Calendar`, `Join URL`, `Handouts`,
`Cancel Registration`, `Audio Details`, `Registration URL`, `Full Name`, `Last Name`,
`Abuse Email`, `iOS app URL`

**Users** — `User Id`, `User Name`, `Email`, `Role`, `Profile`

**Organization** — `Company Name`, `Website`, `Phone`, `Street`, `City`, `State`, `Country`

**General** — `Current Date`, `Current Time`, `Unsubscribe Link`, `View in Browser`

Recipient-module sources carry that module's own fields — Leads offers `Lead Id`,
`Lead Owner`, `Company`, `First Name`, `Last Name`, `Title`, `Email`, `Phone`, `Mobile`,
`Lead Source`, `Industry`, `City`, `State`, `Country`; Contacts offers the equivalent with
`Account Name`, `Department` and mailing address fields.

#### Templates are module-scoped

**An email template belongs to a module, and its merge fields resolve against that module's
record.** A template's module must therefore match its recipient's module. This is standard CRM
behaviour and it is why the invitation's merge sources include the recipient module while the
later emails lead with Registrations.

> Known gap in the mock: the merge-source list leads with `Registrations` for anything whose
> type is not Webinar Invitation, **including plain non-webinar templates**, so a Contacts
> template offers registrant fields rather than the module's own. Scope the Registrations
> source to webinar template types only.

---

### Where templates live

**Setup ▸ Templates** lists them under the **Zoho Webinar** module. The webinar's default set
also appears under **Modules and Fields ▸ Zoho Webinar ▸ Preferences**.

#### The list

Eight shipped rows, one per lifecycle email, **in lifecycle order with Webinar Cancelled
last** — it only goes out if the webinar is called off, so it belongs at the end rather than
at the top.

Each row's subline carries the module, what the email is for, and its type as a third segment:

```
Zoho Webinar · Sent when you invite CRM records to a webinar · Invitation template
```

**The Email Type is a segment of that subline, not a column.** A column that exists for one
module leaves a hole in the table for every other module. Non-webinar rows simply have no third
segment.

> This means there is no way to filter the list by email type. A filterable Email Type column
> was built and removed for the reason above. If filtering comes back as a requirement, solve it
> without a module-specific column.

#### One row per lifecycle email

**Selecting a template for a use case renames the existing row; it never adds a second.** Pick
"Long-form invite" for the invitation and the Invitation row becomes *Long-form invite ·
Invitation template*. Pick the Default back and it returns to *Webinar Invitation Template*.
The count stays eight.

> Getting this wrong produces two rows for one email — the shipped row and the custom you just
> chose — which reads as though both are live. The row stands for *the email*, not for *a
> template*.

A consequence to know: **a custom template that is saved but not currently live has no row of
its own.** The list is a view of what each email is set to; the templates themselves live in the
gallery.

#### Row actions

- **Clicking the name** opens a read-only **preview** (with Preview / Analytics tabs).
- **A pencil icon appears on row hover**, in the column just before the type segment, and opens
  that template in the editor.
- The **shipped defaults are read-only** and have no pencil — their pencil opens **Zoho
  Webinar's own editor in a new tab** instead (below).

---

### Creating a template

**Setup ▸ Templates → + New Template** branches on the module filter:

| Filter | Opens |
|---|---|
| **Zoho Webinar** | the **Email Notification gallery** — a rail of the eight lifecycle emails, each with its Default, its saved customs, and the Basic layouts |
| anything else *(including All Modules)* | the standard **Create Email Template** dialog |

The gallery's rail entry sets the use case, which stamps the type, which sets the required link
and the allowed link list from the start.

#### The Create Email Template dialog

For non-webinar modules: **Select Module** first. When the module is **Zoho Webinar**, an
**Email Type** row appears beneath it — the type means nothing for an ordinary module, so it is
revealed rather than always shown. Its options are the eight lifecycle emails, labelled as the
list labels them.

**Next** carries the choice through: the gallery opens on that use case with its rail entry,
chip and note, and the type is stamped before the editor opens.

> The field is called **Email Type**, not "Template Type" — it names *which lifecycle email
> this is*, and "Template Type" restated the noun already in the dialog title.

#### New templates start blank

Name and subject are **real, empty inputs** with placeholders `Untitled template` and
`Add a subject` — not prefilled with the type name or an invented "Webinar Invite - <Module>".

**Saving with no name is refused inline in the Save dialog** — not as a toast, because the
editor's toast renders behind that modal's scrim.

The Save dialog asks **Template Name** and **Save To**, a folder picklist of the real CRM
template folders with a separated **+ New Folder** row that takes a name inline. **A folder is
required**; saving without one is refused the same way.

> The body's "Write the … email here" prompt must be a real CSS placeholder, not grey content.
> As content, typing merges into it and it gets saved into the email.

---

### Creating a template from a create-webinar slot

`+ Create Template` inside a slot's Select Template dialog **does not open CRM's gallery**. It
opens **a new tab on Zoho Webinar's own domain** — its Email customization screen, showing the
rail of six lifecycle emails with that slot's email in bold, the Quick Templates Default, any
customs already saved for it, and the Basic layouts.

**Save hands the template back and closes the tab**: the child calls back into the opener with
the new template's name and slot, which pushes it into the created set, adds a Setup ▸ Templates
row with its Email Type, selects it for the slot, and reopens the picker on it. Then the child
closes itself.

> The child is same-origin, which is what makes the callback possible.
>
> **Never use `alert()` on the pop-up-blocked path.** A modal dialog freezes the whole renderer
> until somebody dismisses it by hand — it has cost a frozen tab here. Use a toast.

The Select Template dialog's folder dropdown is a **static "Zoho Webinar" label with no caret**
— every template it lists is a webinar template, so there is nothing to filter.

---

### What a created template must be able to reach

A template created anywhere must be selectable everywhere it is valid. Specifically: one
created inside the Send Invite flow must appear in the Select Template picker **in the step that
created it**. Push it into the Templates list at creation, not only into the editor's own state.

---

## 7. What is genuinely undecided

Everything here is unspecified in the source material. **Do not resolve any of the Blocking
items by guessing** — each one changes what the code does in a way that is expensive to undo.

For the rest, a reasonable default is suggested. Take it, and say in your handoff that you did.

---

### Blocking — work cannot be finished without an answer

#### 1. Webinar Cost means two contradictory things

Its tooltip reads *"This is the amount attendees will be charged to register for this
webinar"* — i.e. **revenue**. The ROI panel uses it as **what the webinar cost to run**: the
denominator, in a tile labelled `Cost`, beside a separate `Revenue (Won)` tile fed by closed
deals.

Both cannot be true.

**The ROI arithmetic is self-consistent** — `(16800 − 2500) / 2500 = +572%`, and both
per-attendee tiles divide by attendees — which makes the **tooltip the more likely error**.
But a paid webinar genuinely does have a ticket price, and if that is what this field is,
the ROI panel is missing its cost input entirely.

Affects: section 3 (the field), section 5 (every ROI tile), section 1 (the formulas).

#### 2. Time Decay has no curve

`Increasing Time Decay` and `Decreasing Time Decay` state a *direction* and nothing else. No
decay function, no half-life, no worked example. They cannot be implemented as written.

They also **read inverted** against the usual meaning of the term: "Increasing Time Decay"
gives *more* credit to *earlier* webinars, where time decay conventionally favours the recent.
Decide whether the names or the descriptions are wrong before implementing either.

Affects: section 2, section 5.

#### 3. Attributed share vs full amount in Deals Won

With Linear, a deal influenced by three webinars contributes a third of its amount to each.
**Whether the Deals Won table shows the deal's full value or its attributed share is
unspecified** — and the two give ROI figures three times apart in that example.

The headline number of the entire feature depends on this.

Affects: section 5, section 1.

#### 4. Push to CRM has no deduplication rule

When a registrant's email already matches an existing Lead or Contact, it is unspecified
whether the existing record is **updated**, a **duplicate created**, or the registrant
**skipped**.

This is the feature that most justifies the integration; shipping it with the wrong answer
pollutes the CRM database, which is worse than not shipping it.

Affects: section 3.

---

### Product decisions

| # | Question | Suggested default |
|---|---|---|
| 5 | Should **Push Webinar Registrants to CRM** default to on? It is the feature that most justifies the integration and it ships unchecked. | Raise it; do not change the default unilaterally |
| 6 | **Re-inviting** a record already invited — allowed, resends, or refused? | Allow, and resend; show the previous send date |
| 7 | Does **attribution count attendance or registration**? section 5 divides by attendees, implying attendance, but a no-show who watched the recording was arguably influenced too | Attendance |
| 8 | What happens to **already-invited records when a module is turned off** in Who Can Participate? | Existing invites stand; the module simply stops being offered |
| 9 | Does an **on-demand** webinar really get no reminders and no follow-ups? It still has a date and still takes registrations, so its registrant gets a confirmation and nothing else | Confirm — it looks like a consequence of reusing the live form's visibility rules |
| 10 | **Send failure** in Mass Email — no template chosen, no recipients left after Remove ALL, a transport error — has no modelled state | Block send with an inline reason; never fail silently |
| 11 | **Removing every selected record** in the picker's step 2 — is Next blocked, or does it return to the record table? | Block Next, keep the user where they are |
| 12 | **No invitation templates exist** — does Select Template offer inline creation, or does the flow stall? | Offer `+ Create Template` in the empty state |
| 13 | **Cancel on re-entry**: Cancel returns to the introduction page, but for an already-enabled integration it should arguably return to the enabled panel | Return to the enabled panel when enabled |
| 14 | The three **blocking modals have no stated exit** — only the not-an-admin modal's button is named | All three dismiss back to the Marketplace card |
| 15 | **Save on the enabled page** has no success or failure state; the dirty-state bar is named, its outcome is not | Toast on success; keep the bar and show the reason on failure |

---

### Engineering

| # | Item |
|---|---|
| 16 | **Attendance Count / Attend. Rate must distinguish "not yet known" from zero.** The list view renders `—`, not `0`. Do not store either as `0` |
| 17 | The record page **scrolls an inner element**, capped ~2820px scheduled / ~3812px completed. Reaching content past the cap is done through the related-list rail |
| 18 | **All summary-chart drill-downs currently return 0 records** while their charts show non-zero counts. They are not wired to data |
| 19 | **Webinar Revenue is collapsed by default and absent from the rail** — the feature's headline numbers have no shortcut. Deliberate, but worth revisiting |
| 20 | **Guard every ROI division**: zero attendees, zero or empty cost. Render the tile empty, never `∞` or `NaN` |
| 21 | **Session Files has no upload, size limit, type restriction or delete.** All four are needed |
| 22 | **No action on a Q&A question** — no convert-to-task, no assign, no mark-answered — while the transcript deliberately contains unanswered ones |

---

### Design

| # | Item |
|---|---|
| 23 | **`Next` does nothing before `Add`** in the Send Invite picker — no error, no movement. Disable Next until a selection is committed, or drop Add. **Do not ship the silent version** |
| 24 | The **Actions menu clips** at the right edge of the viewport on a narrow record page |
| 25 | The **Registration & Attendance Summary keeps its name on a scheduled record** where there is no attendance data |
| 26 | **No back navigation in the setup wizard.** Only Cancel and Next exist, yet every answered step stays on screen with its fields live — a user can see an earlier answer but has no way to return to it |
| 27 | **No Cancel or discard on the create form.** Only Save is modelled |
| 28 | **Manage Config has no stated exit** — what closes it, whether it can be cancelled |

---

### Assumptions this spec makes

- **The three account-blocking cases are driven by a demo switcher in the source material.**
  Real behaviour is assumed to come from the user's Zoho Webinar account state and CRM role.
- **Field lists, types, defaults and option lists were extracted from the source prototype's
  DOM and its own constants**, not transcribed by hand. Where a control is custom — Repeat
  Webinar, template slots — the type column says so rather than guessing a primitive.
- **Sample values are placeholders.** Names (`Rao Priya`, `Jayasuriya`), counts, amounts and
  dates illustrate shape only. The one exception is the ROI worked example in section 1, which is
  a consistent set deliberately included so you can test your arithmetic against it.
- **API names are not specified anywhere in this set.** Fields are named by their UI label
  because that is what the source material carries. Agree the API names with whoever owns the
  module schema before building; do not derive them mechanically from the labels.

---

### Sample data that is wrong — do not reproduce

The prototype's numbers do not reconcile. **Build the relationships, not these values.**

| Where | The contradiction |
|---|---|
| Completed summary | Overview says 30 registered / 15 attended / 15 absent; tabs say 13 attendees, 6 absentees, 14 registrants; the table paginates "1 – 10 of 11 records"; module segments total 15 and 10 |
| Q&A | Tab counts sum to 19 against a stated 21 participants |
| Polls | Option counts do not sum to Total Votes, and both polls report identical figures |
| Webinar Revenue | Pipeline by Stage shows 9 Closed Won against 7 rows in the Deals Won table |
| Invited | "Invite Sent on" reads `Matchendran on Jan 28, 2022` — a user and a date unrelated to the record's 2025 data |
| Registrant list | A webinar whose only channel is Email still carries rows sourced LinkedIn, Twitter and Direct |

The correct relationships:

```
attendees + absentees          = registrants
Σ chart segments               = the total that chart is of
Σ Deals Won amounts            = Revenue (Won)
Pipeline by Stage "Closed Won" = row count of Deals Won
```

---

## 8. Decisions already made, and what was rejected

Read this before renaming anything or "improving" a label. Most of what follows looks
arbitrary until you know what it replaced.

---

### Naming rules

#### 1. Keep the product's vocabulary in the label

If the user sees a phrase on the record, in the list view, in filters and on the calendar, the
control that acts on it must contain those words. A label that reads better in isolation and
leaves this screen as the only place in CRM calling the thing something else is worse, however
elegant.

#### 2. Name the decision, not the data structure

**"Zoho Webinar Invite Modules" → "Modules You Can Invite" → "Who Can Participate From CRM".**

The first named the data structure. The second read as a category rather than a choice. The
third names the decision being made — *who is in the room, and that they come from CRM*.

The heading and subline then swapped jobs: the heading carries the intent, the subline the
mechanism.

> **The word "invite" is deliberately absent from that section's heading and subline.**
> Mechanically the setting gates who can be invited, but the section states intent. Do not
> reintroduce it.

#### 3. Name what the button does, not what the page is about

**The introduction page's action reads `Setup`, not `Enable Integration`.** It does not enable
anything — it opens the wizard, and enabling happens at the end of that. The old label promised
an outcome one click too early.

#### 4. "Email Type", not "Template Type"

The field names *which lifecycle email this template is*. "Template Type" restated the noun
already in the dialog's title.

---

### Structural decisions

#### The account check belongs at the marketplace card

Originally the card always opened the introduction page and the account check ran on *that*
page's Setup button — so a user who could not have the integration was shown a page selling it
to them first. The check now runs before anything is rendered, with a second copy on the
introduction page's button as a guard.

#### Wizard steps accumulate rather than replace

Replacing each step with the next meant a decision could not be re-read while the next one was
being made. Answered steps now stay on screen, and only the step in play shows its buttons — a
pair of buttons under a settled section suggests it is still open.

#### The steps are shown and hidden in place, not routed

Deliberate: the final action reads every answer out of the DOM, so every earlier field has to
still exist at the end. If you rebuild this as a router, carry the answers in state instead.

#### Who Can Participate lists only person-shaped modules

Accounts, Potentials, Cases, Campaigns and Meetings were removed: a company, a deal, a ticket,
a campaign and an event cannot attend a webinar. What replaced them are the modules a business
builds to hold *people* — Vendors, Donors, Volunteers, Members, Students, Alumni, Partners,
Speakers, Referrals, Patients, Subscribers.

**Any module added here in future must pass the same test.**

> Known consequence: the Send Invite module list is intersected with this one. A module present
> in one and not the other silently cannot be invited. Keep the two lists in step.

#### Sync past webinars is radios, not a picklist

A binary question behind a click hides one of its two answers.

#### Webinar Cancelled is listed last

It is the eighth row, after Absentees Follow-up, matching the order of the gallery's rail. The
list shows all eight lifecycle emails from the start, and the cancellation email sits at the end
because it only goes out if the webinar is called off.

Previously it had no row at all and appeared at the *top* the first time something was selected
for it, because new rows were unshifted.

#### One row per lifecycle email

A row stands for *the email*, not for *a template*. Selecting a custom renames the row; it never
adds a second. Two rows for one email reads as though both are live.

#### Email Type is a subline segment, not a column

A column that exists for one module leaves a hole in the table for every other module. The type
reads as the tail of the row's own subline instead, and non-webinar rows simply have no third
segment.

**This removed the ability to filter by email type.** That was the accepted cost.

#### A new webinar has no registration sources

A brand-new webinar charts nothing, because it has no channels yet. The first source is created
by the first Send Invite. Seeding defaults would chart registrations from channels that do not
exist.

#### On-demand: Allow video play/pause sits under Video File

Moved out of a row of its own so the right column reads **Video File → Allow video play/pause →
Organizer**, putting the setting next to the file it governs rather than two rows away.

---

### Rejected, with the reason

| Rejected | Why |
|---|---|
| **"Notify Super Admin"** button on the not-an-admin modal | CRM cannot actually send that mail. The button promised something the product does not do |
| **A filterable Email Type column** in the Templates list | Module-specific column, hole in the table for every other module |
| **Multi-select co-organisers** — two source directories, invite-by-email with `+`/`−` rows, duplicate detection across both halves | Built over four rounds and deleted. The brief was "a picklist with search, like Organizer". See below |
| **A module chooser step** before the Send Invite record picker | The picker opens with the module dropdown inside it |
| **"Sent later, automatically"** section in Mass Email | Removed from the compose step |
| **A "<Module> only" chip** dimming non-matching templates in the Select Template picker | Solved an edge case nobody raised, and was the only thing on the row not in the reference dialog |
| **Prefilled template name and subject** | Three defaults the user never chose. New templates start blank |
| **The folder dropdown** in the create-webinar slot's Select Template dialog | Every template it lists is a webinar template; there was nothing to filter. It is a static label now |

#### The co-organiser field — four rounds, one lesson

It was built as a tabbed dropdown, then a modal, then a chips-and-action control, then a
multi-select panel, and finally deleted in favour of **a plain copy of the Organizer picklist**.

Each round treated the new instruction as an *addition* to the last reading rather than a
*correction* of it. The original brief was "a picklist with search, like Organizer".

> **When a request names an existing control to copy, copy it and stop.**

---

### Traps that cost real time

**An unbalanced `<div>` does not throw.** It silently reparents everything after it. A single
extra `</div>` in a form field closed its row early and left a 519px hole in the layout. Walking
`<div>`/`</div>` with a running depth counter over the changed block finds it in one pass;
eyeballing the markup twice did not. **Check depth after any markup swap, and compare the tops
of consecutive rows for gaps.**

**Never use `alert()`, `confirm()` or `prompt()`.** They freeze the renderer until dismissed by
hand. An inline control or a toast does the job without blocking.

**The create form's scroller caps around 770px**, so Preferences, Reminders and Follow-Ups all
occupy one screenful. The record page's caps around 2820px (scheduled) and 3812px (completed).
Content past a cap is reached through the rail, not by scrolling.

**A dropdown containing a search box needs its own minimum width.** Inheriting the trigger's
width clips the search field.

**Anything inside a dropdown must stop propagation** — click and keydown both. Without it the
first keystroke or click reaches the trigger behind and closes the dropdown.

**React renders a tick late.** Anything reading the DOM immediately after a state change gets
the previous state.

---

### The verification habit

Every structural change to a form or record page was checked three ways before being called
done, and the same habit will serve you:

1. **Row tops run contiguously** — no gap where a container closed early.
2. **The variant actually switched** — count the visible fields, do not assume the branch fired.
3. **The value survived the round trip** — read it back after the change, not before.
