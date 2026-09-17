# Zoho Webinar in Zoho CRM

[Figma — CRM and Webinar Integration](https://www.figma.com/design/zBznyEXaHmU2aNJ3ECs9vF/CRM-and-Webinar-Integration)

## Contents

- **[1. Integration](#1-integration)**
- [1.1 Who can participate from CRM](#1-1-who-can-participate-from-crm)
- [1.2 Webinar deal attribution](#1-2-webinar-deal-attribution)
- **[2. Webinar list page](#2-webinar-list-page)**
- **[3. Create webinar](#3-create-webinar)**
- [3.1 Live webinar](#3-1-live-webinar)
- [3.2 On-demand webinar](#3-2-on-demand-webinar)
- [3.3 New fields](#3-3-new-fields)
- **[4. Scheduled webinar](#4-scheduled-webinar)**
- [4.1 Send Invite](#4-1-send-invite)
- [4.2 View registration source](#4-2-view-registration-source)
- [4.3 Registration & Attendance Summary](#4-3-registration-attendance-summary)
- [4.4 Poll creation](#4-4-poll-creation)
- [4.5 Session Files](#4-5-session-files)
- [4.6 Actions](#4-6-actions)
- **[5. Completed webinar](#5-completed-webinar)**
- [5.1 Registration & Attendance Summary](#5-1-registration-attendance-summary)
- [5.2 Webinar Revenue](#5-2-webinar-revenue)
- [5.3 Invited related list](#5-3-invited-related-list)
- [5.4 Polls](#5-4-polls)
- [5.5 Q&A](#5-5-q-a)
- **[Things we still need to decide](#things-we-still-need-to-decide)**
- **[Appendix A — every field in the create form](#appendix-a-every-field-in-the-create-form)**

## Introduction

### What is Zoho Webinar

Zoho Webinar is Zoho's webinar product: you schedule a session, people register through a
public form, they attend or they don't, and afterwards you have a recording, a set of poll
answers and a Q&A transcript. It runs live sessions, on-demand sessions that play a
pre-recorded video, and recurring series. Around the session itself sits a set of lifecycle
emails — an invitation, a confirmation, up to three reminders, and separate follow-ups for
the people who turned up and the people who didn't.

It is a complete product on its own. This document is not about that product. It is about
running it **from inside Zoho CRM**, as a CRM module.

### Who uses it

The person this is built for is a **sales rep or account executive who is also the CRM
admin for the integration** — Jay, in the mock. He lives in Zoho CRM all day. He has never
used standalone Zoho Webinar and does not want to learn it as a second product.

The range is wider than one persona, though, and the module list in §1.1 is the evidence:
the integration ships with thirteen participant modules, from **Leads** and **Contacts**
through **Donors**, **Volunteers**, **Students**, **Alumni**, **Patients** and
**Subscribers**. That is a non-profit running a donor briefing, a university running an
alumni session, a clinic running a patient education webinar, and a B2B software company
running a product masterclass — all using the same surface.

What they have in common is the purpose: **the webinar is a step in a customer
relationship that CRM already owns.** The audience is already in CRM as records. The
outcome — who registered, who attended, what they asked, whether they bought — belongs
back on those records.

### Why this integration, and what it solves

Zoho Webinar on its own cannot see CRM. That produces four specific costs, and the
integration exists to remove them:

- **The audience has to be rebuilt.** The people you want at the webinar are already
  Leads and Contacts. Standalone, you export them to CSV and re-import them into the
  webinar tool as a fresh list that immediately starts drifting from CRM.
  → §1.1 and §4.1: invites are sent **to CRM records**, from the CRM modules you choose.
- **The results have to be brought back by hand.** Registrations and attendance land in
  the webinar tool. Getting them onto the CRM record is another export and another import.
  → §3.3 and §5.3: registrants can be pushed into CRM, and every invited record carries
  its own invite status and attendance status.
- **Nobody can answer "did the webinar make money?"** The cost sits in one place and the
  deals sit in another, and no one joins them.
  → §1.2 and §5.2: a **Webinar Cost** on the record, an attribution model that splits deal
  revenue across the webinars that influenced it, and an ROI panel that does the division.
- **It is a second product to operate.** Different UI, different login, different
  conventions.
  → The whole document: a Zoho Webinar module inside CRM, with CRM's list views, record
  pages, related lists, mass email and templates.

> USECASE: Jay runs a free masterclass to generate pipeline. He picks 200 Leads and 40
> Contacts in CRM and invites them without leaving the module. Registrants who were not
> already in CRM are pushed in as new Leads. After the session the record shows 30
> registered, 15 attended, what each of them asked in Q&A — and that seven deals worth
> $16,800 closed off the back of it, against a $2,500 cost.

---

# 1. Integration

The integration is turned on once, by an admin, from the CRM marketplace. Everything in
sections 2–5 depends on it being enabled, and two of its settings change what the rest of
the product does — which is why they are the two sub-sections here.

**Where it starts:** Setup → Marketplace → Zoho → the Zoho Meetings card → **For webinars
› Set up**.

![[01-marketplace-zoho.jpg|The Zoho Meetings card in Marketplace ▸ Zoho. "For webinars › Set up" is the entry point]]

The card checks the account situation **before** showing anything about the integration. If
the user has no Zoho Webinar account, is not an admin, or the trial has expired, a modal
says so and the flow stops there. Only a valid account reaches the introduction page.

> NOTE: The check lives at the card, not on the introduction page. That ordering is
> deliberate — a user who cannot have the integration should not be sold it first. The same
> branch is also re-checked on the introduction page's Setup button, as a second guard.

![[02-intro-hero.jpg|The introduction page. Enabling happens later — the only action here is Setup, top right]]

**Setup** opens a four-step wizard. Each step has **Cancel** and **Next**; Cancel abandons
setup and returns to the introduction page. The steps **accumulate** rather than replace
each other — an answered step stays on screen so an earlier decision can be re-read while a
later one is being made, and only the step being answered shows its buttons.

![[05-wizard-step1.jpg|Step 1 — Email and Organisation]]

![[06-wizard-step2.jpg|Step 2 — Sync past webinars? Yes/No radios, Yes preselected]]

| Step | What it asks | Control | Default |
|---|---|---|---|
| 1 | Email + Organisation | Text / picklist | the signed-in user's |
| 2 | Sync past webinars? | Radio — Yes / No | **Yes** |
| 3 | Who Can Participate From CRM | Checkbox list | Leads + Contacts, locked |
| 4 | Webinar Deal Attribution | Card select, 6 models | **Linear** |

Step 4's Next button reads **Enable Integration** rather than Next, because it is the last
one — pressing it turns the integration on and lands on the enabled page, which shows the
same settings again plus a dirty-state Save bar.

![[10-enabled-panel.jpg|The enabled page. Same settings, now with a Save bar]]

![[charts/flow-01-integration-setup.png|The account gate. Three blocking cases stop before the introduction page; only a valid account continues]]

![[charts/flow-01-integration-setup-wizard.png|The four-step wizard. Every step's Cancel returns to the introduction page; step 4's Next is Enable Integration]]

## 1.1 Who can participate from CRM

**Step 3 of the wizard.** This is the list of CRM modules whose records may be invited to a
webinar. It is the single most load-bearing setting in the integration: **turn a module off
here and it disappears from the module dropdown in Send Invite** (§4.1). Nothing else
surfaces the consequence, so a developer must treat this list as the source of truth for
that dropdown.

![[07-wizard-step3.jpg|Step 3. A search box over a flat checkbox list. Leads and Contacts are ticked, greyed and cannot be turned off]]

The control is CRM's standard module picker: one card, a **Search** field, then a flat
scrollable checkbox list.

**Every module, verbatim, in list order** (`IM_MODULES`):

| # | Module | State |
|---|---|---|
| 1 | Leads | **Locked on** — ticked, red asterisk, cannot be unticked |
| 2 | Contacts | **Locked on** — ticked, red asterisk, cannot be unticked |
| 3 | Vendors | off by default |
| 4 | Donors | off by default |
| 5 | Volunteers | off by default |
| 6 | Members | off by default |
| 7 | Students | off by default |
| 8 | Alumni | off by default |
| 9 | Partners | off by default |
| 10 | Speakers | off by default |
| 11 | Referrals | off by default |
| 12 | Patients | off by default |
| 13 | Subscribers | off by default |

**The rule:** `IM_LOCKED = ["Leads", "Contacts"]`. The toggle handler returns early for
anything in that list, so the two cannot be switched off by any route. Everything else
starts unchecked, which means a freshly enabled integration can invite Leads and Contacts
and nothing else.

> NOTE: Every module in this list is a **person** — someone who can hold an email address
> and sit in a seat. Accounts, Potentials, Cases, Campaigns and Meetings were deliberately
> removed: a company, a deal, a ticket, a campaign and an event cannot attend a webinar.
> Any module added here in future must satisfy the same test.

> NOTE: Mechanically this setting gates who can be **invited**, not who can **attend** —
> anyone holding the public registration link can still register. The heading says
> "participate" as a statement of intent, not a literal description of the control.

> OPEN: A module can be turned off *after* invites have already been sent to its records.
> What happens to those existing invited records is not modelled.

## 1.2 Webinar deal attribution

**Step 4 of the wizard.** A contact usually attends more than one webinar before a deal
closes. This setting decides how that deal's revenue is divided across them, and it is what
makes the ROI figures in §5.2 mean anything.

![[08-wizard-step4.jpg|Step 4 — Webinar Deal Attribution]]

![[09-wizard-attribution-models.jpg|The six models as selectable cards. Linear carries the selected state]]

Six models, presented as cards. **Verbatim descriptions, in the order shown:**

| Model | What it does |
|---|---|
| First Webinar Interaction | Attributes 100% of the deal revenue to the earliest webinar attended. |
| Last Webinar Interaction | Attributes 100% of the deal revenue to the most recent webinar attended. |
| **Linear** *(default)* | Distributes the deal revenue equally across all webinars attended. |
| Increasing Time Decay | Assigns more credit to earlier webinars and gradually less to later ones. |
| Decreasing Time Decay | Assigns more credit to the most recent webinars and gradually less to earlier ones. |
| Position-Based | Gives 40% to first, 40% to last, 20% split across in-between webinars. |

**Linear is preselected.** In the mock the selected card is marked by an inline pink border
(`#C2185B`) and pink fill (`#fdf0f4`) rather than a class, so anything reading selection
state out of the DOM must look at the style, not a class name.

> NOTE: Only Position-Based states its split numerically (40/40/20). The two Time Decay
> models describe a direction but no decay function and no half-life, so the actual
> weighting is unspecified. That has to be defined before this can be built.

> OPEN: The two Time Decay descriptions read inverted against the usual meaning of the
> term — "Increasing Time Decay" gives **more** credit to **earlier** webinars. Confirm
> whether the names or the descriptions are what's wrong before implementing either.

> OPEN: What counts as an interaction for attribution — attending, or merely registering?
> §5.2 divides by attendees, which implies attendance, but the model descriptions all say
> "attended" while the deal could equally have been influenced by a no-show who watched
> the recording.

---

# 2. Webinar list page

Zoho Webinar is a CRM module, so its landing page is a CRM list view — the same shell as
Leads or Contacts, with the module's own columns.

![[38-webinar-list.jpg|The Zoho Webinar module list view]]

**Columns, in order:**

| # | Column | Notes |
|---|---|---|
| 1 | *(checkbox)* | row select |
| 2 | Webinar Name | carries the "All ▼" view selector |
| 3 | Webinar Category | Scheduled Webinar / Completed Webinar / On-Demand Webinar |
| 4 | Webinar Date & Time | e.g. `Mon, Aug 11, 2025 11:00 AM IST` |
| 5 | Registration Count | integer |
| 6 | Attendance Count | **`—` until the webinar has happened** |
| 7 | Attend. Rate | **`—` until the webinar has happened**, e.g. `77%` |
| 8 | Webinar Duration | e.g. `1 hr 30 mins` |
| 9 | Organiser | user |
| 10 | Webinar Type | Live Webinar / On-Demand Webinar |

**Actions on the page:** `▿ Filter`, `⇅ Sort`, **Create Webinar**, and a `⋮` overflow.

**The category drives the record.** Which sections a record shows (§4 vs §5) follows from
Webinar Category, not from comparing the date to now — a Scheduled Webinar shows Start
Webinar / Send Invite / View Registration Link in its header, a Completed Webinar shows
neither and gains Webinar Revenue instead.

> NOTE: Attendance Count and Attend. Rate render as an em dash rather than `0` for a
> webinar that has not happened. That distinction matters: zero attendance and *not yet
> known* are different states and must not both be stored as 0.

> USECASE: A recurring webinar appears as one row **per occurrence** — the mock lists
> "Recurrent Webinar" twice, on Sep 2 and Sep 9, each with its own registration count.

---

# 3. Create webinar

**Where it starts:** the **Create Webinar** button on the list page.

The form is five sections in a single scroll — **Webinar Details**, **Registration Setup**,
**Preferences**, **Reminders**, **Follow-Ups** — and it carries **63 fields in total**, of
which 42 are visible in the default configuration. The rest are revealed by the branches
below.

![[14-create-form-details.jpg|The Create Webinar form, Webinar Details section]]

**Only one field is required: Webinar title.** Saving without it is refused.

![[37-save-validation.jpg|Save with an empty title. The field is marked and the save does not proceed]]

Two picklists restructure the form, and they are the two branches worth understanding
before anything else:

- **Webinar Type** — `Live Webinar` (default) / `OnDemand Webinar` → §3.1, §3.2
- **Registration Type** — `With Registration` (default) / `Without Registration`

![[charts/flow-02-create-webinar.png|Create Webinar, with the branches that restructure the form]]

## 3.1 Live webinar

The default. **Webinar Details** in flow order:

| Field | Type | Required | Default | Options |
|---|---|---|---|---|
| Webinar title | Text | **Yes** | *(placeholder: Enter webinar title)* | — |
| Webinar Type | Picklist | No | Live Webinar | Live Webinar, OnDemand Webinar |
| Webinar Date & Time | Date input + time picklist | No | today + 10:00 AM | 9:00 AM, 10:00 AM, 11:00 AM, 12:00 PM, 1:00 PM, 2:00 PM … |
| Webinar Duration | Compound picklist (hr + min) | No | 1 hr + 00 min | 1–24 hr; minutes in 00/15/30/45 |
| Webinar Timezone | Picklist | No | (-6) Central | (-5) Eastern, (-6) Central, (-7) Mountain, (-8) Pacific, (+0) UTC, (+5:30) IST |
| Webinar Owner | Picklist + user lookup | No | Rao Priya | Rao Priya, Jay Acme, Mark Acme, Suriya → §3.3 |
| Organizer | Picklist w/ search | No | Jayasuriya | Jayasuriya, Morrison Troy |
| Repeat Webinar | Custom control → modal | No | off | → repeat modal |
| Co-Organizer | Custom control → panel | No | None | → co-organiser panel |
| Webinar Cost | Text, `$` prefix | No | *(placeholder: 0.00)* | → §3.3 |
| Description | Textarea | No | empty | — |

![[70-webinar-owner-open.jpg|Webinar Owner open. A search box over the user list — the same shell Organizer uses]]

**Repeat Webinar** opens its own modal (Repeat Type, Repeat Ends — On / After *n* Webinars).

![[23-repeat-webinar-modal.jpg|The Repeat Webinar modal]]

**Registration Setup**, with `Registration Type = With Registration`:

| Field | Type | Required | Default | Options |
|---|---|---|---|---|
| Registration Type | Picklist | No | With Registration | With Registration, Without Registration |
| Registration Form | Picklist | No | Default Form | Default Form, Real Estate Form, Stock Trading Form, + Create New Form → §3.3 |
| Customize Registration Page | Picklist | No | Standard Template | Standard Template, Custom Created |
| Moderation Type | Picklist | No | Automatic Moderation | Automatic Moderation, Manual Moderation |
| Set Registration Limit | Text | No | empty | — |
| Push Webinar Registrants to CRM | Checkbox | No | **unchecked** | → §3.3 |
| Allow/deny registrants from specific countries | Picklist | No | No Restrictions | No Restrictions, Allow registrants from Countries, Block registrants from Countries |
| Allow/Block Specific Domains | Picklist | No | No Restriction | No Restriction, Allow specific email domains, Block specific email domains |
| Post_Registration Custom Redirection | Text | No | *(placeholder: https://)* | — |
| Allow access to join link only through mail | Checkbox | No | **checked** | — |
| Allow only authenticated Zoho Users with a Zoho account | Checkbox | No | unchecked | — |
| Send Confirmation to Registrants | Checkbox | No | **checked** | — |
| Confirmation Email Template | Template picker | No | Webinar Confirmation Template | — |

![[24-registration-setup.jpg|Registration Setup]]

**Customize Registration Page** reveals an eye icon on hover over either option, which
previews the public registration page as a registrant will see it — built from the title,
date and time currently on the form rather than fixed sample text.

![[27-customize-reg-page-picklist.jpg|The picklist, with the hover eye that opens the preview]]

![[28-reg-page-preview-standard.jpg|Standard Template — First Name, Last Name, Email]]

![[29-reg-page-preview-custom.jpg|Custom Created — adds Phone Number, Company and Portfolio Size]]

The preview has a desktop/mobile toggle; mobile narrows the card to 420px and stacks the
two columns.

![[30-reg-page-preview-mobile.jpg|The same page, mobile layout]]

**Choosing `Without Registration`** hides the entire registration apparatus — all thirteen
fields above except Registration Type — and reveals three others instead:

| Revealed | Type | Why |
|---|---|---|
| Who can Join | Picklist | with no registration there is no registrant list, so access is decided here |
| Send thank you email to attendees | Checkbox | replaces the confirmation/reminder chain |
| Thank You Email Template | Template picker | its template |

![[36-without-registration.jpg|Without Registration. Registration Form, limits, moderation and the whole reminder chain are gone]]

> NOTE: **Without Registration removes the reminder and follow-up chain entirely** — 1st/
> 2nd/3rd Reminder, both Follow-ups and both Include Recording settings all disappear,
> because those emails address a registrant and there are none. Only "Send thank you email
> to attendees" survives.

**Preferences, Reminders and Follow-Ups** share the remainder of the scroll:

![[32-preferences-reminders.jpg|Preferences, Reminders and Follow-Ups — the form's scroller maxes out around 770px, so all three land in one screenful]]

| Field | Type | Default | Options |
|---|---|---|---|
| Allow attendees to ask questions | Checkbox | — | — |
| Allow anonymous questions | Checkbox | — | — |
| Show questions to all | Checkbox | — | — |
| Auto Reply for questions | Checkbox *(revealed)* | — | — |
| Automatic session recording | Checkbox | — | — |
| Video recording | Checkbox | — | — |
| Display attendee list to all | Checkbox | — | — |
| Use Emoji reactions | Checkbox | — | — |
| Post webinar Re-direction | Checkbox | — | — |
| 1st Reminder | Picklist | 15 mins before the webinar | 2/5/10/15/30 mins, 1/2/6/12 hrs, 1/2 days before the webinar |
| 2nd Reminder | Picklist | **None** | **None**, then the same eleven intervals |
| 3rd Reminder | Picklist | **None**, then the same eleven intervals |
| Send Follow-up Email to Attendees | Picklist | 2 mins after the webinar ends | None, 2/5/10/15/30 mins, 1/2/6/12 hrs, 1/2 days after the webinar ends |
| Send Follow-up Email to Absentees | Picklist | 2 mins after the webinar ends | same as above |
| Include Recording for Attendees | Checkbox | unchecked | — |
| Include Recording for Absentees | Checkbox | unchecked | — |

> NOTE: The 2nd and 3rd reminders carry **None** on top of the same eleven intervals the
> 1st offers, and both default to None. That is how a webinar sends fewer than three
> reminders — there is no separate "number of reminders" setting. The 1st reminder has no
> None option, so **at least one reminder always goes out** on a registration webinar.

Each reminder and follow-up has its own template slot, chosen through **Select Template**:

![[34-slot-select-template.jpg|A template slot's Select Template dialog]]

## 3.2 On-demand webinar

Setting **Webinar Type = OnDemand Webinar** changes what the session *is*: instead of a
live session at a time, it plays a pre-recorded video.

![[35-ondemand-form.jpg|The on-demand form. Video File replaces Webinar Duration; Allow video play/pause sits directly beneath it]]

**What changes, exactly:**

| Direction | Field | Note |
|---|---|---|
| **Gained** | Video File | replaces Webinar Duration — the video's own length is the duration |
| **Gained** | Allow video play/pause | sits in the Webinar Timezone row's empty right cell, directly under Video File |
| **Lost** | Webinar Duration | — |
| **Lost** | Repeat Webinar | a recording does not recur |
| **Lost** | Co-Organizer | — |
| **Lost** | Allow anonymous questions, Show questions to all | there is no live Q&A to moderate |
| **Lost** | Automatic session recording, Video recording | it *is* a recording |
| **Lost** | Display attendee list to all, Use Emoji reactions | no shared live audience |
| **Lost** | 1st/2nd/3rd Reminder + their templates | — |
| **Lost** | Both Follow-up emails + their templates | — |
| **Lost** | Include Recording for Attendees / Absentees | — |

On-demand keeps **25 visible fields** against live-with-registration's 42.

> NOTE: The placement of **Allow video play/pause** is deliberate: it was moved out of a
> row of its own so the right column reads **Video File → Allow video play/pause →
> Organizer**, putting the setting next to the file it governs rather than two rows away.

> OPEN: On-demand loses the entire reminder and follow-up chain even though it still has a
> Webinar Date & Time and still takes registrations. A registrant for an on-demand session
> therefore gets a confirmation and nothing else — no reminder that it is available, no
> follow-up. Confirm this is intended rather than a consequence of reusing the live form's
> visibility rules.

## 3.3 New fields

Four fields this integration introduces that a plain Zoho Webinar form does not have, or
does not have in this form. They are the fields that make the CRM half work, so they are
worth reading together.

### 1. Webinar Owner

| Field | Type | Required | Default | Options |
|---|---|---|---|---|
| Webinar Owner | Picklist with search + user-lookup button | No | Rao Priya | Rao Priya, Jay Acme, Mark Acme, Suriya |

![[70-webinar-owner-open.jpg|Webinar Owner open — search box, then the user list, with a lookup icon beside the field]]

**Owner is a CRM concept, not a webinar one.** Every CRM record has an owner, and it drives
record-level sharing, assignment rules and "My Webinars" filters. It is distinct from
**Organizer**, which is the webinar's host — the person who actually runs the session.

> NOTE: Owner and Organizer are separate fields with separate option lists — Owner offers
> Rao Priya / Jay Acme / Mark Acme / Suriya, Organizer offers Jayasuriya / Morrison Troy.
> They are not the same directory and must not be collapsed into one field. Both use the
> same picklist-with-search shell.

### 2. Webinar Cost

| Field | Type | Required | Default | Options |
|---|---|---|---|---|
| Webinar Cost | Text, `$` prefix, info tooltip | No | *(placeholder: 0.00)* | — |

![[71-webinar-cost.jpg|Webinar Cost — a $ prefix inside the field and an info icon at its right]]

The tooltip reads: *"This is the amount attendees will be charged to register for this
webinar."*

**This field is the denominator of every ROI figure in §5.2.** A cost of `2500` entered
here is what produces Cost `$2,500`, ROI `+572%`, Cost/Attendee `$167` and
Revenue/Attendee `$1,120` on the completed record.

> NOTE: There is a contradiction to resolve. The tooltip says this is **what attendees are
> charged** — revenue. §5.2 uses it as **what the webinar cost to run** — expenditure, the
> ROI denominator, shown in a tile labelled "Cost" beside a separate "Revenue (Won)" tile
> fed by closed deals. Both cannot be true. The ROI arithmetic is self-consistent, so the
> **tooltip is the more likely error**, but this must be decided before build.

> OPEN: The field is plain text with no validation and no currency selector, while the `$`
> prefix is hard-coded. Multi-currency orgs need a currency; free-text needs a numeric
> constraint.

### 3. Registration Form

| Field | Type | Required | Default | Options |
|---|---|---|---|---|
| Registration Form | Picklist | No | Default Form | Default Form, Real Estate Form, Stock Trading Form, **+ Create New Form** |

![[25-registration-form-picker.jpg|The Registration Form picklist. Each row reveals a Preview tag on hover]]

This is the form a registrant fills in on the public registration page — the fields it
collects are what you get back about a person who was not already in CRM, which makes it
the input side of §3.3.4.

Each option reveals a **Preview** tag on hover, opening the form builder's preview:

![[26-registration-form-preview.jpg|A registration form preview]]

**+ Create New Form** is the last option and opens a form builder rather than selecting
anything — a create action living inside a picklist.

> NOTE: Don't confuse **Registration Form** with **Customize Registration Page**. The form
> is *which fields are collected*; the page is *how the public page looks* (Standard
> Template / Custom Created). They are separate picklists sitting one above the other in
> the same column, and the page preview's field set is driven by the page choice, not this
> one.

### 4. Push Webinar Registrants to CRM

| Field | Type | Required | Default | Options |
|---|---|---|---|---|
| Push Webinar Registrants to CRM | Checkbox + **Manage Config** link | No | **unchecked** | — |

![[72-push-to-crm-row.jpg|The checkbox, with Manage Config beside its label]]

**This is the field that closes the loop.** Someone who registers from the public link —
found the webinar on LinkedIn, was forwarded it, arrived from a tweet — does not exist in
CRM. Ticked, they are created as CRM records automatically, and the re-import step
disappears.

**Manage Config** opens the field mapping — which registration form field lands in which
CRM field, and which module the new record is created in:

![[31-push-to-crm-config.jpg|The Push to CRM configuration]]

> NOTE: It is **off by default**, so the loop is open unless someone closes it. Given this
> is the single feature that most justifies the integration, a default of unchecked is
> worth challenging.

> OPEN: Deduplication is not modelled. If a registrant's email already matches a Lead or
> Contact, it is unspecified whether the existing record is updated, a duplicate is
> created, or the registrant is skipped.

---

# 4. Scheduled webinar

A webinar whose **Webinar Category** is `Scheduled Webinar` — created, not yet run.

![[39-detail-scheduled.jpg|A scheduled webinar. Start Webinar, Send Invite, View Registration Link, Edit, Actions]]

**Header buttons:** Start Webinar · Send Invite · View Registration Link · Edit · Actions
**Tabs:** Overview · Timeline
**Related list rail:** Notes · Invited · Polls · Q&A · Recordings · Session Files · Open
Activities · Closed Activities

The Details panel above the summary carries Webinar Date & Time, Webinar Duration,
Organiser, Co-Organiser and Webinar Type, with a **Hide Details** toggle expanding the full
Webinar Details and Registration Details blocks.

![[40-detail-details-panel.jpg|The expanded Details panel]]

> NOTE: The detail page scrolls an **inner element**, not the window. Its scroller maxes out
> around 2820px on a scheduled webinar and 3812px on a completed one. Anything driving this
> page programmatically must set `scrollTop` on that element and cannot rely on scrolling
> past the maximum.

## 4.1 Send Invite

The flow that connects the webinar to CRM's records.

![[charts/flow-03-send-invite.png|Send Invite end to end. Add commits the selection; Next opens Mass Email]]

**Step 1 — the record picker.** A module dropdown, a view filter, then the records.

![[41-send-invite-picker.jpg|The record picker. Module dropdown first, then the view, then the records]]

**The module dropdown is populated from §1.1.** Only modules enabled in Who Can Participate
From CRM appear. Leads and Contacts are always there; anything else appears only if an
admin ticked it.

**Step 2 — this picker has two internal steps.** Tick the record rows, then press **Add**,
which commits the selection and moves to a selected-records list with **Remove ALL**. Only
then does **Next** do anything.

![[42-send-invite-confirm.jpg|After Add — the committed selection, with Remove ALL]]

> NOTE: **Pressing Next before Add does nothing at all** — no error, no movement. This
> silently cost time during capture and will cost a developer the same. Either Next should
> be disabled until a selection is committed, or Add should be removed and Next should
> commit.

**Step 3 — Mass Email.** CRM's mass-email compose step.

![[43-mass-email.jpg|The Mass Email step]]

The **Invitation Template** is chosen through **Select Template**, which lists only
templates whose Email Type is Webinar Invitation:

![[44-select-template.jpg|Select Template. Only Invitation-type templates are offered]]

**Step 4 — what sending does.** Two things happen, and both are observable:

1. The invited records appear in the **Invited** related list, each with an invite status
   and a webinar status.
2. An **Email** row is created in View Registration Link and **Enable Source Tracking** is
   switched on (§4.2).

![[45-invited-section.jpg|The Invited section after sending]]

> OPEN: Re-inviting is not fully modelled — whether a record already invited can be
> selected again, and whether that resends or is refused, is unspecified.

## 4.2 View registration source

**View Registration Link** in the header opens the public registration link and the list of
tracked sources underneath it.

![[46-registration-link-empty.jpg|Before any invite — the default link, source tracking off, no source rows]]

A webinar nobody has been invited to has **no sources at all** and the table is empty. This
is deliberate: a brand-new webinar should not chart registrations from channels that do not
exist yet.

Completing Send Invite creates the first source:

![[47-registration-link-email-source.jpg|After sending — Enable Source Tracking is on and an Email row exists]]

| Column | Example |
|---|---|
| Source | Email |
| Created by | Jay |
| Visited | 0 |
| Registered | 0 |
| Status | enabled |

**Enable Source Tracking switches itself on** when the first source is created, because a
source with tracking off would record nothing.

> NOTE: A second Send Invite does **not** add a second Email row — the creation is guarded
> against duplicates. One channel, one row.

## 4.3 Registration & Attendance Summary

A collapsible band below the Details panel. On a scheduled webinar it answers "who has
signed up so far", and it is deliberately thinner than its completed-webinar counterpart
(§5.1) because attendance does not exist yet.

![[73-scheduled-summary.jpg|Registration & Attendance Summary on a scheduled webinar]]

| Block | What it shows |
|---|---|
| Registration Overview | `10 / 200` Total Registration with a % ring, `190 seats left`, and `5` Waiting for Approval with a View → link |
| Registration by Module | pie — Lead (7), Contact (2), Vendor (1) |
| Registration by Source | grouped bar, **Visited vs Registered** per channel |
| Daily Registration Trend | line — `10` Total Registered, `Aug 9 (2)` Peak Day, `1` Avg / Day |

**Registration Overview reads against the limit** set by Set Registration Limit (§3.1) —
`190 seats left` is `200 − 10`. With no limit set, there is nothing to count down from.

**Waiting for Approval** only means something under `Moderation Type = Manual Moderation`.

Each chart is clickable and opens a drill-down record list (Last Name, Created By, Created
Time).

> NOTE: There is **no attendance data on a scheduled webinar** — no Total Attendees, no
> Total Absentees, no Attendance by Module or Source. Those four appear only after the
> session (§5.1). The band keeps its name in both states.

> OPEN: Every drill-down in the mock reports "0 records" while the chart it opened shows
> non-zero counts. The drill-down is not wired to real data.

## 4.4 Poll creation

Polls are written before the session and answered during it.

![[48-polls-pre.jpg|Creating a poll before the webinar]]

**Create Poll** opens the editor. A poll has a question and a set of answer options, and
three question types are offered:

| Type | Behaviour |
|---|---|
| Multiple choice | one answer from a list |
| Short answer | free text |
| Checkbox | several answers from a list |

The Polls related list carries a count badge (`Polls 2`) once polls exist. Results are
empty until the session runs — see §5.4 for the answered state.

## 4.5 Session Files

The webinar's attachments — slides, handouts, recordings, promotional assets.

![[74-session-files.jpg|The Session Files related list]]

| Column | Example |
|---|---|
| File Name | 📄 Webinar_Slides_Q3.pdf |
| Size | 3.2 MB |
| Date Added | Sep 4, 2025 |

Four sample files, each with a type icon: `Webinar_Slides_Q3.pdf` (3.2 MB),
`Product_Demo_Recording.mp4` (128 MB), `Attendee_Handout.docx` (0.8 MB),
`Q3_Promo_Banner.png` (1.4 MB).

> NOTE: **Session Files is separate from Recordings**, which is its own rail entry and
> reads "No recordings available." on both states in the mock. A recording uploaded as a
> session file is not the same object as the automatic session recording produced by the
> Preferences toggle (§3.1).

> OPEN: No upload control, size limit, permitted types, or delete action is modelled — the
> list is read-only in the mock.

## 4.6 Actions

The overflow menu in the record header, beside Edit.

![[75-actions-menu.jpg|The Actions menu open on a scheduled webinar]]

**All thirteen items, in order:**

| # | Item | Notes |
|---|---|---|
| 1 | **Cancel Webinar** | shown in red. On a recurrent webinar the label is **Cancel** and it opens a choice modal (this occurrence / all future). **Absent on a completed webinar** |
| 2 | Clone | |
| 3 | Share | |
| 4 | Delete | |
| 5 | Share via Cliq | |
| 6 | Print Preview | |
| 7 | Customize Business Card | standard CRM |
| 8 | Organize Campaign Details | standard CRM |
| 9 | Add Related List | standard CRM |
| 10 | Add Kiosk ✨ | ✨ marks a Zia/AI item |
| 11 | Create Button | standard CRM |
| 12 | Create Client Script ✨ | |
| 13 | View Followers | |

**Items 7–13 are CRM's standard record actions**, inherited because Zoho Webinar is a CRM
module. Only item 1 is webinar-specific and only it is conditional.

> NOTE: The cancel item is the only thing in this menu whose label and behaviour change
> with record state — `Cancel Webinar` for a one-off, `Cancel` plus a
> this-occurrence/all-future modal for a recurrent one, and nothing at all once completed.

---

# 5. Completed webinar

A webinar whose **Webinar Category** is `Completed Webinar`. The record answers a different
question now: not "who is coming" but "what did we get".

![[49-completed-overview.jpg|A completed webinar]]

**What changes in the header:** Start Webinar, Send Invite and View Registration Link are
**gone**. Only **Edit** and **Actions** remain. The rail is unchanged, and a **Webinar
Revenue** band appears that a scheduled webinar does not have.

## 5.1 Registration & Attendance Summary

The same band as §4.3, now with the attendance half filled in.

![[50-registration-summary.jpg|Registration Overview on a completed webinar — registration, attendees and absentees]]

**Registration Overview** carries three figures instead of one:

| Figure | Value in the mock |
|---|---|
| Total Registration | 30 |
| Total Attendees | 15 (50%) |
| Total Absentees | 15 (50%) |

**Four charts, where a scheduled webinar had two.** Attendance is added alongside
registration, so the same cut can be compared before and after:

| Chart | Segments |
|---|---|
| Attendance by Module | Lead (10), Contact (3), Vendor (2) |
| Attendance by Source | Email (8), Twitter (4), LinkedIn (3) |
| Registration by Module | Lead (7), Contact (2), Vendor (1) |
| Registration by Source | Twitter (4), Email (3), LinkedIn (2), Direct (1) |

![[51-registration-by-source.jpg|Registration and Attendance by Source]]

**Attendees and Registrants List** — six tabs, each with its own count:

| Tab | Count |
|---|---|
| All Attendees | 13 |
| All Absentees | 6 |
| All Registrants | 14 |
| Approved Registrants | 11 |
| Unapproved Registrants | 4 |
| Denied Registrants | 3 |

![[52-attendees-list.jpg|The Attendees and Registrants list]]

**Columns:** Last Name · Email · All Modules · All Sources · Polls · Q&A · Registered Date ·
Webinar Status

**Webinar Status** is `Attended` or `Not Attended`. **Polls** is the count of polls that
person answered and **Q&A** is `Yes` / `—` — so the list doubles as an engagement ranking,
not just an attendance register. A row whose Module is `—` came from the public link and is
not in CRM.

> NOTE: **Mock defect — do not reproduce.** These numbers do not reconcile. Registration
> Overview says 30 registered / 15 attended / 15 absent; the tabs say 13 attendees, 6
> absentees, 14 registrants; the table paginates "1 – 10 of 11 records"; and the module
> segments total 15 for attendance and 10 for registration. Build the relationships
> (attendees + absentees = registrants; segments sum to the total), not these values.

## 5.2 Webinar Revenue

The band a completed webinar gains, and the reason Webinar Cost (§3.3.2) exists.

![[55-revenue-roi.jpg|Webinar ROI, Pipeline by Stage, Deals Won by Source and the Deals Won table]]

**Webinar ROI — six tiles:**

| Tile | Value | How it is derived |
|---|---|---|
| Cost | $2,500 | **Webinar Cost** from the create form |
| Revenue (Won) | $16,800 | sum of the Deals Won table |
| ROI | +572% | `(Revenue − Cost) / Cost` = (16,800 − 2,500) / 2,500 |
| In Pipeline | $32,450 | sum of open influenced deals |
| Cost / Attendee | $167 | `Cost / attendees` = 2,500 / 15 |
| Revenue / Attendee | $1,120 | `Revenue / attendees` = 16,800 / 15 |

**The arithmetic is consistent** — the seven Deals Won rows
(1000 + 1500 + 2000 + 3200 + 2800 + 1800 + 4500) total exactly $16,800, and both
per-attendee figures divide by 15, the Total Attendees from §5.1. Those formulas are the
specification.

**Two charts:**

- **Pipeline by Stage** — Proposal Sent (7), Negotiation (5), Closed Won (9),
  Closed Lost (3), Waiting for Manager (4)
- **Deals Won by Source** — Twitter (4), Email (3), LinkedIn (2), Direct (1)

**Deals Won table** — Deal Name · Amount · Stage · Account Name · Contact Name, 7 records,
with Deal Name, Amount, Account Name and Contact Name all rendered as links into their CRM
records. **Deals in Pipeline** follows in the same shape.

> NOTE: **Webinar Revenue is collapsed by default** and is **not in the related-list rail**,
> so it cannot be reached the way Polls or Q&A can. It has to be scrolled to and expanded.

> NOTE: Which deals appear here is decided by the **attribution model** from §1.2. With
> Linear, a deal influenced by three webinars contributes a third of its amount to each.
> The mock does not show the split, so an implementation must decide whether Amount shows
> the deal's full value or its attributed share — the two give very different ROI.

> OPEN: Pipeline by Stage shows 9 Closed Won against 7 rows in the Deals Won table. Either
> the chart counts something wider than the table, or one of them is wrong.

## 5.3 Invited related list

The record of who was invited from CRM and what became of them — the direct output of §4.1.

![[76-completed-invited.jpg|The Invited related list]]

**Tabs:** All Modules · Invited · Registered · Not Registered · Attended · Not Attended —
each carrying a count, so the funnel is readable in one line.

**Columns:**

| Column | Example |
|---|---|
| Name | Jayasuriya |
| Email | Jayasuriya |
| Module | Leads / Contacts |
| All Invite Status | Not Registered / Registered |
| Webinar Status | Not Attended / Attended |
| Invite Sent on | Matchendran on Jan 28, 2022 at 08:25 PM |

**Two separate status fields, and they are not the same thing.** *All Invite Status* tracks
the invitation — did this person act on it. *Webinar Status* tracks the session — did they
turn up. A record can be Registered and Not Attended, which is the no-show case the
Absentees follow-up email exists for.

> NOTE: This list is the CRM half of the funnel and the Attendees and Registrants list
> (§5.1) is the webinar half. A person from the public link appears in §5.1 with Module `—`
> and **never appears here**, because they were never invited from CRM. Neither list is a
> superset of the other.

> NOTE: **Mock defect — do not reproduce.** "Invite Sent on" shows `Matchendran on Jan 28,
> 2022` — a user and a date unrelated to the rest of the record's 2025 data.

## 5.4 Polls

The polls written in §4.4, now with answers.

![[53-polls-completed.jpg|Poll results on a completed webinar]]

**Poll Answered by** tabs cut the results by who answered: All Modules · Leads · Contacts ·
Vendors · Not in CRM.

Each poll shows its question, every option with its vote count as a bar, then two summary
figures:

**"How would you rate this webinar?"** — ⭐ 1 - Poor · ⭐⭐ 2 - Fair · ⭐⭐⭐ 3 - Good ·
⭐⭐⭐⭐ 4 - Very Good · ⭐⭐⭐⭐⭐ 5 - Excellent
**"Would you recommend us to others?"** — Yes, definitely · Maybe · No, not really

Both report **`67.3%` Voted** and **`100` Total Votes**.

Clicking through opens the respondent list — Name · Email · Company · Phone · Owner — which
is what makes a poll answer actionable: a 5-star rating attached to a named Lead is a
follow-up, not a statistic.

> NOTE: The **Not in CRM** tab is the important one. Poll respondents who arrived from the
> public link have no CRM record, so their answers cannot be attributed to anyone — unless
> Push Webinar Registrants to CRM (§3.3.4) was ticked, in which case they will have been
> created as records.

> OPEN: Both polls report exactly `67.3%` Voted and `100` Total Votes, and the option
> counts do not sum to 100. Sample data, but the relationship between option counts, Total
> Votes and % Voted needs defining.

## 5.5 Q&A

The questions asked during the session, and the host's answers.

![[54-qa.jpg|The Q&A transcript]]

**Tabs:** Overall Q&A · Leads · Contacts · Not in CRM — the same cut as Polls.

**A participation summary** heads the section:

| Figure | Value |
|---|---|
| Participated in Q&A | 21 |
| Leads | 7 |
| Contacts | 7 |
| Not in CRM | 5 |

**The transcript is a threaded conversation**, not a table. Each entry carries an avatar
with initials, the asker's name, a timestamp, **their CRM module as a tag**, and the
question. A host answer is nested under it, marked **Host** with the responder's name:

> **JS** jonam suriya · 11:08 AM · *Leads*
> "What does the Enterprise plan cost per seat?"
> **J** Host · 11:09 AM · Jay
> "Our Enterprise plan starts at $49/seat/month — we can share a detailed pricing deck
> after the session."

**Not every question has an answer.** Two of the seven in the mock are unanswered — which
is real behaviour, not a gap: an unanswered question is a follow-up the rep still owes.

> NOTE: The module tag on each question is what makes this worth having in CRM rather than
> in the webinar tool. "A Lead asked about Salesforce integration" is a sales signal
> attached to a record; the same sentence in a webinar transcript is not.

> OPEN: `7 + 7 + 5 = 19`, but the summary says 21 participated. The tab counts and the
> total disagree.

> OPEN: There is no action on a question — no convert-to-task, no assign, no mark-answered.
> For unanswered questions, which the mock deliberately includes, that is the obvious
> missing step.

---

# Things we still need to decide

### Blocking

- **Webinar Cost means two different things** (§3.3.2). The tooltip calls it what attendees
  are charged; the ROI panel treats it as what the webinar cost to run. Cannot build either
  until this is settled.
- **Time Decay is undefined** (§1.2). Two of the six attribution models describe a direction
  but no decay function and no half-life.
- **Attribution and the Deals Won amount** (§5.2). Does Amount show a deal's full value or
  its attributed share? Linear across three webinars gives an ROI three times apart.

### Product

- Should **Push Webinar Registrants to CRM** default to on? It is the feature that most
  justifies the integration and it ships unchecked (§3.3.4).
- **Deduplication** on push: update, duplicate, or skip when a registrant's email already
  matches a record (§3.3.4).
- **Re-inviting** a record that has already been invited — allowed, resend, or refused
  (§4.1).
- Does an **on-demand** webinar really get no reminders and no follow-ups (§3.2)?
- **Send failure is not modelled** (§4.1). What happens if Mass Email refuses — no template
  chosen, no recipients left after Remove ALL, a send error — has no state.
- **Removing every selected record** in the picker's step 2 is a dead end: is Next blocked,
  or does it return to the record table (§4.1)?
- **No invitation templates exist** — does Select Template offer inline creation, or does
  the flow stall (§4.1)?
- **Cancel on re-entry** (§1). Cancel is specified as returning to the introduction page,
  but for an integration that is already enabled it should arguably return to the enabled
  panel. Confirm which.
- **The three blocking modals have no stated exit** (§1) — only the not-an-admin modal's
  button is named. Where dismissal lands is unspecified.
- **Save on the enabled page** (§1) has no success or failure state; the dirty-state bar is
  named but its outcome is not.
- Does attribution count **attendance or registration** (§1.2)?
- What happens to already-invited records when a **module is turned off** in §1.1?

### Engineering

- **Attendance Count / Attend. Rate must distinguish "not yet known" from zero** — the list
  renders `—`, not `0` (§2).
- The detail page **scrolls an inner element**, capped at 2820px (scheduled) / 3812px
  (completed) (§4).
- Attribution card selection is carried by **inline style, not a class** (§1.2).
- **Webinar Revenue is collapsed by default and absent from the rail** (§5.2).
- All drill-downs from summary charts currently return **0 records** (§4.3).

### Design

- **Next does nothing before Add** in the Send Invite picker (§4.1) — disable Next, or drop
  Add.
- The **Actions** menu is clipped at the right edge of the viewport in the mock (§4.6).
- The Registration & Attendance Summary band keeps its name on a scheduled webinar where
  there is no attendance data (§4.3).
- **No back navigation in the setup wizard** (§1). Only Cancel and Next exist, yet every
  answered step stays on screen with its fields live — so a user can see an earlier answer
  but has no stated way to return to it.
- **No Cancel or discard on the create form** (§3) — only Save is modelled.
- **Manage Config has no stated exit** (§3.3.4) — what closes it, and whether it can be
  cancelled, is unspecified.

### Assumptions this document makes

- The three account-blocking cases in §1 are driven by a DEMO switcher in the mock; real
  behaviour is assumed to come from the user's Zoho Webinar account and CRM role.
- Field lists, types, defaults and options were **extracted from the mock's DOM**, not
  typed. Where a control is custom (Repeat Webinar, Co-Organizer, template slots) the type
  column says "custom control" rather than guessing a primitive.
- Sample values (names, counts, amounts) are mock data and are quoted only to show shape.

### Mock defects — do not reproduce

- **§5.1** Registration, attendance and tab counts do not reconcile with each other or with
  the table's own pagination.
- **§5.5** Q&A tab counts sum to 19 against a stated 21 participants.
- **§5.4** Poll option counts do not sum to Total Votes; both polls report identical
  figures.
- **§5.2** Pipeline by Stage shows 9 Closed Won against 7 rows in Deals Won.
- **§5.3** "Invite Sent on" reads `Matchendran on Jan 28, 2022`, unrelated to the record.
- The registrant list on a webinar whose only channel is Email still carries rows sourced
  LinkedIn, Twitter and Direct.

---

# Appendix A — every field in the create form

63 fields. **Visible** is per variant: **L** = Live + With Registration, **W** = Live +
Without Registration, **O** = On-Demand. A field not visible in a variant is not rendered
at all, not merely disabled.

| Field | Type | Req | Default | L | W | O |
|---|---|---|---|---|---|---|
| Webinar title | Text | **Yes** | *(Enter webinar title)* | ✓ | ✓ | ✓ |
| Webinar Type | Picklist | No | Live Webinar | ✓ | ✓ | ✓ |
| Webinar Date & Time | Date + time picklist | No | today, 10:00 AM | ✓ | ✓ | ✓ |
| Webinar Duration | Compound picklist | No | 1 hr + 00 min | ✓ | ✓ | — |
| Video File | File | No | — | — | — | ✓ |
| Webinar Timezone | Picklist | No | (-6) Central | ✓ | ✓ | ✓ |
| Allow video play/pause | Checkbox | No | checked | — | — | ✓ |
| Webinar Owner | Picklist + lookup | No | Rao Priya | ✓ | ✓ | ✓ |
| Organizer | Picklist w/ search | No | Jayasuriya | ✓ | ✓ | ✓ |
| Repeat Webinar | Custom → modal | No | off | ✓ | ✓ | — |
| Co-Organizer | Custom → panel | No | None | ✓ | ✓ | — |
| Webinar Cost | Text, `$` prefix | No | *(0.00)* | ✓ | ✓ | ✓ |
| Description | Textarea | No | empty | ✓ | ✓ | ✓ |
| Registration Type | Picklist | No | With Registration | ✓ | ✓ | ✓ |
| Registration Form | Picklist | No | Default Form | ✓ | — | ✓ |
| Customize Registration Page | Picklist | No | Standard Template | ✓ | — | ✓ |
| Moderation Type | Picklist | No | Automatic Moderation | ✓ | — | ✓ |
| Set Registration Limit | Text | No | empty | ✓ | — | ✓ |
| Push Webinar Registrants to CRM | Checkbox + Manage Config | No | **unchecked** | ✓ | — | ✓ |
| Allow/deny registrants from specific countries | Picklist | No | No Restrictions | ✓ | ✓ | ✓ |
| Select Allowed Countries | Multi-select *(revealed)* | No | — | ○ | ○ | ○ |
| Allow/Block Specific Domains | Picklist | No | No Restriction | ✓ | — | ✓ |
| Add Allowed Domains | Text *(revealed)* | No | — | ○ | ○ | ○ |
| Post_Registration Custom Redirection | Text | No | *(https://)* | ✓ | — | ✓ |
| Post Redirection URL | Text *(revealed)* | No | — | ○ | ○ | ○ |
| Allow access to join link only through mail | Checkbox | No | **checked** | ✓ | — | ✓ |
| Allow only authenticated Zoho Users with a Zoho account | Checkbox | No | unchecked | ✓ | ✓ | ✓ |
| Who can Join | Picklist | No | — | — | ✓ | — |
| Send Confirmation to Registrants | Checkbox | No | **checked** | ✓ | — | ✓ |
| Confirmation Email Template | Template picker | No | Webinar Confirmation Template | ✓ | — | ✓ |
| Send thank you email to attendees | Checkbox | No | — | — | ✓ | — |
| Thank You Email Template | Template picker | No | — | — | ✓ | — |
| Allow attendees to ask questions | Checkbox | No | — | ✓ | ✓ | ✓ |
| Allow anonymous questions | Checkbox | No | — | ✓ | ✓ | — |
| Show questions to all | Checkbox | No | — | ✓ | ✓ | — |
| Auto Reply for questions | Checkbox *(revealed)* | No | — | ○ | ○ | ○ |
| Automatic session recording | Checkbox | No | — | ✓ | ✓ | — |
| Video recording | Checkbox | No | — | ✓ | ✓ | — |
| Display attendee list to all | Checkbox | No | — | ✓ | ✓ | — |
| Use Emoji reactions | Checkbox | No | — | ✓ | ✓ | — |
| Post webinar Re-direction | Checkbox | No | — | ✓ | ✓ | ✓ |
| 1st Reminder | Picklist | No | 15 mins before the webinar | ✓ | — | — |
| 1st Reminder Template | Template picker | No | — | ✓ | — | — |
| 2nd Reminder | Picklist | No | **None** | ✓ | — | — |
| 2nd Reminder Template | Template picker *(revealed)* | No | — | ○ | — | — |
| 3rd Reminder | Picklist | No | **None** | ✓ | — | — |
| 3rd Reminder Template | Template picker *(revealed)* | No | — | ○ | — | — |
| Send Follow-up Email to Attendees | Picklist | No | 2 mins after the webinar ends | ✓ | — | — |
| Send Follow-up Email to Absentees | Picklist | No | 2 mins after the webinar ends | ✓ | — | — |
| Attendees Follow-up Template | Template picker | No | — | ✓ | — | — |
| Absentees Follow-up Template | Template picker | No | — | ✓ | — | — |
| Include Recording for Attendees | Checkbox | No | unchecked | ✓ | — | — |
| Include Recording for Absentees | Checkbox | No | unchecked | ✓ | — | — |

✓ visible · — not rendered · ○ revealed only when its parent field is set

## Picklist options, verbatim

| Field | Options |
|---|---|
| Webinar Type | Live Webinar · OnDemand Webinar |
| Webinar Timezone | (-5) Eastern · (-6) Central · (-7) Mountain · (-8) Pacific · (+0) UTC · (+5:30) IST |
| Webinar Owner | Rao Priya · Jay Acme · Mark Acme · Suriya |
| Organizer | Jayasuriya · Morrison Troy |
| Registration Type | With Registration · Without Registration |
| Registration Form | Default Form · Real Estate Form · Stock Trading Form · **+ Create New Form** |
| Customize Registration Page | Standard Template · Custom Created |
| Moderation Type | Automatic Moderation · Manual Moderation |
| Allow/deny registrants from specific countries | No Restrictions · Allow registrants from Countries · Block registrants from Countries |
| Allow/Block Specific Domains | No Restriction · Allow specific email domains · Block specific email domains |
| 1st Reminder | 2 mins · 5 mins · 10 mins · 15 mins · 30 mins · 1 hr · 2 hrs · 6 hrs · 12 hrs · 1 day · 2 days — *before the webinar* |
| 2nd / 3rd Reminder | **None** + the same eleven intervals |
| Send Follow-up to Attendees / Absentees | **None** · 2 mins · 5 mins · 10 mins · 15 mins · 30 mins · 1 hr · 2 hrs · 6 hrs · 12 hrs · 1 day · 2 days — *after the webinar ends* |

## Integration constants

**`IM_MODULES`** — Leads · Contacts · Vendors · Donors · Volunteers · Members · Students ·
Alumni · Partners · Speakers · Referrals · Patients · Subscribers
**`IM_LOCKED`** — Leads · Contacts
**Attribution models** — first · last · **linear** *(default)* · increasing · decreasing ·
position

## Where each flow starts, for testing

| Flow | Entry |
|---|---|
| Integration | Setup → Marketplace → Zoho → Zoho Meetings card → For webinars › Set up |
| Webinar list | Zoho Webinar module in the left rail |
| Create webinar | List page → **Create Webinar** |
| Scheduled webinar | List page → any row with Category `Scheduled Webinar` |
| Send Invite | Scheduled webinar → **Send Invite** |
| Registration source | Scheduled webinar → **View Registration Link** |
| Completed webinar | List page → any row with Category `Completed Webinar` |
| Webinar Revenue | Completed webinar → scroll past the attendee list, expand the band |
