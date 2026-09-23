# 01 — The module, its entities and every derived value

Read this before anything else. The rest of the set assumes these names and these formulas.

---

## Zoho Webinar is a CRM module

Not an embedded app, not a page — a module, with everything that implies: records, an owner,
a list view, a record detail page, related lists, layouts, email templates, and standard
record actions. It appears in the left rail alongside Leads, Contacts and Meetings once the
integration is enabled (file 02), and not before.

**Nothing in the module is reachable until the integration is enabled.** That is the only gate.

### Webinar Category — the field that drives everything

Every webinar record carries **Webinar Category**, a picklist with three values:

| Value | Meaning |
|---|---|
| `Scheduled Webinar` | Created, not yet run |
| `Completed Webinar` | Has run |
| `On-Demand Webinar` | A recorded session, played on demand |

**Which record page a webinar shows follows from this field, not from comparing its date to
now.** A scheduled record shows Start Webinar / Send Invite / View Registration Link in its
header and gains none of the revenue reporting. A completed record loses all three of those
buttons and gains the Webinar Revenue band. Files 04 and 05 cover the two states.

Do not compute the state from the date. A webinar whose time has passed but which was never
run is not automatically completed — the category is what says so.

---

## Entities

### Webinar

The module record. Its full field list is file 03 — 63 fields, because the create form *is*
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
| Webinar Cost | Currency-ish text | every ROI figure in file 05 |
| Registration Type | Picklist — `With Registration` / `Without Registration` | whether registrants exist at all |
| Set Registration Limit | Number | seats-left arithmetic |

### Registrant

Created when somebody signs up. Holds their name, email, the **source** they arrived through,
their registered date, and — after the session — whether they attended.

A registrant **may or may not** correspond to a CRM record. One who came through the public
link is not in CRM unless *Push Webinar Registrants to CRM* was on (file 03). A registrant
with no CRM record shows an em dash in the Module column.

**After the session every registrant is exactly one of: attendee or absentee.** That partition
is what decides which follow-up email they receive (file 06).

### Invitee

Distinct from Registrant, and the distinction is load-bearing. An **invitee** is a CRM record
that was sent an invitation through Send Invite (file 04). It carries:

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

### Registration Source

A tracked channel a registration can arrive through. Holds source name, created-by, visited
count, registered count, enabled flag.

**A new webinar has no sources at all** — the list is empty, not seeded with defaults. The
first one is created by completing Send Invite, which creates a source named `Email` and
switches *Enable Source Tracking* on. A second Send Invite does **not** create a second row;
the creation is guarded against duplicates. One channel, one row.

### Poll

Written before the session, answered during it. A poll has a question, a set of options, and a
type: `Multiple choice`, `Short answer` or `Checkbox`. After the session it carries per-option
vote counts and a respondent list.

### Q&A entry

A question asked during the session: asker, timestamp, their CRM module as a tag, the question
text, and optionally a nested host answer with the responder's name. **Not every question has
an answer**, and that is real behaviour rather than missing data — an unanswered question is a
follow-up somebody still owes.

### Session File

An attachment: file name, size, date added. Separate from **Recordings**, which is its own
related list. A recording uploaded as a session file is not the same object as the automatic
session recording produced by the Preferences toggle.

---

## Derived values — compute these, never store them

### Attendance

```
Total Registration  = count(registrants)
Total Attendees     = count(registrants where attended)
Total Absentees     = Total Registration − Total Attendees
Attendance Rate     = Total Attendees / Total Registration        (as a percentage)
```

**Before the webinar has run, attendance does not exist.** Total Attendees, Total Absentees,
Attendance Rate and the two attendance charts are absent — not zero. The list view renders
`—` for Attendance Count and Attend. Rate on any webinar that has not happened.

### Seats

```
Seats Left = Set Registration Limit − Total Registration
```

Only meaningful when a limit is set. With no limit there is nothing to count down from, and
the seats-left line is absent rather than showing a large number or infinity.

### Webinar ROI

Six tiles on the completed record (file 05). The arithmetic:

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

### Which deals count

Decided by the **attribution model** set in the integration (file 02). A contact usually
attends several webinars before a deal closes, and the model decides how that deal's revenue
is divided across them.

> **This is unresolved and blocks the revenue panel.** Whether the Deals Won table shows each
> deal's *full* amount or its *attributed share* is not specified anywhere, and the two give
> answers that differ by a factor of the number of webinars involved. See file 07. Do not
> guess — the ROI figure is the headline number of the whole feature.

---

## State: what exists when

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
list — but it means there is no rail shortcut to the feature's headline numbers. File 07 raises
whether that is right.

---

## The list view

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

## Naming

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

File 08 covers the naming decisions that were made and rejected, and why.
