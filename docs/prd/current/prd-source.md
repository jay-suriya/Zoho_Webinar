# Zoho Webinar in Zoho CRM

Written by clicking through the mock at `webinar.html` as it stands on `master`. Every screenshot is a real screen from it, captured headlessly from the same file. Where the mock does not answer a question, this document says so rather than guessing.

## Table of Contents

1. Introduction
2. Turning the integration on
3. Creating a webinar
4. Fields in the create flow
5. Before the webinar
6. The webinar list
7. After the webinar
8. Open questions

## Introduction

### What Zoho Webinar is

Zoho Webinar is Zoho's webinar product. You schedule a session, publish a registration form, and people sign up. The product emails them along the way — an invitation, a confirmation when they register, up to three reminders before it starts, and afterwards a follow-up that differs depending on whether they turned up. It runs the session itself, and it keeps what happened in the room: the polls you ran, the questions people asked, the recording, the files you shared.

None of that is missing today. Zoho Webinar does the webinar well.

### Who uses it

Businesses that sell by getting people into a room — not as an occasional marketing experiment, but as the way the pipeline actually starts.

The business used throughout this document is one of those: a company that runs **training courses for other businesses**. Jay is its account executive. His week has a webinar in it every week, because the webinar is both halves of his job:

- **The free masterclass** — an hour of genuinely useful teaching, ending in an offer. This is how strangers become leads.
- **The paid course sessions** — the thing customers bought, delivered as webinars too.

So a single session is a marketing channel, a sales pitch and a product at once. Two hundred people register, sixty turn up, and somewhere in that sixty are the companies that will buy a team licence this quarter. Jay's job is to find them.

That makes three questions matter more to him than anything else about a webinar: **who registered, who actually turned up, and which of them ended up paying.**

### The problem

Those are exactly the three questions that stop at the product boundary.

Jay lives in CRM. The Leads and Contacts he invites are there, the Deals he closes are there, the Accounts they belong to are there. The webinar sits outside it, so every session costs him the same manual round trip:

- He **exports** a recipient list out of CRM to invite anyone, so the invite goes to whatever the data looked like the day he exported it — not to the record as it stands.
- He **re-imports** the registrants afterwards, hand-matching the ones who already exist so he does not create duplicates.
- He **guesses** at the result. Attendance lives in one product and pipeline in the other, so "did that webinar produce anything?" is answered by eyeballing two lists side by side, if it is answered at all.

The cost is not only the effort. A rep opening a lead in CRM cannot see that this person sat through a masterclass last Thursday, so the next call starts colder than it needed to. And because the link between attendance and revenue is never recorded, the case for running the next webinar rests on a feeling rather than a number.

### How the CRM integration solves it

It closes the boundary rather than adding a second place to work. Once enabled, Zoho Webinar becomes a module in CRM, sitting in the left nav alongside Leads and Contacts, and each webinar is a record like any other:

- **Inviting CRM records directly**, so the invite always goes to current data — and to the modules the admin allows, not only Leads and Contacts.
- **Bringing registrations, joins and no-shows back onto the webinar record**, and optionally creating CRM records from registrants who were not in CRM to begin with, so there is nothing to re-import.
- **Sending the whole email lifecycle** — invitation, confirmation, up to three reminders, and separate follow-ups for attendees and absentees — from templates that live with the module.
- **Tying attendance to the deals it influenced**, through an attribution model you choose, so what a webinar was worth is a figure on the record instead of a guess.

Who registered and who turned up land on the record. What it was worth is attributed to the deals. The rest of this document walks that in the order a user meets it.

## Turning the integration on

### Where it starts

Setup ▸ Marketplace ▸ Zoho lists the Zoho apps that connect to CRM. Zoho Webinar and Zoho Meetings share one card, because they share one login: **For webinars** and **For online meetings** are set up independently, and the note on the card says so.

![[int-01-marketplace-zoho.jpg|Setup ▸ Marketplace ▸ Zoho. The Zoho Meetings card carries both paths; the DEMO switcher top-right is a mock-only control for walking the blocking states]]

> NOTE: The **DEMO** dropdown at the top right of this page exists only in the mock. It selects which account situation to simulate, and is how the five cases below are reached.

### The blocking cases come first

Clicking **Set up** answers the account question before anything else. Three of the five cases cannot proceed, and each stops here with a modal rather than letting the user walk further in:

