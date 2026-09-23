# 05 — The completed webinar record

A record whose **Webinar Category** is `Completed Webinar`. It answers a different question
from the scheduled one: not *who is coming* but **what did we get**.

---

## What changes from scheduled

**Header:** `Start Webinar`, `Send Invite` and `View Registration Link` are **gone**. Only
`Edit` and `Actions ⌄` remain, and `Cancel Webinar` is absent from the Actions menu.

**Rail:** unchanged.

**Body:** the Registration & Attendance Summary fills in its attendance half, an **Attendees
and Registrants List** appears, and a **Webinar Revenue** band appears that a scheduled record
does not have.

---

## Registration & Attendance Summary

Same band as file 04, now complete.

**Registration Overview carries three figures instead of one:**

| Figure | Example |
|---|---|
| Total Registration | `30` |
| Total Attendees | `15 (50%)` |
| Total Absentees | `15 (50%)` |

Formulas in file 01. Attendees and absentees must sum to registrations; the percentages are of
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

## Attendees and Registrants List

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

## Webinar Revenue

The band a completed record gains, and the reason **Webinar Cost** exists.

**Collapsed by default, and not in the related-list rail.** It is reachable only by scrolling
the record body and expanding it. That is deliberate — it is reporting, not a related list —
but it means the feature's headline numbers have no shortcut. File 07 asks whether that is
right.

### Webinar ROI — six tiles

| Tile | Example | Derivation |
|---|---|---|
| Cost | `$2,500` | **Webinar Cost** from the create form |
| Revenue (Won) | `$16,800` | Σ amount of the Deals Won table |
| ROI | `+572%` | `(Revenue − Cost) / Cost` |
| In Pipeline | `$32,450` | Σ amount of open influenced deals |
| Cost / Attendee | `$167` | `Cost / Total Attendees` |
| Revenue / Attendee | `$1,120` | `Revenue / Total Attendees` |

The worked example and the division guards are in file 01. **Those formulas are the
specification** — the numbers above are a consistent set you can test against.

### Two charts

| Chart | Segments |
|---|---|
| Pipeline by Stage | Proposal Sent (7), Negotiation (5), Closed Won (9), Closed Lost (3), Waiting for Manager (4) |
| Deals Won by Source | Twitter (4), Email (3), LinkedIn (2), Direct (1) |

### Two tables

**Deals Won** and **Deals in Pipeline**, same shape:

```
Deal Name · Amount · Stage · Account Name · Contact Name
```

**Deal Name, Amount, Account Name and Contact Name all render as links into their CRM
records.** That is the point of having this panel inside CRM rather than in the webinar tool —
every figure is one click from the record behind it.

> **Which deals appear, and at what amount, is decided by the attribution model** (file 02).
> With Linear, a deal influenced by three webinars contributes a third of its amount to each.
> **Whether Amount shows the deal's full value or its attributed share is unspecified**, and
> the two produce ROI figures that differ by a factor of three in that example. Blocking —
> file 07.

---

## Invited related list

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

**The two status columns answer different questions** — see file 01. A row reading
`Registered` + `Not Attended` is a no-show, and that is exactly the population the Absentees
follow-up email addresses.

### This list and the Attendees list are not the same population

**Invited** is the CRM half of the funnel. **Attendees and Registrants** is the webinar half.

- Somebody invited from CRM who never registered appears in **Invited** only.
- Somebody who found the public link appears in **Attendees and Registrants** with Module `—`
  and **never appears in Invited at all**, because they were never invited from CRM.

**Neither list is a superset of the other.** Do not implement one as a filtered view of the
other.

---

## Polls, answered

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
Registrants to CRM** was ticked (file 03), in which case they will have been created as
records and the tab will be near-empty. The two features are connected; that tab is the visible
cost of leaving the push off.

> The mock's poll numbers do not add up — option counts do not sum to Total Votes and both
> polls report identical figures. Define the relationship between option counts, Total Votes
> and % Voted yourself; do not copy the sample.

---

## Q&A

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
> File 07.

> The mock's Q&A tab counts sum to 19 against a stated 21 participants. Build the relationship,
> not the numbers.
