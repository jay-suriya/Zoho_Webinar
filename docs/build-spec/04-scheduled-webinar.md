# 04 — The scheduled webinar record

A record whose **Webinar Category** is `Scheduled Webinar`: created, not yet run. It answers
one question — *who is coming* — and it has no attendance data of any kind.

---

## The record page

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

## Registration & Attendance Summary

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
Module or Source. Those four appear only after the session (file 05).

> Every drill-down currently returns "0 records" while the chart that opened it shows non-zero
> counts. The drill-downs are not wired to real data — wire them.

---

## Send Invite

The flow that connects the webinar to CRM's records. **This is the most important flow in the
feature.**

### Step 1 — the record picker

Opens directly on a record picker: a **module dropdown** first, then a view filter, then the
records with checkboxes.

**The module dropdown is populated from *Who Can Participate From CRM*** (file 02). Only
enabled modules appear. Leads and Contacts are always there because they are locked on;
anything else appears only if an admin ticked it.

> There is no separate module-chooser step before this. It was removed — the picker opens with
> the module dropdown inside it.

### Step 2 — the picker has two internal steps

**Tick the record rows → press `Add` → then press `Next`.**

`Add` **commits** the selection and moves to a selected-records list with a **Remove ALL**
action. Only then does `Next` do anything.

> **Pressing `Next` before `Add` does nothing at all — no error, no movement, no feedback.**
> This has cost real time twice: once building the flow, once automating it. **Fix it while you
> are here:** either disable `Next` until a selection is committed, or remove `Add` and let
> `Next` commit. Do not ship the silent version.

### Step 3 — Mass Email

Hands off to **CRM's existing Mass Email compose step**. Out of scope to rebuild — you supply
recipients and a template.

The **Invitation Template** is chosen through a **Select Template** button, whose dialog lists
**only templates whose Email Type is `Webinar Invitation`** (file 06). The chosen template
shows as a preview link beside the button.

The dialog's second column is the **template folder** — Public Email Templates, Managerial
Templates and so on. It is not the module: every row in this picker is a webinar invitation
template already, so the module would say nothing.

> There is no "sent later, automatically" section in this compose step. It was removed.

### Step 4 — what sending does

Two observable consequences, both of which you must implement:

1. **The invited records appear in the `Invited` related list**, each carrying All Invite
   Status and Webinar Status (file 01).
2. **An `Email` row is created in View Registration Link, and Enable Source Tracking switches
   on** (below).

---

## View Registration Link

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

## Polls

Polls are **written before the session and answered during it**. On a scheduled webinar they
exist but have no results.

**Create Poll** opens the editor. A poll has a question, a set of answer options, and a type:

| Type | Behaviour |
|---|---|
| Multiple choice | one answer from a list |
| Short answer | free text |
| Checkbox | several answers from a list |

The Polls rail entry carries a count badge once polls exist. File 05 covers the answered state.

---

## Session Files

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
> read-only. You will need all four — file 07.

---

## Actions

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

### Cancel Webinar — the only conditional item

| Record | Label | Behaviour |
|---|---|---|
| One-off, not completed | `Cancel Webinar` | opens a confirm |
| **Recurrent**, not completed | `Cancel` | opens a **choice modal**: this occurrence / all future occurrences |
| **Completed** | **absent** | there is nothing left to cancel |

Cancelling sends the cancellation email to registrants (file 06).

> The menu is clipped at the right edge of the viewport when the record page is narrow. It is
> positioned `right: 0` against a container that does not account for its width. Fix the
> positioning; do not shorten the labels.