| Case | Situation | What happens |
|---|---|---|
| 1 | No Zoho Webinar account for this email | Modal offering to create one |
| 2 | One Webinar organisation | Straight to the introduction page |
| 3 | Several organisations | Introduction page, then an org picker in setup |
| 4 | Account exists, user is a Member not an Admin | Modal explaining only Admins can connect |
| 5 | Trial expired | Modal explaining the trial has ended |

![[int-09-case1-no-account.jpg|Case 1 — no Webinar account under this email. The user can create one without leaving CRM]]

![[int-10-case4-not-admin.jpg|Case 4 — the account exists but the user is a Member. Only Cancel is offered: CRM cannot promote someone inside Zoho Webinar, so it does not pretend to]]

![[int-11-case5-trial-expired.jpg|Case 5 — trial expired]]

> USECASE: Jay's colleague clicks Set up and gets Case 4. Nothing is half-configured and no marketing is shown to someone who cannot act on it — the modal names the Super Admin to ask.

### The introduction page

Cases 2 and 3 reach an introduction page. It exists because most people meeting this card have never used Zoho Webinar and are deciding whether to switch a working process. It explains the integration and nothing else: there is no form on it, and the only action is **Setup** in the header.

![[int-02-intro-hero.jpg|The introduction page. One claim, one supporting line, and Setup in the header]]

![[int-03-intro-features.jpg|What you get — five capabilities, one card each]]

![[int-04-intro-solves.jpg|What it solves — each old way struck through, with what replaces it underneath]]

### The setup page

**Setup** opens the form. It asks for four things, in this order:

1. **Email and organisation** — which Zoho Webinar account to connect. On Case 3 this is where the organisation is chosen.
2. **Sync past webinars** — Yes or No. Yes brings historical webinars in as records so reporting is not starting from empty.
3. **Who Can Participate From CRM** — the modules a webinar invite may be sent to.
4. **Webinar Deal Attribution** — how a webinar's contribution to a deal is counted.

![[int-05-setup-top.jpg|Connection details and Sync past webinars]]

**Who Can Participate From CRM** is the setting with the longest reach: it decides the module list in Send Invite. **Leads and Contacts are mandatory** — checked, asterisked, and not clickable — because an integration that cannot invite either has nothing to invite. Everything else is opt-in, and the list holds only modules that describe people.

![[int-06-setup-participate.jpg|Who Can Participate From CRM. Leads and Contacts are locked on; the rest are the person-shaped modules a business might keep]]

**Webinar Deal Attribution** picks between six models, with **Linear** selected by default — the least opinionated choice, splitting credit evenly across the touchpoints.

![[int-07-setup-attribution.jpg|Webinar Deal Attribution, Linear pre-selected]]

### After enabling

Enabling adds the Zoho Webinar module and returns the same settings as an editable panel, with a dirty-state save bar. The introduction page stays reachable, and its badge flips from NOT ENABLED to ENABLED so it never contradicts the state of the account.

![[int-08-enabled.jpg|The enabled panel — the same decisions, now editable]]

## Creating a webinar

**Create Webinar** on the module opens one long form in five sections: Webinar Details, Registration Setup, Preferences, Reminders and Follow-Ups. The two decisions that reshape the rest of it are **Webinar Type** and **Registration Type**.

### A live webinar

![[cr-01-live-details.jpg|Webinar Details for a live webinar]]

Webinar Details is the session itself: title, type, date and time with its own timezone picklist, duration, owner and organiser, co-organisers, cost, and description. **Webinar Cost** is worth noticing this early — it is the figure the ROI calculation on the completed webinar divides by, so a webinar created without it produces a revenue section with no cost side.

### Registration Setup, with registration

![[cr-02-registration-setup.jpg|Registration Setup with registration on]]

With registration on, the section decides how people get in and who is allowed:

- **Registration Mode** — register per event, or register once and attend any event in a series.
- **Registration Form** — the form registrants fill in. Three sample forms ship, each previewable, and **+ Create New Form** opens the builder.
- **Moderation Type** — Automatic (anyone who registers is approved) or Manual (each registration waits for approval, which is what produces the *Waiting for Approval* tile on the detail page).
- **Set Registration Limit** — the denominator in "10 / 200" on the detail page.
- **Push Webinar Registrants to CRM** — the switch that decides whether registrants become CRM records.
- Country and domain allow/deny rules, post-registration redirection, and whether the join link works only from the invitation email.

