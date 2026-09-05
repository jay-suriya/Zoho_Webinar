# Zoho Webinar in Zoho CRM

Everything below was written by clicking through the mock at `webinar.html`. Every screenshot is a real screen from it, and every behaviour described is one that was actually triggered. Where the mock doesn't answer a question, it says so instead of guessing.

## Table of Contents

1. [Introduction](#introduction)
2. [Turning the integration on](#turning-the-integration-on)
3. [Creating a webinar](#creating-a-webinar)
4. [The webinar list](#the-webinar-list)
5. [A webinar that hasn't happened yet](#a-webinar-that-hasn-t-happened-yet)
6. [A webinar that has happened](#a-webinar-that-has-happened)
7. [On-demand webinars](#on-demand-webinars)
8. [The emails](#the-emails)
9. [Things we still need to decide](#things-we-still-need-to-decide)
10. [Appendix: full field reference](#appendix-full-field-reference)

## Introduction

Zoho Webinar is Zoho's webinar product. You schedule a session, publish a registration form, people sign up, they show up or they don't, and the product emails them along the way — an invitation, a confirmation, reminders, and a follow-up afterwards. It also keeps what happened in the room: the polls you ran, the questions people asked, the recording, the files you shared.

All of that already works. The problem is where it happens. A sales rep lives in CRM, and today the webinar sits outside it, which means the rep does this: export the registrant list, re-import it somewhere, and try to work out by hand whether the session actually produced any pipeline.

This integration removes that gap. The rep creates the webinar from inside CRM, invites the Leads and Contacts they already work with, and reads the results — who registered, who turned up, who didn't, and which deals the session influenced — on the record, without leaving CRM.

Specifically, it handles:

- Inviting CRM records directly, so the invite always goes to current data rather than a stale export.
- Bringing registrations, joins and no-shows back onto the webinar record, and optionally creating CRM records from registrants who aren't in CRM yet.
- Sending the whole email lifecycle — invitation, confirmation, up to three reminders, and separate follow-ups for people who attended and people who missed it.
- Tying attendance to the deals it influenced, so you can see what a webinar was actually worth.

Once enabled, Zoho Webinar becomes a module in CRM, sitting in the left nav alongside Leads and Contacts.

![[01-webinar-list.jpg|The Zoho Webinar module, with six webinars covering every state the product has]]

## Turning the integration on

### Where it lives

The integration is set up from **Setup → Marketplace → Zoho**, on the **Zoho Meetings** card. That one card covers two products from a single login, and it says so: *"One Zoho Meetings login connects both. Set up one or both independently."*

- **For webinars** — sync registrants, track attendance, convert attendees to leads.
- **For online meetings** — instant and scheduled meetings, audio/video and screen sharing, recording and management.

This document is about the webinars half.

![[46-marketplace-zoho-meetings-card.jpg|The Zoho Meetings card, with the two halves you can set up independently]]

> NOTE: The **DEMO** dropdown at the top right of this page is a mock control, not a product feature. It exists so the five account states in the next section can be demonstrated on demand.

### The introduction page comes first

Pressing **Set up** does not drop the user into a settings form. It opens an introduction page that explains what the integration does before asking for anything, with **Enable Integration** waiting at the top right and a **NOT ENABLED** pill next to the title.

![[47-integration-intro-not-enabled.jpg|The introduction page: hero, How it works, and Why teams enable it]]

The page makes its case in four steps — create the webinar in CRM, invite your records, registrations come back, see the revenue — and then gives four reasons teams turn it on: no exporting lists, attendance on the record, emails handled for you, proof it worked.

It closes by committing to exactly what enabling will do, which is worth reading as a summary of the whole feature:

1. Connect your Zoho Webinar organisation to this CRM account.
2. Add a Zoho Webinar module, with its registrants, attendance and recordings.
3. Let you choose which modules a webinar invite can be sent to.
4. Optionally sync your past webinars, and attribute deal revenue to them.

![[48-integration-intro-when-you-enable.jpg|"When you enable, this integration will" — the four commitments]]

### What happens when you press Enable depends on the account

This is the part worth getting right, because the same button leads to five different outcomes. The introduction page looks identical in all five cases; the account is only checked when **Enable Integration** is pressed.

| The user's Zoho Webinar account | What they get | What they can do about it |
|---|---|---|
| No account under this email | A *Select Organization* dialog saying no account was found | Per the dialog |
| Admin of exactly one org | The setup page, with that org already filled in | Carry on and enable |
| Admin of several orgs | The setup page, with an org chooser | Pick one, then enable |
| A member, not an admin | An *Insufficient Permission* dialog | Cancel, or **Notify Super Admin** |
| Trial has expired | A *Trial Expired* dialog | Nothing — see below |

![[11-integration-case1-no-account.jpg|The no-account case: the integration asks which organisation to connect and reports that none was found]]

The two failure cases both explain themselves properly rather than just refusing.

**Not an admin.** The dialog shows the email and a **Member** role badge, then says: *"A Zoho Webinar account was found under this email, but you're a Member of the organisation — not an Admin. Only Webinar Admins can connect the organisation to Zoho CRM."* It then tells them what to do: ask the Webinar Super Admin — named in the copy — to either do the setup for them or promote them to Admin.

![[53-integration-case4-not-an-admin.jpg|The not-an-admin case, naming the Super Admin who can unblock it]]

Because the Super Admin's name is rendered into the sentence, the build needs that name back from the account lookup, not just a permission boolean.

**Trial expired.** The dialog shows a **Trial expired** status badge and the date the trial ended, then asks the user to renew or upgrade and come back.

![[54-integration-case5-trial-expired.jpg|The trial-expired case — note there is no way forward from here]]

> OPEN: This dialog has no upgrade link and no action button, only a close icon. A user who lands here has to leave and find the billing page themselves. It probably wants a link to the upgrade flow.

### Connecting the account

The setup page opens with the connection details. There are only three fields, and the sub-line above them changes with the case — for a user who administers several organisations it reads *"You're an admin in multiple Webinar organisations. Pick the one to connect to Zoho CRM."*

![[49-integration-case3-multiple-orgs.jpg|The setup page for an admin of several organisations]]

- **Email** is read-only. It is the Zoho Webinar account being connected, and the user can't change it here.
- **Organisation** is a dropdown of the organisations they administer, with the first pre-selected. The helper text below it sets the rule: *"Only one organisation can be connected to CRM at a time."*
- **Sync past webinars?** defaults to **Yes**, and decides whether their history comes across as records. The introduction page calls this optional, so a **No** here should be a perfectly normal choice.

### Choosing which modules can be invited

Below the connection details is **Zoho Webinar Invite Modules** — *"Choose the modules from which records can be invited to a webinar."*

This one setting matters more than it looks, because it drives the module dropdown in Send Invite later on. Whatever is ticked here is what a rep can pick from when they invite people to a webinar; untick something and it disappears from that dropdown.

![[12-integration-setup-connection-invite-modules.jpg|Invite Modules: the chip row of what's selected, a search box, and the grouped list]]

The picker is a chip row plus a searchable, grouped checkbox list rather than a flat wall of checkboxes. **Leads**, **Contacts** and **Custom Module 1** come ticked by default, and the count above the chips keeps track (`3 selected:`). Standard modules on offer are Leads, Contacts, Accounts, Potentials, Vendors, Cases, Campaigns and Meetings; custom modules follow in their own group.

> NOTE: The list is already filtered. As the UI puts it: *"Modules without an email field can't receive invites and aren't listed."* If a module has nowhere to send an email, it never appears as an option.

### Deal attribution

The last section is **Webinar Deal Attribution**, and it is the reason the revenue panel on the record works at all: *"It connects your webinar attendees to the CRM deals they influenced and shows how much revenue each webinar contributed."*

It is on by default, with **Linear** pre-selected out of six models.

![[50-integration-attribution-linear-default.jpg|The six attribution models, with Linear selected by default]]

| Model | How it splits the revenue |
|---|---|
| First Webinar Interaction | All of it to the earliest webinar the person attended |
| Last Webinar Interaction | All of it to the most recent webinar they attended |
| **Linear** (the default) | Equally across every webinar they attended |
| Increasing Time Decay | More to earlier webinars, tapering off towards later ones |
| Decreasing Time Decay | More to recent webinars, tapering off towards earlier ones |
| Position-Based | 40% to the first, 40% to the last, 20% shared by everything in between |

Each model has a small bar chart showing the shape of the split, and turning the whole feature off hides the chooser entirely.

> OPEN: *Increasing Time Decay* is described as giving more credit to **earlier** webinars. Time decay usually means the opposite — recent touches get more credit. Worth confirming the two descriptions aren't swapped before anyone builds the maths.

### After it's enabled

Enabling shows a toast — *"Integration was enabled successfully"*, with a **Visit Webinar module** link — and the page becomes the enabled view.

![[51-integration-enabled-active-toast.jpg|The enabled state: an ACTIVE pill, Deactivate, and read-only connection details]]

Three things change. The pill reads **ACTIVE** and the enable button is replaced by **Deactivate** and **Help**. Email and Organisation become read-only text, because you don't re-point a live connection at a different org casually. And *Sync past webinars?* disappears, having already happened.

Invite Modules and Deal Attribution stay editable, which is the point — those are the two things a rep will come back to change. Editing either one raises a save bar at the foot of the page: **"You have unsaved changes"**, with **Cancel** and **Save**. Nothing autosaves.

![[52-integration-enabled-dirty-save-bar.jpg|Ticking one more module raises the unsaved-changes bar]]

Note that the chip row updates the moment you tick something — it went to `4 selected:` with an *Accounts ×* chip immediately — so the chips reflect the pending state, not the saved one.

> OPEN: We never established what **Deactivate** does. Is there a confirmation step, and what happens to the webinar records and history that already exist in CRM?

## Creating a webinar

From the Zoho Webinar list, **Create Webinar** opens a full-page CRM create form — not a modal. It has the usual CRM chrome: a **Standard ▾** layout switcher, **Edit Page Layout**, and **Cancel / Save & New / Save** at the top right.

The form has five sections, and they follow the life of a webinar: what it is, how people sign up, what's allowed in the room, what gets sent before, and what gets sent after.

![[55-create-webinar-details-registration-live.jpg|Webinar Details and Registration Setup, with the defaults the form ships with]]

### Webinar details

Only one field here is required — **Webinar title**, which becomes the record name. Everything else has a sensible default, which means a rep can fill in a title and save.

A few fields are worth knowing about because they aren't what they look like:

- **Webinar Date & Time** is three controls, not one: a date picker, a time dropdown, and a timezone dropdown on its own row underneath. The timezone defaults to **(-6) Central**.
- **Webinar Duration** is two dropdowns — hours (**1 hr**) and minutes (**00 min**).
- **Webinar Owner** and **Organizer** are different people. The owner is the CRM record owner; the organiser is who actually hosts the session.
- **Webinar Cost** looks like a throwaway field with a `$` prefix and a placeholder of `0.00`. It isn't — it's the input to the entire ROI panel on the record later. Cost, cost per attendee and ROI percentage all come from this one number.
- **Repeat Webinar** is a button reading *None* with a pencil beside it. The pencil opens a separate repeat dialog, and setting a schedule there is what produces the recurring webinars you see in the list.

> NOTE: When a repeat schedule is set, two extra fields appear: **Registration Mode** (register for each occurrence individually, or register once and attend any) and **Open Registration for** (all webinars, or a set number of occurrences). Both are recurrence-only — they don't exist on a one-off webinar.

### Registration setup

This section decides whether there's a registration step at all, and what it looks like.

**Registration Type** defaults to *With Registration*. Switching it to *Without Registration* is the significant choice — it takes the registration form and the confirmation email out of the picture entirely, because there's nothing to confirm.

The rest of the section only makes sense while registration is on:

- **Registration Form** picks which form registrants fill in, and each option has a *Preview*. There's a **+ Create New Form** option that opens the form builder.
- **Moderation Type** defaults to *Automatic Moderation*. Choosing *Manual Moderation* is what creates the approve/deny queue on the record — the Waiting for Approval tile and the Approved/Unapproved/Denied tabs only mean anything under manual moderation.
- **Set Registration Limit** is empty by default, meaning no cap. Fill it in and the record starts showing `10 / 200` and *"190 seats left"*.
- **Push Webinar Registrants to CRM** is off by default. Turning it on is what creates CRM records out of registrants who aren't in CRM yet — the mechanism behind it is covered in the emails section.

Two fields gate who can register at all. **Allow/deny registrants from specific countries** and **Allow/Block Specific Domains** both default to no restriction, and picking either an allow or a block variant reveals a further control for the actual list of countries or domains.

> NOTE: **Allow access to join link only through mail** is one of only three checkboxes in the whole form that ships **on**. The other two are in Preferences.

### Preferences

Eight checkboxes covering what people can do during the session — asking questions, anonymous questions, whether questions are visible to everyone, recording, the attendee list, emoji reactions, and post-webinar redirection.

Three of them ship on: **Automatic session recording**, **Video recording** and **Use Emoji reactions**.

![[56-create-webinar-preferences-reminders-followups-live.jpg|Preferences, Reminders and Follow-Ups — the whole back half of the form fits on one screen]]

That first one matters more than it appears. Automatic session recording being on by default is the reason the follow-up emails can promise a recording link — which, as the open questions at the end explain, is not actually holding together yet.

### Reminders

Three reminders, and only the first is switched on: **1st Reminder** defaults to *15 mins before the webinar*, while the 2nd and 3rd default to *None*.

Each reminder has a template beside it, and the template row is conditional — with **2nd Reminder** set to *None*, there is no 2nd Reminder Template row on the form at all. Set an offset and the row appears.

The offsets available run from 2 minutes before through to 1 week before, so the same dropdown covers "just before we start" and "save the date".

### Follow-ups

Both follow-ups are on by default at *2 mins after the webinar ends* — one for attendees, one for absentees, each with its own template.

Which one a person gets is decided by whether they turned up. That's read off the **Webinar Status** on their registrant row after the session, so the split is automatic; nobody segments a list by hand.

There are also two **Include Recording** checkboxes, one per audience, both off by default.

### What blocks a save

Just the title. Pressing **Save** with an empty title scrolls back to the top, puts an error border on the field, and shows the message beneath it:

> NOTE: **"Webinar title cannot be empty"** — this is the only validation message the create form produces. Every other field in all five sections has a default good enough to save with.

![[57-create-webinar-title-required-error.jpg|The only thing standing between a rep and a saved webinar]]

> OPEN: What happens *after* a successful save isn't shown. Which list view does the user land on, and is there a confirmation toast? Worth deciding rather than inheriting whatever the framework does.

## The webinar list

The module list is where a rep starts. Seven views sit across the top — All Webinars, **My Webinars** (the default), Scheduled, Completed, Today's, Ongoing (with a live dot) and On Demand — and the columns tell you the state of every webinar at a glance.

The six rows the mock ships happen to cover every state the product has:

| Webinar | Category | When | Registered | Attended | Rate |
|---|---|---|---|---|---|
| Real Estate Webinar | Scheduled | Mon 11 Aug 2025, 11:00 | 142 | — | — |
| Recurrent Webinar ⟳ | Scheduled | Tue 2 Sep 2025, 10:00 | 89 | — | — |
| Recurrent Webinar ⟳ | Scheduled | Tue 9 Sep 2025, 10:00 | 61 | — | — |
| Contact Webinar | Completed | Mon 11 Aug 2025, 11:00 | 203 | 157 | 77% |
| Product Reveal Webinar | Completed | Wed 3 Sep 2025, 14:00 | 318 | 241 | 76% |
| On Demand Webinar | On-Demand | Mon 10 Mar 2025, 10:00 | 184 | 131 | 71% |

Two things to get right when building this:

1. **Webinar Category and Webinar Type are different columns and mean different things.** Category is the state — Scheduled, Completed, On-Demand — and is colour-coded. Type is what was chosen at creation, Live or On-Demand. A record can quite legitimately be Category *Completed* and Type *Live Webinar*.
2. **Attendance is blank until the session happens.** Attended and Rate show `—` for anything scheduled, because those numbers don't exist yet.

Each occurrence of a recurring webinar is its own row and its own record, with its own registration count — the ⟳ marker beside the name is the only thing telling you they're related.

> OPEN: The list footer says **Total Records 12** while six rows render and pagination reads *1 to 10*. Separately, the filter sidebar is headed **"Filter Invoices by"**. Both are mock bugs, not behaviour to copy.

## A webinar that hasn't happened yet

Open a scheduled webinar and the page is built around one question: who's signed up so far?

![[26-scheduled-live-detail-header-registration.jpg|A scheduled webinar: countdown pill, four header actions, and registration-only figures]]

### The header

The title carries a **– Scheduled** suffix and a countdown pill — *"Starts in 16 mins"*. Four actions sit to the right, and this is the fullest the header ever gets:

- **Start Webinar** — begin the session.
- **Send Invite** — the flow described below.
- **View Registration Link** — the public sign-up link and its tracking.
- **Edit** and **Actions ▾**.

The **Actions ▾** menu is the standard CRM record menu — Clone, Share, Delete, Share via Cliq, Print Preview, and the various customisation entries — and it's identical on every webinar regardless of state.

![[20-detail-actions-menu.jpg|The Actions menu — the same twelve entries on every webinar, whatever its state]]

### Registration overview

Before the session there's no attendance to report, so the summary shows registration only: a donut reading **10 / 200** with *"190 seats left"* beneath it, and a **Waiting for Approval** tile showing **5**.

The `/ 200` and the seats-left line are both driven by the Set Registration Limit field from the create form. With no limit set, there's nothing to count down from.

Three charts follow — registration by module, registration by source (a bar chart with two series, *Visited* and *Registered*), and a daily registration trend with peak-day and average read-outs.

> OPEN: The **View →** link on the Waiting for Approval tile does nothing when clicked. It presumably ought to jump to the Unapproved Registrants tab.

### Approving registrants

Under manual moderation the registrants list splits into three tabs — **Approved (6)**, **Unapproved (6)** and **Denied (3)** — with **Deny All** and **Approve All** buttons at the foot for working through a queue quickly.

### The registration link, and tracking where sign-ups come from

**View Registration Link** opens a small dialog with the public link, a copy button and an embed-code button.

![[27-registration-link-modal.jpg|The registration link, with source tracking switched off]]

Underneath is **Enable Source Tracking for Registration Link**, off by default. Switching it on reveals a table and a **Create New Source Tracking Link** button.

![[28-registration-link-source-tracking-empty.jpg|Source tracking on, with nothing created yet]]

The idea is one link per channel, so you can tell where registrations actually came from. Creating one asks for a single thing — a **Source Name**, with *e.g. Twitter* as the placeholder — and the Add button stays disabled until you type something.

![[29-create-source-tracking-link-dialog.jpg|Naming a source. Add is disabled until the field has a value]]

Once created, the row carries who made it and when, a **Visited Count**, a **Registered Count**, and three actions: copy, embed code, and a toggle to switch that source off without deleting it.

![[30-source-tracking-link-created.jpg|A created source link, already counting visits and registrations]]

Those two counts are what feed the *Visited* and *Registered* series in the registration-by-source chart above.

> USECASE: A rep is promoting the same webinar on LinkedIn and in a newsletter. They create one tracking link for each, and afterwards the record shows 14 visits and 3 registrations from LinkedIn against the newsletter's numbers — so next quarter they know where to spend the effort.

### Sending an invite

**Send Invite** is two steps. There is deliberately no separate "pick a module" step; the record picker opens straight away with a module dropdown inside it.

**Step one** is choosing who. The module dropdown is populated from the Invite Modules setting configured back in Setup, then a view dropdown, then the records themselves with checkboxes.

![[03-send-invite-record-picker.jpg|Step one: the module dropdown, a view filter, and the records]]

Selecting records raises a bar with **Remove ALL** and **Next**.

![[04-send-invite-records-selected.jpg|Two records selected, ready to move on]]

**Step two** is the CRM Mass Email compose screen — the recipients in **To**, a **Select Template** button, the **From** address, the usual sending warnings, and **Send Options**.

![[05-mass-email.jpg|Step two: Mass Email, with the chosen template shown as a preview link]]

**Select Template** lists the available templates with a search box and a **+ Create Template** option. Creating a template from here skips the "which module, which type" dialog, because the context has already answered both — it's a webinar invitation.

![[06-select-template.jpg|Choosing the invitation template]]

> NOTE: The dependency to respect: the module dropdown in step one offers exactly what's ticked in Invite Modules. Turn Accounts off in Setup and it must disappear from here.

### The related lists, before the session

The related lists on a scheduled webinar are all in their "collecting" state, and it's worth seeing them together because they change completely after the session:

| Related list | Before the webinar |
|---|---|
| Notes | Empty, with **+ Add Note** |
| Invited | Tabs for Invited / Registered / Not Registered, and an **Invite** button |
| Polls | The polls exist, but every vote count is **0**, and there's a **Create Poll** button |
| Q&A | A placeholder: *"Q&A will be available after the webinar is completed."* |
| Recordings | *"No recordings available."* |
| Session Files | An **Attach Files** button and an empty state |

There is no **Webinar Revenue** panel at all on a scheduled webinar. It only appears once there's attendance to attribute.

> OPEN: The *Hide Details* panel on the record shows the same placeholder content — *Test Webinar*, *XYZ*, *1000* — on every single record rather than that record's own values. A mock bug, but flagging it because it's easy to reproduce accidentally.

## A webinar that has happened

Once a webinar is over the page answers a different question. It stops asking who's coming and starts reporting what happened.

![[21-completed-detail-overview.jpg|A completed webinar. Note the related-list rail on the left has grown]]

### What changes

The clearest way to hold this in your head: **before the webinar the page collects, after the webinar it reports.** The same related lists swap their input controls for read-outs.

| | Scheduled | Completed |
|---|---|---|
| Header actions | Start, Send Invite, Registration Link, Edit, Actions | Edit and Actions only |
| Registration overview | Donut with seats left, plus approvals | Three tiles: total registered, attendees, absentees |
| Polls | Vote counts all 0, **Create Poll** button | Full results, no Create Poll |
| Q&A | *"available after the webinar is completed"* | Questions **with the host's replies** |
| Session Files | **Attach Files** button, empty | The files, listed |
| Invited | Invited / Registered / Not Registered | Adds **Attended** and **Not Attended** |
| Webinar Revenue | Not present | Present |

The registrant list also grows from three tabs to six — **All Attendees**, **All Absentees**, **All Registrants**, and the three approval states — and picks up two new columns, **Polls** and **Q&A**, showing what each person actually did in the session, plus a **Webinar Status** badge reading *Attended* or *Not Attended*.

![[22-completed-attendees-registrants-list.jpg|The registrant list after the session, with per-person participation]]

Look at the module column in that screenshot: some rows say Leads or Contacts, and some say `—`. Those dashes are people who registered but aren't in CRM at all. They're the reason push-to-CRM and the registration forms exist.

### Polls, questions and files

**Polls** report per question: each option with its vote count, a percentage voted and a total. There's a *Poll Answered by* filter so you can look at just Leads, just Contacts, or people not in CRM.

![[23-completed-polls.jpg|Poll results, filterable by who answered]]

Under the results is a participant table with name, email, company, phone and owner — so a poll answer is traceable back to a CRM record, which is the whole point of running the poll inside CRM.

**Q&A** renders as a conversation: who asked, when, which module they belong to, the question, and — only on a completed webinar — the host's reply beneath it.

![[24-completed-qa-with-host-replies.jpg|Questions with the host's answers. Some questions have no reply, so replies are optional]]

> USECASE: A rep opens a completed webinar and sees that a Lead asked *"Can we schedule a demo with your team after this?"* and never got an answer in the room. That question is sitting on the CRM record next to the person's name, so it becomes a follow-up call rather than a lost opportunity.

**Session Files** lists what was shared — file name with a type icon, size and date added.

![[25-completed-recordings-session-files.jpg|Session files. Note the Recordings list directly above it is empty]]

### Webinar revenue

This is the payoff for the attribution setting from Setup, and it only exists on webinars that have happened.

![[17-webinar-revenue-roi-attribution.jpg|The ROI tiles, and how the pipeline breaks down]]

Six tiles across the top:

| Tile | In the mock | Where it comes from |
|---|---|---|
| Cost | $800 | The Webinar Cost field from the create form |
| Revenue (Won) | $16,800 | Attributed revenue from won deals |
| ROI | +2000% | Revenue against cost |
| In Pipeline | $32,450 | Attributed value of deals still open |
| Cost / Attendee | $53 | Cost divided by attendees |
| Revenue / Attendee | $1,120 | Revenue divided by attendees |

Then two tables. **Deals Won** lists the closed-won deals with their amounts, accounts and contacts.

![[18-webinar-revenue-deals-won.jpg|The deals this webinar is credited with winning]]

**Deals in Pipeline** does the same for open deals, with a probability column.

![[19-webinar-revenue-deals-in-pipeline.jpg|Open deals, with probability]]

> OPEN: Two problems in this panel. The tiles don't reconcile with the tables — Revenue (Won) reads $16,800 while the seven Deals Won rows add up to $16,000. And *Deals in Pipeline* contains Closed Won and Closed Lost rows at 100% and 0%, which contradicts the name. Both need settling before the numbers can be trusted.

## On-demand webinars

An on-demand webinar is one people watch afterwards rather than attending live, and the mock treats it as its own state — the title carries a **– On Demand** suffix.

![[14-ondemand-detail-overview.jpg|An on-demand webinar, with attendance figures and no live-session controls]]

Because there's no start time to turn up for, the header loses both **Start Webinar** and **Send Invite**, leaving just **Edit** and **Actions**. The registration overview looks like a completed webinar's — total registered, attendees, absentees — and the revenue panel is present.

![[15-ondemand-attendees-registrants-list.jpg|The on-demand registrant list, with the same six tabs a completed webinar gets]]

The related-list rail is noticeably shorter: no Polls, no Recordings, no Session Files. The Q&A list has questions but no host replies.

![[16-ondemand-invited-related-list.jpg|The Invited list on an on-demand record, now showing attendance]]

> OPEN: Two things about this state need a decision. First, should an on-demand webinar really have no **Send Invite**? You'd think inviting people to watch a recording is exactly the point. Second, an on-demand webinar *is* a recording, so having no **Recordings** list looks like an oversight rather than a decision. It's also worth deciding whether there's a "published but nobody's watched it yet" state — the mock only shows one with attendance already in it.

## The emails

Seven emails carry a webinar: the invitation, the confirmation when someone registers, up to three reminders, and two different follow-ups depending on whether the person showed up.

### Where the templates live

They appear in two places, and the two don't agree with each other.

**Setup → Templates**, filtered to the Zoho Webinar module, lists seven, each with a one-line description of when it's sent.

![[33-templates-zoho-webinar-7-defaults.jpg|Setup → Templates, filtered to Zoho Webinar: seven templates]]

**Modules and Fields → Zoho Webinar → Preferences** lists eight, under the heading *Customise Email Notifications*.

![[43-modfields-zoho-webinar-preferences.jpg|The same emails under the module's own Preferences tab — but eight of them, with different names]]

| Setup → Templates (7) | Module Preferences (8) |
|---|---|
| Webinar Invitation Template | Send Invite Template |
| Confirmation Template | Webinar Confirmation Template |
| 1st / 2nd / 3rd Reminder Template | 1st / 2nd / 3rd Reminder Template |
| Attendees Follow-up Template | Attendees Follow-up Template |
| Absentees Follow-up Template | Absentees Follow-up Template |
| — | **Meetings Cancelled Template** (its button is disabled) |

> OPEN: Three things wrong here at once. Two templates have different names in the two places. Preferences has a **Meetings Cancelled Template** that Setup → Templates doesn't list at all, and its *Customise Template* button is greyed out with no explanation. And the Preferences page says these emails are *"managed here, not under Setup › Templates"* — while Setup → Templates is listing them. Someone needs to pick one home for these.

### Creating a template

Creating one from Setup asks two questions first: which module, and which of the eight types it is.

![[34-create-email-template-dialog.jpg|Module and type — the two things that decide what the template can do]]

The type is the important half, because it determines what the template is allowed to contain. When you reach this dialog from somewhere that already implies the type — a template slot on the create-webinar form, or the Send Invite flow — the dialog is skipped entirely.

Next comes the gallery, which offers six basic layouts and nothing else: Blank, one column, two column, two column with an image (two variants), and three column.

![[35-template-gallery-basic.jpg|The gallery. The chosen type rides along as a chip at the top]]

Then the editor. The type is the title, the layout and module sit underneath it, and the body carries a placeholder written for that specific type — for an invitation, *"Write the webinar invitation email here. Type # to insert a merge field."*

![[36-template-editor-invitation.jpg|The editor, with the type named in the header and a type-specific placeholder]]

### What each type is allowed to link to

This is the rule set that matters most in the whole feature, and it is enforced in two directions. The **Insert Link** dropdown only offers the link types that template's type permits — and the template **will not save** unless it contains the one link its type depends on.

| Template type | Can link to | Must contain |
|---|---|---|
| Webinar Invitation | Web URL, Email, Registration Link, calendar links | **Registration Link** |
| Confirmation Email | Web URL, Join URL, Cancel Registration, calendar links | **Join URL** |
| 1st / 2nd / 3rd Reminder | Web URL, Join URL, Cancel Registration, calendar links | **Join URL** |
| Attendees Follow-up | Web URL, Join URL, Recording Link, calendar links | **Recording Link** |
| Absentees Follow-up | Web URL, Join URL, Recording Link, calendar links | **Recording Link** |
| None | All of the above | Nothing |

The logic is straightforward once you see it: an invitation needs somewhere to sign up, a reminder needs somewhere to join, and a follow-up needs the recording. The calendar links — Add to Google, Yahoo, Outlook, Zoho and a generic one — are available on every type.

You can see the rule working in the Insert Link dialog. On an invitation template, the dropdown offers eight options and no Join URL, no Cancel Registration, no Recording Link.

![[38-insert-link-dialog.jpg|Insert Link on an invitation template. A Web URL asks for an address]]

Pick a system-supplied link like the registration link and the **Link Address** field disappears altogether, because the URL is resolved per registrant when the email actually goes out. The display text pre-fills to *"Register Now"* with a note explaining what the link does.

![[40-insert-registration-link.jpg|The registration link needs no address — just the text to show]]

And if you try to save without it, the editor stops you:

![[39-required-link-save-error.jpg|The exact message: what's missing, and what to do about it]]

The message is built from the type name and the required link, so each type produces its own version of the same sentence.

Saving asks for a name — pre-filled, in this case *"Webinar Invite - Zoho Webinar"* — and confirms where it's going.

![[41-save-template-dialog.jpg|Naming the template on save]]

> OPEN: After saving, the list comes back showing only the seven original templates. The new one isn't there and there's no toast to say the save worked, so from the user's side a successful save is indistinguishable from a failure.

![[42-templates-list-after-save.jpg|Back at the list after saving. The new template is nowhere to be seen]]

### Merge fields

Typing `#` in the editor body opens the merge-field picker: a category dropdown and that category's fields.

![[37-merge-field-picker.jpg|The merge-field picker, showing the Webinar Details category]]

On an invitation there are three categories — **Webinar Details**, **Users** and **Organization**. Every email after the invitation adds a fourth, **Registrations**, at the top of the list.

That difference has a reason worth understanding. An invitation goes to a CRM record — someone who hasn't registered yet, so there's no registration to draw from. Every later email goes to a *registrant*, so per-person values become available: their join URL, their cancellation link, their timezone, their calendar links.

| Category | What's in it |
|---|---|
| Webinar Details | Title, date and time, organiser, duration, description |
| Registrations | Registration id, name, email, country, timezone, join URL, cancel registration, registration URL, handouts, audio details, the calendar links, and more |
| Users | User id, name, email, role, profile |
| Organization | Company name, website, phone, and the address fields |

Note that per-registrant links show up twice — once as an Insert Link type and again as a Registrations merge field. Two routes to the same value.

### Registration forms, and getting registrants into CRM

The **Registration Form** tab on the module is where push-to-CRM is actually configured: *"Forms used to collect registrant details and push them into CRM as records."*

![[44-modfields-registration-forms.jpg|Registration forms, and the module each one pushes into]]

The important column is **Push As**. It decides which module a registrant becomes a record in — the *Leads form* creates Leads, the *Contacts* form creates Contacts. This is what turns those `—` rows in the registrant list into real CRM records.

> OPEN: The **Registration Form** dropdown on the create-webinar form offers *Default Form*, *Real Estate Form* and *Stock Trading Form* — none of which are the two forms configured here. One of these two lists is wrong, and we need to know which one drives the other.

## Things we still need to decide

Everything above is what the mock actually does. This section is what it doesn't answer. They're grouped by who needs to answer them, and the first one is genuinely blocking.

### The blocking one

**Where does the recording come from?**

The Recordings related list is empty on every record in the mock, including a completed webinar whose *Automatic session recording* preference is on by default. But the Attendees Follow-up and Absentees Follow-up template types **require** a Recording Link, and refuse to save without one.

So as it stands, two of the seven lifecycle emails depend on something nothing in the product produces. Either recordings need to arrive somewhere and appear in that list, or the required-link rule for follow-ups is wrong. This needs answering before anyone builds either piece.

### Decisions for product

1. **Which template list is real** — seven under Setup → Templates, or eight under Module Preferences? And which of the two competing names for the invitation and confirmation templates is canonical?
2. **Why is the Meetings Cancelled Template's edit button disabled?** Is that a permission rule, an unbuilt screen, or a template that shouldn't be listed?
3. **Should on-demand webinars have Send Invite?** And should they have a Recordings list, given that an on-demand webinar is a recording?
4. **Is there an on-demand state before anyone has watched?** The mock only shows one with attendance already recorded.
5. **What does Deactivate do** to the integration and to the records that already exist?
6. **What does Notify Super Admin actually do**, and what does the blocked user see afterwards?
7. **Are the two Time Decay models described correctly?** *Increasing* is said to favour earlier webinars, which is the opposite of how time decay normally works.

### Decisions for engineering

1. **Are Webinar Owner, Webinar Cost and Repeat Webinar module fields?** They're on the create form and in the list filters, but absent from the module's Fields tab. Webinar Cost drives the entire ROI panel, so this isn't cosmetic.
2. **Which registration form list is authoritative** — the create-form dropdown or the module's Registration Form tab?
3. **How is Attend. Rate calculated** — attendees over registrations, or over approved registrations? The mock shows 77%, 76% and 71% without showing the working.
4. **Why don't the revenue tiles match the deal tables?** ($16,800 against $16,000.)
5. **Why does Deals in Pipeline contain closed deals?**
6. **Where do the source-tracking visit and registration counts come from**, and how do they relate to the registration-by-source chart?
7. **Does the new template appear in the list after saving,** and what confirms the save to the user?

### Decisions for design

1. **Where should the Waiting for Approval "View" link go?** It currently does nothing.
2. **Should the Trial Expired dialog offer a way forward?** Right now it's a dead end with only a close icon.
3. **Does Allow anonymous questions depend on Allow attendees to ask questions?** The mock doesn't enforce any relationship.
4. **What confirms a saved webinar,** and where does the user land?
5. Two copy bugs to fix rather than reproduce: the filter sidebar headed **"Filter Invoices by"**, and the *Hide Details* panel showing placeholder values on every record.

### Assumptions this document makes

Stated so they can be corrected rather than inherited:

- **Webinar Category is derived, not entered.** Nothing sets it directly; it follows from the type and whether the session has happened.
- **Co-Organizer is multi-value**, because record pages show two co-organisers while the create form offers a single select.
- **A recurring webinar creates one record per occurrence**, since the two recurring rows in the list have separate dates and separate registration counts.
- **Registration Mode and Open Registration for are recurrence-only.**
- **The required-link error message is templated** from the type name and the link, so all seven types share one sentence with different nouns.
- **The DEMO switcher is a mock control**, and the five account states are outcomes of a real lookup at the moment Enable is pressed.

## Appendix: full field reference

The narrative above covers what matters and why. This appendix is the exhaustive version, for when you're actually building a form and need every default in one place.

### Every control on the create-webinar form

| Section | Field | Type | Required | Default |
|---|---|---|---|---|
| Webinar Details | Webinar title | Single-line text | **Yes** | Empty |
| Webinar Details | Webinar Type | Picklist | No | Live Webinar |
| Webinar Details | Webinar Date & Time — date | Date input | No | Today |
| Webinar Details | Webinar Date & Time — time | Picklist | No | 10:00 AM |
| Webinar Details | Webinar Date & Time — timezone | Picklist | No | (-6) Central |
| Webinar Details | Webinar Duration — hours | Picklist | No | 1 hr |
| Webinar Details | Webinar Duration — minutes | Picklist | No | 00 min |
| Webinar Details | Webinar Owner | Picklist + lookup | No | Rao Priya |
| Webinar Details | Organizer | Picklist | No | Jayasuriya |
| Webinar Details | Co-Organizer | Picklist | No | None |
| Webinar Details | Repeat Webinar | Button + dialog | No | None |
| Webinar Details | Webinar Cost | Text with $ prefix | No | Empty |
| Webinar Details | Description | Multi-line text | No | Empty |
| Webinar Details | Registration Mode | Picklist | No | Register and attend each event individually — recurrence only |
| Registration Setup | Open Registration for | Picklist | No | All Webinars — recurrence only |
| Registration Setup | Registration Type | Picklist | No | With Registration |
| Registration Setup | Registration Form | Picklist | No | Default Form |
| Registration Setup | Moderation Type | Picklist | No | Automatic Moderation |
| Registration Setup | Set Registration Limit | Number | No | Empty (no cap) |
| Registration Setup | Push Webinar Registrants to CRM | Checkbox | No | Off |
| Registration Setup | Allow/deny registrants from countries | Picklist | No | No Restrictions |
| Registration Setup | Select Allowed Countries | Multi-select | No | Empty — conditional |
| Registration Setup | Allow/Block Specific Domains | Picklist | No | No Restriction |
| Registration Setup | Add Allowed Domains | Multi-entry | No | Empty — conditional |
| Registration Setup | Post_Registration Custom Redirection | URL | No | Empty |
| Registration Setup | Post Redirection URL | URL | No | Empty — conditional |
| Registration Setup | Allow access to join link only through mail | Checkbox | No | **On** |
| Registration Setup | Confirmation Email Template | Template picker | No | Webinar Confirmation Template |
| Registration Setup | Who can Join | Picklist | No | Anyone can Join |
| Preferences | Allow attendees to ask questions | Checkbox | No | Off |
| Preferences | Allow anonymous questions | Checkbox | No | Off |
| Preferences | Show questions to all | Checkbox | No | Off |
| Preferences | Automatic session recording | Checkbox | No | **On** |
| Preferences | Video recording | Checkbox | No | **On** |
| Preferences | Display attendee list to all | Checkbox | No | Off |
| Preferences | Use Emoji reactions | Checkbox | No | **On** |
| Preferences | Post webinar Re-direction | Checkbox | No | Off |
| Reminders | 1st Reminder | Picklist | No | 15 mins before the webinar |
| Reminders | 1st Reminder Template | Template picker | No | 1st Reminder Template |
| Reminders | 2nd Reminder | Picklist | No | None |
| Reminders | 2nd Reminder Template | Template picker | No | Hidden while None |
| Reminders | 3rd Reminder | Picklist | No | None |
| Reminders | 3rd Reminder Template | Template picker | No | Hidden while None |
| Follow-Ups | Send Follow-up Email to Attendees | Picklist | No | 2 mins after the webinar ends |
| Follow-Ups | Attendees Follow-up Template | Template picker | No | Attendees Follow-up Template |
| Follow-Ups | Send Follow-up Email to Absentees | Picklist | No | 2 mins after the webinar ends |
| Follow-Ups | Absentees Follow-up Template | Template picker | No | Absentees Follow-up Template |
| Follow-Ups | Include Recording for Attendees | Checkbox | No | Off |
| Follow-Ups | Include Recording for Absentees | Checkbox | No | Off |

### Picklist values, verbatim

- **Webinar Type** — Live Webinar · OnDemand Webinar
- **Time** — 9:00 AM · 10:00 AM · 11:00 AM · 12:00 PM · 1:00 PM · 2:00 PM
- **Timezone** — (-5) Eastern · (-6) Central · (-7) Mountain · (-8) Pacific · (+0) UTC · (+5:30) IST
- **Duration** — 1 to 24 hr; 00 · 15 · 30 · 45 min
- **Registration Type** — With Registration · Without Registration
- **Moderation Type** — Automatic Moderation · Manual Moderation
- **Country restriction** — No Restrictions · Allow registrants from Countries · Block registrants from Countries
- **Domain restriction** — No Restriction · Allow specific email domains · Block specific email domains
- **Who can Join** — Anyone can Join · Only Authenticated Users can Join
- **Reminder offsets** — None · 2 / 5 / 10 / 15 / 30 mins before · 1 / 2 / 6 / 12 hours before · 1 day before · 1 week before
- **Follow-up offsets** — None · 2 / 5 / 10 / 15 mins after the webinar ends · 1 / 2 / 6 hours after · 1 day after
- **Template Type** — None · Webinar Invitation · Confirmation Email · 1st Reminder · 2nd Reminder · 3rd Reminder · Attendees Follow-up · Absentees Follow-up
- **Template module** — Zoho Webinar · Leads · Contacts · Vendors · Custom Module 1
- **Attribution model** — First Webinar Interaction · Last Webinar Interaction · Linear · Increasing Time Decay · Decreasing Time Decay · Position-Based

### The module's own fields

From **Modules and Fields → Zoho Webinar → Fields** — the authoritative list of 26.

![[45-modfields-fields-tab.jpg|The module's Fields tab, the authoritative field and type list]]

| Field | Type |
|---|---|
| Webinar Title | Single Line |
| Webinar Category | Pick List |
| Webinar Type | Pick List |
| Webinar Date & Time | Date/Time |
| Webinar Duration | Duration |
| Organiser | Lookup |
| Co-Organiser | Lookup |
| Description | Multi Line |
| Registration Type | Pick List |
| Registration Form | Pick List |
| Moderation Type | Pick List |
| Set Registration Limit | Number |
| Push to CRM | Boolean |
| Allow/deny registrants from specific countries | Multi Select |
| Allow/block specific domains | Multi Select |
| Post_Registration Custom Redirection | URL |
| Allow access to join through email | Boolean |
| Allow only authenticated Zoho Users with a Zoho account | Boolean |
| Send Confirmation to Registrants | Boolean |
| Allow attendees to ask questions | Boolean |
| Allow anonymous questions | Boolean |
| Show questions to all | Boolean |
| Automatic session recording | Boolean |
| Video recording | Boolean |
| Display attendee list to all | Boolean |
| Use Emoji reactions | Boolean |

> NOTE: This list is missing several fields the create form and list filters actually use — Webinar Owner, Webinar Cost, Repeat Webinar, Post Webinar Re-direction, and both follow-up offsets. That gap is engineering question 1 above.

### Integration settings

| Section | Field | Type | Default |
|---|---|---|---|
| Connection | Email | Read-only | The signed-in Webinar account |
| Connection | Organisation | Dropdown | First org the user administers |
| Connection | Sync past webinars? | Yes / No | **Yes** |
| Invite Modules | Module selection | Checkboxes + chips | Leads, Contacts, Custom Module 1 |
| Deal Attribution | Enable Deal Revenue Attribution | Toggle | **On** |
| Deal Attribution | Revenue Attribution Type | Six cards | **Linear** |