### Without registration

![[cr-06-without-registration.jpg|Registration Type set to Without Registration]]

Switching **Registration Type** to *Without Registration* removes the registration questions: there is no form, no moderation, no limit, and no registrant list to approve. Anyone with the link joins. It suits an internal or invite-only session, and it is the one case where the registration half of the detail page has nothing to show.

### An on-demand webinar

![[cr-05-ondemand.jpg|Webinar Type set to OnDemand Webinar — the live date and time give way to a recorded video]]

An on-demand webinar is a recording people watch when they choose. Selecting it replaces the live scheduling fields with a **Video File** picker and an **Allow video play/pause** switch. There is no start time to remind anyone about, so reminders stop applying, but registration still does — which is the point of it.

![[cr-09-ondemand-registration.jpg|On-demand with registration still on: the form and moderation questions remain]]

### Pushing registrants into CRM

![[cr-07-push-registrants-config.jpg|Manage Configuration for Push Webinar Registrants to CRM]]

This is the setting that answers the re-import problem from the introduction. With it on, a registrant who is not already in CRM is created as a record; **Manage Configuration** decides which module they land in and how the form's answers map onto its fields. Without it, registrations stay inside the webinar and the manual round trip survives.

> USECASE: Two hundred people register for Jay's masterclass and a hundred and forty are strangers. With push on, they are Leads by the time the session ends, each carrying the form answers that say which course they were interested in.

### The registration form

![[cr-08-registration-form.jpg|The registration form builder]]

The builder is where the questions come from. A form has a name, a description and a set of fields — multiple choice, short answer, checkbox — and the answers travel with the registrant, which is what makes the pushed records useful rather than just names.

## Fields in the create flow

Every field the create form presents, in form order, with its control and — for a picklist — the options it actually offers. Toggle rows are checkboxes styled as switches.

### Webinar Details

| Field | Control | Options |
|---|---|---|
| Webinar title * | Text, required | — |
| Webinar Type | Picklist | Live Webinar · OnDemand Webinar |
| Webinar Date & Time | Date input + time picklist | 9:00 AM · 10:00 AM · 11:00 AM · 12:00 PM · 1:00 PM · 2:00 PM |
| Webinar Duration | Two picklists, hours and minutes | Hours: 1–24 hr. Minutes: 00 · 15 · 30 · 45 min |
| Webinar Timezone | Picklist | (-5) Eastern · (-6) Central · (-7) Mountain · (-8) Pacific · (+0) UTC · (+5:30) IST |
| Video File | Picklist — on-demand only | From Zoho Webinar Recordings · Upload Files / Documents · Zoho WorkDrive · Other Cloud Services |
| Allow video play/pause | Toggle — on-demand only | — |
| Webinar Owner | Picklist | Rao Priya · Jay Acme · Mark Acme · Suriya |
| Organizer | Picklist | Jayasuriya · Morrison Troy |
| Co-Organizer (two rows) | Picklist | None · Jayasuriya · Morrison Troy |
| Repeat Webinar | Toggle, opens the repeat dialog | — |
| Webinar Cost | Text, currency | — |
| Description | Multi-line text | — |

The repeat dialog, when Repeat Webinar is on:

| Field | Control | Options |
|---|---|---|
| Repeat Type | Picklist | None · Daily · Weekly · Monthly · Yearly · Custom |
| Repeat Ends | Radio | Never · On *(date)* · After *(N)* Webinars |

### Registration Setup

| Field | Control | Options |
|---|---|---|
| Registration Type | Picklist | With Registration · Without Registration |
| Registration Mode | Picklist | Register and attend each event individually · Register once and attend any event |
| Open Registration for | Picklist | All Webinars · Only selected number of occurrences · 1–6 occurrences |
| Registration Form | Picklist, each entry previewable | Default Form · Real Estate Form · Stock Trading Form · + Create New Form |
| Moderation Type | Picklist | Automatic Moderation · Manual Moderation |
| Set Registration Limit | Number | — |
| Push Webinar Registrants to CRM | Toggle + Manage Configuration | — |
| Allow/deny registrants from specific countries | Picklist + country multi-select | No Restrictions · Allow registrants from Countries · Block registrants from Countries |
| Allow/Block Specific Domains | Picklist + domain list | No Restriction · Allow specific email domains · Block specific email domains |
| Post_Registration Custom Redirection | Toggle + Post Redirection URL (text) | — |
| Allow access to join link only through mail | Toggle | — |
| Allow only authenticated Zoho Users with a Zoho account | Toggle | — |
| Send Confirmation to Registrants | Toggle + Confirmation Email Template *(Select Template)* | — |

### Preferences

| Field | Control | Options |
|---|---|---|
| Who can Join | Picklist | Anyone can Join · Only Authenticated Users can Join |
| Allow/deny registrants from specific countries | Picklist + country multi-select | None · Allow registrants from Countries · Block registrants from Countries |
| Allow attendees to ask questions | Toggle | — |
| Allow anonymous questions | Toggle | — |
| Show questions to all | Toggle | — |
| Auto Reply for questions | Multi-line text | — |
| Automatic session recording | Toggle | — |
| Video recording | Toggle | — |
| Display attendee list to all | Toggle | — |
| Use Emoji reactions | Toggle | — |
| Post webinar Re-direction | Toggle + Post Redirection URL (text) | — |
| Send thank you email to attendees | Picklist + Thank You Email Template | 2 minutes · 5 mins · 10 mins after webinar ends |

### Reminders

All three reminders offer the same intervals; the 2nd and 3rd add **None** so a webinar can send fewer than three.

| Field | Control | Options |
|---|---|---|
| 1st Reminder | Picklist + 1st Reminder Template | 2 mins · 5 mins · 10 mins · 15 mins · 30 mins · 1 hour · 2 hours · 6 hours · 12 hours · 1 day · 1 week — before the webinar |
| 2nd Reminder | Picklist + 2nd Reminder Template | None, then the same eleven intervals |
| 3rd Reminder | Picklist + 3rd Reminder Template | None, then the same eleven intervals |

### Follow-Ups

| Field | Control | Options |
|---|---|---|
| Send Follow-up Email to Attendees | Picklist + Attendees Follow-up Template | None · 2 mins · 5 mins · 10 mins · 15 mins · 1 hour · 2 hours · 6 hours · 1 day — after the webinar ends |
| Send Follow-up Email to Absentees | Picklist + Absentees Follow-up Template | None, then the same eight intervals |
| Include Recording for Attendees | Toggle | — |
| Include Recording for Absentees | Toggle | — |

![[cr-03-preferences-reminders-followups.jpg|Preferences, Reminders and Follow-Ups. Every template row is a Select Template button, not a text field]]

> NOTE: Every email row here selects a template rather than composing one. That is deliberate: the template is a reusable object with its own link and merge-field rules, covered in *Before the webinar*.

> NOTE: The Webinar Owner and Organizer picklists hold the mock's sample users. In the product they would be the CRM users of the org.

## Before the webinar

### The detail page with nothing on it yet

A webinar that has just been created has registration switched on and nobody in it. The detail page is honest about that: the summary tiles read zero, and the primary actions are the three ways to get people in — **Start Webinar**, **Send Invite**, **View Registration Link**.

![[pre-01-detail-blank.jpg|A scheduled webinar before anyone has been invited]]

The left rail is the CRM related list: Notes, Invited, Polls, Q&A, Recordings, Session Files, Open and Closed Activities. Overview and Timeline sit above the body.

### Two ways in

**View Registration Link** is the public route: a URL to put in a newsletter or a social post. Anyone who arrives through it is a registrant with a source of their own.

![[pre-09-registration-link.jpg|The registration link — the public route into the webinar]]

**Send Invite** is the CRM route, and it is the one this integration exists for.

### Send Invite

![[pre-02-send-invite-picker.jpg|The record picker: a module dropdown, a view filter, then the records]]

The picker opens on a module dropdown holding exactly the modules the admin allowed in *Who Can Participate From CRM*, a view filter, and the records themselves. Selecting records and pressing **Next** opens **Mass Email**, which is CRM's own compose step: recipients, the **Invitation Template**, From and Reply-To, and whether to send now or schedule.

The Invitation Template is chosen through **Select Template**, which lists the Zoho Webinar templates whose Email Type is *Invitation* — the ones that can carry a registration link. **+ Create Template** creates a new one, and because the step already knows what it is for, it does not ask what type to make.

> NOTE: An invitation template must contain the **Registration Link** merge field, and saving one without it is refused. That is the rule that makes the invite work: the link is how a recipient becomes a registrant, and how the registration is attributed back to the email.

### How a CRM invite becomes a tracked registration

The invitation carries the registration link. When a recipient uses it, the registration is recorded with a **source** — and an invite sent from CRM lands under **Email**, which is why the *Registration by Source* and *Attendance by Source* charts can separate the people Jay invited from the people who found the webinar on LinkedIn or came in direct. The registrant also keeps the module they came from, so *Registration by Module* can say how many were Leads and how many were Contacts.

> OPEN: The mock records the source and shows it in the charts and the registrant table, but does not expose a "view the invitation email that produced this registration" link on the row. If that traceability is wanted per registrant, it needs designing.

### The Invited section, and re-inviting

Once invites go out, the **Invited** section is the register of who was asked. It counts them along the top — Invited, Registered, Not Registered, Attended, Not Attended — and lists each person with their module, invite status, webinar status and when the invite was sent.

![[pre-03-invited-section.jpg|The Invited section: counts across the top, one row per invited record]]

The gap between *Invited* and *Registered* is the number Jay actually works. **Re-invite** exists for exactly that: it offers to re-invite the people who have not registered yet, chosen by module, so the second email goes only to the ones who have not acted.

![[pre-08-reinvite-panel.jpg|Re-invite those not yet registered, by module]]

> USECASE: A hundred invited, two registered. Jay presses Re-invite, picks Leads, and the reminder goes to the ninety-odd Leads who ignored the first one — not to the two who already signed up.

### Polls, before the session

![[pre-04-polls.jpg|Polls on a scheduled webinar — written in advance]]

Polls are written before the webinar, not during it. Each poll has a question and a set of answers, and the section is where they are added and ordered. Writing them in advance is what allows the answers to be attributed to CRM records afterwards.

### Q&A, before the session

![[pre-05-qa.jpg|Q&A before the webinar — nothing to show yet, and it says so]]

Q&A only fills in once the session has run. Before that the section states plainly that it will be available after the webinar is completed, alongside the other sections that are empty until there is something to hold: Recordings, Session Files, Activities.

### Registration and attendance summary

![[pre-06-registration-summary.jpg|Registration & Attendance Summary while registrations are still arriving]]

This is the section Jay watches in the days before the session. Its components:

- **Registration Overview** — total registrations against the limit, seats left, and a *Waiting for Approval* tile with a link to the queue when moderation is manual.
- **Registration by Module** — how many registrants came from Leads, Contacts, or another module. Clicking a slice lists those records.
- **Registration by Source** — visited against registered, per channel, so a channel that draws visits but no registrations is visible.
- **Daily Registration Trend** — registrations per day, with total, peak day and average.

Each chart can be switched between pie and bar, and each is clickable through to the underlying records.

> USECASE: Two days out, the trend line has flattened and the limit is nowhere near. That is the cue to send the second invite — and the Invited section already knows who has not registered.

### The registrant list

![[pre-07-registrant-list.jpg|The registrant list before the webinar]]

Below the charts is the list itself, one row per person, filterable by module and by source. Before the webinar it answers "who is coming"; after it, the same list gains the attendance columns and becomes the follow-up worklist.

## The webinar list

![[list-01-all-webinars.jpg|The Zoho Webinar module list, on the All Webinars view]]

The module list behaves like any CRM list view, with the views a webinar business actually sorts by:

| View | What it holds |
|---|---|
| All Webinars | Everything, whatever its state |
| My Webinars | The ones this user organises — the default |
| Scheduled Webinars | Not yet run |
| Completed Webinars | Already run |
| Today's Webinars | Starting today |
| Ongoing Webinars | Running right now |
| On Demand Webinars | Recordings, which have no start time |

Columns cover the session and its outcome together: Webinar Name, Category, Date & Time, Registration Count, Attendance Count, Attendance Rate, Duration, Organiser and Webinar Type. Attendance Rate is the one to read across rows — it is how a webinar that filled the room but bored it becomes visible.

> NOTE: A row's Category reflects state rather than a field the user sets: Scheduled, Completed, On-Demand, Canceled. Cancelling a webinar from its detail page moves the row.

## After the webinar

### The completed webinar

![[done-01-completed-overview.jpg|A completed webinar. Registration Overview now splits into attendees and absentees]]

Once the session has run, the same detail page answers a different question. **Registration Overview** stops being a countdown and becomes a result: total registrations, total attendees, total absentees, each with its percentage. The module and source charts gain attendance versions, so *who came* can be compared with *who signed up* channel by channel.

### The attendees and registrants list

![[done-02-registrant-list.jpg|Attendees and Registrants List, with the tabs that make it a worklist]]

This is the component Jay works after every webinar. It is one table with six tabs across the top — **All Attendees, All Absentees, All Registrants, Approved, Unapproved, Denied** — and per-person columns: name, email, module, source, **Polls** answered, whether they asked in **Q&A**, registered date, and webinar status.

How it gets used: the Polls and Q&A columns are the ranking. Someone who answered three polls and asked a question sat through the whole hour and engaged; someone who registered and never appeared did not. Jay sorts by those, works the engaged attendees first, and leaves the absentees to the follow-up email that already went out with the recording.

> USECASE: Fourteen registered, thirteen attended, six did not. Three of the thirteen answered every poll and asked a question — those are the calls Jay makes on Monday morning.

### Webinar revenue

![[done-06-revenue-roi.jpg|Webinar Revenue expanded — ROI across the top, pipeline and deal-source charts below]]

The revenue section is collapsed by default and expands to the answer the introduction promised. **Webinar ROI** carries six figures:

| Figure | In this webinar |
|---|---|
| Cost | $2,500 — the Webinar Cost from the create form |
| Revenue (Won) | $16,800 |
| ROI | +572% |
| In Pipeline | $32,450 — influenced but not yet closed |
| Cost / Attendee | $167 |
| Revenue / Attendee | $1,120 |

Below that, **Pipeline by Stage** shows where the influenced deals have reached — Proposal Sent, Negotiation, Closed Won, Closed Lost, Waiting for Manager — and **Deals Won by Source** splits the wins by the channel the person arrived through.

![[done-07-revenue-deals-won.jpg|Deals Won — the deals themselves, with amount, stage, account and contact]]

**Deals Won** lists the deals: name, amount, stage, account and contact. This is the table that ends the argument about whether webinars work, because each row is a deal a reader can open.

How it gets used: ROI justifies the next session, *In Pipeline* justifies the next two, and Cost / Attendee is the number to compare across webinars — a cheap room full of the wrong people is worse than an expensive room full of the right ones.

> NOTE: The figures depend on two things being set: **Webinar Cost** at creation, and an **attribution model** at setup. Without the cost there is no ROI, and without attribution no deal is ever credited to a webinar.

### Polls, after the session

![[done-04-polls.jpg|Poll results, filterable by the module the voter belongs to]]

After the session each poll shows its answer distribution with counts, the percentage of the room that voted, and total votes. The control that makes it a CRM feature rather than a webinar statistic is **Poll Answered by** — All Modules, Leads, Contacts, Vendors, Not in CRM — and clicking through a poll answer lists the people who chose it.

How it gets used: a poll is a qualifying question. "What is your team size?" or "When are you looking to start?" sorts the room without anyone having to ask, and the answer arrives attached to a record Jay can act on.

### Q&A, after the session

![[done-05-qa.jpg|The Q&A transcript, with each asker tagged by module]]

Q&A is kept as a transcript: each question with who asked it, when, which module they belong to, and the host's answer beneath it. A header line counts participation and splits it — Participated in Q&A, Leads, Contacts, Not in CRM — and the **Overall Q&A** dropdown narrows the transcript to one of those groups.

How it gets used: a question is the strongest buying signal a webinar produces. "What does the Enterprise plan cost per seat?" is not curiosity, it is a budget conversation starting, and the transcript tells Jay who said it and what he answered — so the follow-up call picks up where the room left off rather than starting again.

### On-demand, after the fact

![[done-04-ondemand.jpg|An on-demand webinar's detail page]]

An on-demand webinar has no session to attend, so attendance means *watched*. The registration half of the page behaves as it always did, which is why registration is worth keeping on for on-demand: without it, a recording is a file nobody is attributable to.

## Open questions

> OPEN: Per-registrant traceability back to the invitation email. The source is recorded and charted, but a row does not link to the email that produced the registration.

> OPEN: Reminders on on-demand webinars. There is no start time to count back from, but the reminder fields still render on the form.

> OPEN: `Webinar Cost` is a plain text field on the create form. It drives every figure in the revenue section, so it may deserve validation and a currency of its own.

> OPEN: Attendance Rate appears on the list view but not as a figure on the detail page, where it has to be read off the attendees and absentees percentages.
