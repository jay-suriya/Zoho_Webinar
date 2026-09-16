# Zoho Webinar in Zoho CRM — Build Specification

This document was written by clicking through the mock at `webinar.html` as it stands on `master`, screen by screen, and by reading the rule sets out of the page's own JavaScript. Every screenshot in it is a real capture from that file, not a redraw. Every picklist value is listed in the order the UI shows it. Where the mock does not answer a question, the document says so in an **Open question** callout rather than filling the gap with a guess — so a sentence here is either something you can see in the mock, or something explicitly marked as undecided.

It is written to be built from. If you have to open the mock to answer a question about a field, a state or a rule, this document has failed; tell us which question, and it gets fixed.

**The business used in the examples** is Northline Capital, a wealth-management firm. They advise business owners on their money and earn on the portfolios they end up managing. They cannot cold-call their way to a portfolio, so once a month they run a free market-outlook webinar — an hour on where rates are going, no pitch until the last five minutes. Two hundred people register, sixty turn up, and that room is the top of the pipeline. Jay is an advisor there, and his screen is the one every flow in this document is seen from.

## Contents

1. [Introduction](#1-introduction)
2. [Turning the integration on](#2-turning-the-integration-on)
3. [Creating a webinar](#3-creating-a-webinar)
4. [Co-organisers](#4-co-organisers)
5. [The registration page](#5-the-registration-page)
6. [The webinar list](#6-the-webinar-list)
7. [A webinar that hasn't happened yet](#7-a-webinar-that-hasn-t-happened-yet)
8. [A webinar that has happened](#8-a-webinar-that-has-happened)
9. [On-demand webinars](#9-on-demand-webinars)
10. [The emails](#10-the-emails)
11. [Attribution](#11-attribution)
12. [Things we still need to decide](#12-things-we-still-need-to-decide)
13. [Appendix A — every field in the create form](#13-appendix-a-every-field-in-the-create-form)
14. [Appendix B — integration settings, templates and directories](#14-appendix-b-integration-settings-templates-and-directories)

## 1. Introduction

### What Zoho Webinar is

Zoho Webinar is Zoho's webinar product. You schedule a session, publish a registration form, and people sign up. The product emails them along the way — an invitation, a confirmation when they register, up to three reminders before it starts, and afterwards a follow-up that differs depending on whether they turned up. It runs the session itself, and it keeps what happened in the room: the polls you ran, the questions people asked, the recording, the files you shared.

None of that is missing today. Zoho Webinar does the webinar well.

### What it cannot do on its own

It has no business context. Sixty people attended Jay's outlook webinar; Zoho Webinar can tell him sixty names, sixty email addresses and what each of them did in the hour. It cannot tell him the only thing he needs on Monday morning: who to call first.

Three questions, none of which the webinar can answer on its own:

- **Who is worth the call?** Sixty names, ranked how?
- **Is this question a signal?** Someone asked "what is your minimum portfolio size" — chase it or not?
- **What do we already know about them?** Have we spoken? Is there a proposal out?

The middle one is the sharpest. That question from a stranger who found the webinar on LinkedIn is a curious browser. The identical question from someone Jay has met twice, with a proposal sitting at negotiation, is a buying signal. Same words, completely different follow-up — and the webinar shows both of them the same way, because it had never heard of either person before they registered.

Northline already holds that context. Every client and every lead is in CRM, with the history, the calls and the open deals. It just has no idea the webinar happened. So today the only thing joining the two halves is somebody exporting a spreadsheet:

- **Export** a recipient list out of CRM to invite anyone, so the invite goes to whatever the data looked like on export day rather than to the record as it stands.
- **Re-import** the registrants afterwards, hand-matching the ones who already exist so as not to create duplicates.
- **Guess** at the result, because attendance lives in one product and pipeline in the other.

### What this integration closes

Zoho Webinar becomes a module inside CRM, sitting in the left nav alongside Leads and Contacts, and each webinar is a record like any other:

- **Invite CRM records directly**, so the invite always goes to current data — and to whichever modules the admin allows, not only Leads and Contacts.
- **Registrations, joins and no-shows land back on the webinar record**, with the option of creating CRM records from registrants who were not in CRM to begin with, so there is nothing to re-import.
- **The whole email lifecycle is sent from CRM** — invitation, confirmation, up to three reminders, and separate follow-ups for attendees and absentees — from templates that live with the module.
- **Attendance is tied to the deals it influenced**, through an attribution model chosen once in setup, so what a webinar was worth is a figure on the record instead of a feeling.

> NOTE: One sentence to hold on to for the rest of the document: **before the webinar the record collects, after the webinar it reports.** Nearly every difference between the two record states follows from that.

## 2. Turning the integration on

### Where it starts

Setup ▸ Marketplace ▸ Zoho lists the Zoho apps that connect to CRM. Zoho Webinar and Zoho Meetings share one card, because they share one login: **For webinars** and **For online meetings** are set up independently, and the note on the card says so.

![[01-marketplace-zoho.jpg|Setup ▸ Marketplace ▸ Zoho. One card carries both paths. The DEMO switcher at the top right is a mock-only control for walking the blocking states below]]

> NOTE: The **DEMO** dropdown exists only in the mock. It selects which account situation to simulate, and is how the five cases below are reached. `window._selectedCase` defaults to **2**.

### The account question is answered at the card

Clicking **Set up** checks the account situation before showing anything else — `integWebinarCardSetup()` branches on the case and returns early for the three that cannot proceed. This matters: a user with no Zoho Webinar account is not walked through a marketing page and a four-step form before being told they cannot have it.

| Case | Situation | What happens |
|---|---|---|
| 1 | No Zoho Webinar account for this email | Modal offering to create one |
| 2 | One Webinar organisation | Straight to the introduction page |
| 3 | Several organisations | Introduction page, then an org picker in step 1 |
| 4 | Account exists, user is a Member not an Admin | Modal explaining only Admins can connect |
| 5 | Trial expired | Modal explaining the trial has ended |

![[11-case1-no-account.jpg|Case 1. The only way forward is creating a Webinar account]]

![[12-case4-not-admin.jpg|Case 4. A Member cannot connect the integration. The modal has no action beyond Cancel — the "Notify Super Admin" button was deliberately removed, because CRM cannot actually send that mail]]

![[13-case5-trial-expired.jpg|Case 5. Trial expired]]

### The introduction page comes before the form

Cases 2 and 3 land on an introduction page rather than on settings. It explains what the integration makes possible — what you get, and what it solves — and the only action on it is **Setup** at the top right. The badge next to the title reads **NOT ENABLED** until the integration is on, and flips to a green **ENABLED** afterwards, at which point the same button opens the enabled settings panel instead of the form.

![[02-intro-hero.jpg|The introduction page. Setup is the only action; the body has no buttons at all]]

![[03-intro-features.jpg|What you get — five features, each with what it changes for the user]]

![[04-intro-solves.jpg|What it solves. Each old way strikes itself through as the row arrives, answered by the line beneath it]]

### Setup is a four-step wizard, and the steps accumulate

**Setup** opens a wizard: four steps, each with **Cancel** and **Next**, and the last Next reading **Enable Integration**. Answering a step does not hide it — every answered step stays on the page, so while choosing an attribution model you can still scroll up and re-read which modules you allowed. Only the step you are on carries the two buttons; earlier footers are hidden, because a pair of buttons under a settled section reads as though it is still in play.

**Cancel** abandons setup and returns to the introduction page, or to the enabled panel if the integration is already on. Re-opening the setup panel always resets to step 1 — `integShowPanel('integ-setup-panel')` calls `setupStep(1)` — so a second visit never resumes mid-wizard.

> NOTE: The steps are `.wz-step` blocks shown and hidden in place, not four separate pages. That is deliberate: `setupActivateIntegration()` reads the answers straight out of the DOM at the end, so every earlier field has to still exist when the last button is pressed.

**Step 1 — Email and organisation.** The Zoho account being connected, and which Webinar organisation to connect it to. The organisation picklist lists the orgs on that account (in the mock: Acme Corp Webinars, ClientCo Marketing, Consulting Practice) and carries the rule underneath it: *"Only one organisation can be connected to CRM at a time."* Case 3 is the reason this field exists.

![[05-wizard-step1.jpg|Step 1. Email, organisation, and the one-org-at-a-time rule]]

**Step 2 — Sync past webinars?** A Yes/No radio pair, **Yes** preselected. Yes imports the webinars that already exist in the connected Webinar organisation, so the module is not empty on day one.

![[06-wizard-step2.jpg|Step 2, with step 1 still above it — scroll up and the connection is still there to re-read]]

**Step 3 — Who Can Participate From CRM.** Which CRM modules a webinar invite may be sent to. One card, a search box, a flat checkbox list. **Leads and Contacts are mandatory** — checked, red asterisk, muted label, and `imToggle()` returns early for anything in `IM_LOCKED`, so they cannot be turned off. Everything else starts unchecked.

This is the section with the longest reach: it drives the module dropdown in **Send Invite**. Turn a module off here and its records can no longer be added to a webinar.

![[07-wizard-step3.jpg|Step 3. Leads and Contacts are locked on; the rest of the list is the modules a business builds to hold people]]

**Step 4 — Webinar Deal Attribution.** Whether to attribute deal revenue to webinars at all, and if so, under which model. The section explains itself first — *"Webinar Deal Attribution tells you which webinars actually helped close your deals"* — then offers **Enable Deal Revenue Attribution**, and below it the six models as cards, each with a worked example. **Linear** is selected by default, and the copy is explicit that the whole thing is optional: *"Deal Attribution is optional. You can enable it later from the integration settings if you'd prefer to skip this for now."*

![[08-wizard-step4.jpg|Step 4. The explanation comes before the choice]]

![[09-wizard-attribution-models.jpg|The six models, each with the A → B → C example that shows what it does to the money]]

The models themselves are specified in [Attribution](#11-attribution).

### The enabled page

**Enable Integration** activates the integration and lands on the enabled panel: the same connection details, the sync answer carried across from step 2, the participating modules and the attribution model, with a dirty-state Save bar that appears as soon as anything changes.

![[10-enabled-panel.jpg|The enabled panel. Everything set in the wizard is editable here]]

> OPEN: Disconnecting is not modelled. The enabled panel has no disconnect or re-authorise action, and `mpDisconnectWebinar()` only resets the marketplace card's own button. What happens to synced webinars, registrants and attribution figures when an admin disconnects is undecided.

## 3. Creating a webinar

### Where it starts

Once the integration is on, **Zoho Webinar** is a module in the left nav. Its list view has the standard CRM chrome, and **Create Webinar** opens a full-page form — not a modal — with **Cancel**, **Save & New** and **Save** at the top right, and **Edit Page Layout** next to the layout name, because this is a CRM module like any other.

![[14-create-form-details.jpg|The create form. Five sections: Webinar Details, Registration Setup, Preferences, Reminders, Follow-Ups]]

The form has five sections in this order: **Webinar Details**, **Registration Setup**, **Preferences**, **Reminders**, **Follow-Ups**. Every field, with its type, default and full option list, is in [Appendix A](#13-appendix-a-every-field-in-the-create-form). What follows is only the fields that do something a developer would not guess.

### The fields that surprise

**Webinar Type** is the branch that changes the form. **Live Webinar** is the default; **OnDemand Webinar** replaces Webinar Duration with a **Video File** picker, adds **Allow video play/pause**, and drops Reminders and Follow-Ups, because there is no start time to remind anyone about. See [On-demand webinars](#9-on-demand-webinars).

**Webinar Date & Time** is a compound control: a native date input and a time picklist inside one bordered box. **Webinar Timezone** is a row of its own directly beneath it.

**Webinar Owner** and **Organizer** are two different things and both are picklists with a search box inside the dropdown. The Owner is the CRM user who owns the record; the Organizer is who runs the session in Zoho Webinar.

> NOTE: The search box inside those dropdowns is why `.cs-dd:has(.co-search)` sets a `min-width` — without it the dropdown inherits the button's width and the search field is clipped.

**Repeat Webinar** opens its own modal (No Repeat / Daily / Weekly / Monthly, with an interval and an end condition) and writes a summary back onto the field. A repeating webinar appears in the list as several rows, one per occurrence.

![[23-repeat-webinar-modal.jpg|Repeat Webinar. The summary it writes back is what the list view reads]]

**Webinar Cost** looks like a throwaway currency field. It is not: it is the denominator of the entire ROI panel on the completed record. A webinar saved with no cost reports no ROI.

**Co-Organizer** is not a picklist at all — it is **+ Add co-organisers**, which opens a panel. That is [section 4](#4-co-organisers).

### Registration Setup

**Registration Type** decides how much of this section exists. **With Registration** (default) means people sign up through a form and become registrants; **Without Registration** means anyone with the link joins, and the section collapses to who-can-join rules and a single thank-you email.

![[24-registration-setup.jpg|Registration Setup with registration on]]

**Registration Form** is the form registrants fill in. The dropdown lists the saved forms — Default Form, Real Estate Form, Stock Trading Form — each revealing a **Preview** tag on hover, plus **+ Create New Form** which opens the form builder.

![[25-registration-form-picker.jpg|Each row reveals Preview on hover; the last row creates a new form]]

![[26-registration-form-preview.jpg|The preview shows the form's fields read-only, with Edit in the header]]

> USECASE: Northline's outlook webinar is open to anyone, but their "Portfolio construction for business owners" session is not: they want to know the size of the portfolio before they take the call. That is a second registration form, not a second webinar product — which is why the form is a field on the webinar rather than a global setting.

**Customize Registration Page** is the field below it, and it is about the page rather than the form — see [The registration page](#5-the-registration-page).

**Moderation Type** — Automatic or Manual — is the field that decides whether a queue exists. Manual Moderation is what creates the approve/deny lists that show up on the record after the webinar as **Approved / Unapproved / Denied Registrants**.

**Push Webinar Registrants to CRM** is off by default. Turn it on and **Manage Configuration** appears, which is where the registrant-to-CRM mapping is set: which module a new registrant becomes, which layout, and what to do when the email already exists.

![[31-push-to-crm-config.jpg|Manage Configuration. This is the setting that removes the re-import step described in the introduction]]

The rest of the section is access control: country allow/deny, domain allow/deny, join-link-only-through-mail (on by default), authenticated-Zoho-users-only (off), a registration limit, and a post-registration redirect URL.

### Preferences, Reminders and Follow-Ups

Preferences are the in-session switches — questions, anonymous questions, showing questions to all, automatic session recording, video recording, the attendee list, emoji reactions, post-webinar redirection.

Reminders and Follow-Ups are the email schedule. The **1st Reminder** defaults to *15 mins before the webinar*; the 2nd and 3rd default to **None**, and their option lists are the same eleven intervals plus None — so a webinar can legitimately send one reminder, or three. Follow-ups default to *2 mins after the webinar ends* for both attendees and absentees, each with its own template slot and an **Include Recording** checkbox.

![[32-preferences-reminders.jpg|Preferences, Reminders and Follow-Ups all fit in one screenful of the form's scroll]]

Every template slot here works the same way: a **Select Template** button and, beside it, the currently chosen template as a link that previews it.

![[34-slot-select-template.jpg|A slot's Select Template dialog. The folder dropdown is a static "Zoho Webinar" label — every template it lists is a webinar template, so there is nothing to filter]]

### What blocks a save

**Webinar title** is the only hard requirement on the form. Saving without it outlines the field and shows *"Webinar title cannot be empty"* underneath it; the message clears as soon as you type.

![[37-save-validation.jpg|Save with no title. The message is inline, under the field]]

> OPEN: Nothing else is validated in the mock — not the date being in the past, not a registration limit of zero, not a cost that isn't a number, not an on-demand webinar saved with no video file. Which of those should block a save is undecided.

## 4. Co-organisers

A webinar can have more than one host, and the second host may be a CRM user, a Zoho Webinar user, or somebody who is in neither system yet. The field reflects that: it is not a picklist but an action.

![[15-coorg-field.jpg|The field reads + Add co-organisers until something is selected]]

Clicking it opens the **Add Co-organisers** panel:

![[16-coorg-panel-open.jpg|The panel. Source picklist, search, All / Selected tabs, the directory below, and the invite-by-email block at the foot]]

**The source picklist** chooses which directory you are looking at — **CRM users** or **Webinar users** — and the list below is grouped under that name.

![[17-coorg-panel-webinar-users.jpg|Switching the source switches the group heading and the people under it]]

**Search** filters the directory that is showing.

![[18-coorg-panel-search.jpg|Search narrows the list in place]]

**All / Selected (n)** are two views of the same panel. **Selected** lists everyone chosen across both directories together, because after picking from both you want one list to check rather than two tabs to flick between. Anyone invited by email appears under their own **Invited by email** group so they are not mistaken for a directory user.

![[19-coorg-panel-selected.jpg|Selected (3) — the tab label carries the count]]

**Invite by email address** is for the person who is in neither directory. There is no Invite button: each invitation is a row of **Email Address \*** and **Name \*** with **+** and **−** beside it. **+** inserts another row below and focuses it; **−** removes that row and is disabled on the only row, since there would be nothing left to type into.

![[20-coorg-invite-rows.jpg|Three invitation rows after two +. The − on a single row is disabled]]

Rows are read when **Done** is pressed, so there is no separate commit step to forget. A half-filled row keeps the panel open and says why — *"Enter a name for kate.williams@zylker.com."* A name is required rather than optional on purpose: a bare address is not recognisable in a list of co-organisers six weeks later.

**The same person can exist in both directories** — that is the ordinary case for anyone who runs webinars, and the mock's directories overlap on Rao Priya and Jayasuriya to make it reachable. Both copies are tickable; the clash is caught on **Done**, which keeps the panel open and shows *"Duplicate exists: rao.priya@northline.com has been added twice."* The same check covers a typed invitation whose address matches somebody already selected.

![[21-coorg-duplicate-error.jpg|One person picked from both directories. Done refuses until one of the two is removed]]

> NOTE: Identity inside the panel is the directory entry (`src|email`), which is what makes two copies of one person two separate selections rather than one silently de-duplicated row. Identity for the *duplicate check* is the email address alone. Both behaviours are deliberate and the pair is what produces the error above.

Once anything is selected, the field reads **Manage co-organisers** rather than the names, with the full list on its `title`.

![[22-coorg-manage-label.jpg|After Done. "Manage" rather than "Add", because there is now something to manage]]

Selection is stored on the field itself as hidden chips carrying name, email, source and whether the person was invited; the panel reads them on open and writes them on Done, which is what makes **Cancel** genuinely discard.

> OPEN: What a co-organiser can actually do is not modelled — whether they can edit the webinar, start it, see registrants, or appear on the registration page. And an invited co-organiser's email is never sent anywhere in the mock: there is no invitation email template for it.

## 5. The registration page

The registration **form** is the fields somebody fills in. The registration **page** is what that form is wrapped in — the branded page a registrant actually lands on from the link you publish. They are two different fields, one under the other.

**Customize Registration Page** is a picklist with two options, **Standard Template** (default) and **Custom Created**. Hovering either option reveals an **eye**, and the eye previews that page as a registrant sees it. It previews without selecting: the click is stopped before it reaches the option.

![[27-customize-reg-page-picklist.jpg|The eye appears on the hovered row. Clicking it previews; clicking the label selects]]

The preview is a full-screen render of the public page — the webinar title in the bar, a desktop/mobile toggle, the branded card, the session details and countdown on the left, the registration form on the right with the consent line and **Register**, and the footer.

![[28-reg-page-preview-standard.jpg|Standard Template. Note the title, date and time are the ones being set on the form, not sample text]]

The two layouts differ in the fields they carry:

| | Standard Template | Custom Created |
|---|---|---|
| First Name | required | required |
| Last Name | required | required |
| Email Address | required | required |
| Phone Number | — | required |
| Company | — | optional |
| Portfolio Size | — | optional |

![[29-reg-page-preview-custom.jpg|Custom Created adds the three extra fields]]

The toggle in the bar switches the same page to the mobile width, which stacks the two columns.

![[30-reg-page-preview-mobile.jpg|The mobile view of the same page]]

> OPEN: "Custom Created" is presented as a single option, but a customer will have more than one custom page. Whether this picklist should list saved page templates by name (the way Registration Form does), and where a custom page is authored, is undecided. The mock has no builder behind it.

> OPEN: The two fields overlap: the registration *form* already defines the fields, and the page preview shows a field set of its own. Which one wins when a Real Estate Form is selected alongside a Standard page needs deciding before this is built.

## 6. The webinar list

The module's list view is a CRM list like any other — view selector, column headers with sort, the standard toolbar.

![[38-webinar-list.jpg|The list. Webinar Category is the state, Webinar Type is the kind; the two are easy to confuse]]

| Column | What it holds |
|---|---|
| Webinar Name | Record name, links to the detail page |
| Webinar Category | The **state**: Scheduled Webinar, Completed Webinar, On-Demand Webinar |
| Webinar Date & Time | Start, with timezone |
| Registration Count | Registrations so far — populated before the webinar too |
| Attendance Count | Blank (`—`) until the webinar has run |
| Attend. Rate | Attendance ÷ registration, blank until completed |
| Webinar Duration | e.g. *1 hr 30 mins* |
| Organiser | Who runs it |
| Webinar Type | Live Webinar / On-Demand Webinar |

Two reading rules a developer needs:

- **Category and Type are different columns.** Category is the lifecycle state; Type is Live vs On-Demand. An on-demand webinar reads *On-Demand Webinar* in both, which is why they look redundant until you see a completed live one.
- **A repeating webinar is several rows**, one per occurrence, sharing a name and differing by date — *Recurrent Webinar* appears twice in the sample data with different dates and registration counts.

## 7. A webinar that hasn't happened yet

This is the record state you will spend the most time on, because it is where everything is collected.

![[39-detail-scheduled.jpg|A scheduled webinar with nothing in it yet. The status pill next to the title reads "Starts in 16 mins"]]

The header carries the actions: **Start Webinar**, **Send Invite**, **View Registration Link**, **Edit**, and an **Actions** menu. The left rail is the related-list index — Notes, Invited, Polls, Q&A, Recordings, Session Files, Open Activities, Closed Activities — and the counts on it are the fastest read of what the record holds.

Below the summary is the **Details** panel: everything set on the create form, in two columns, under **Webinar Details** and **Registration Details**.

![[40-detail-details-panel.jpg|The Details panel is the create form's answers, read-only]]

> NOTE: **Mock defect, do not copy.** The Details panel is hardcoded sample content — it reads *Test Webinar*, organiser *XYZ*, *Leads Form*, limit *1000* on every record, whichever row you opened. Populate it from the record.

### Send Invite

**Send Invite** is the flow that makes this integration worth building: it invites CRM records, from the modules the admin allowed in setup, without an export.

**Step 1 — pick the records.** A module dropdown, a view filter, a search box, the standard CRM filter sidebar, and the records with checkboxes. **Create Lead** sits top right for someone who isn't in CRM yet, and **Invite Additional Recipient Via Email: Add Email_ID** at the foot covers an address with no record at all.

![[41-send-invite-picker.jpg|Step 1. The module dropdown only offers what Who Can Participate From CRM allows]]

**Step 2 — confirm the list.** **Add** commits the ticked records and moves to a confirmation step that shows the breakdown by module, with **Remove ALL** and **Next**.

![[42-send-invite-confirm.jpg|Step 2. The module breakdown is how you catch having grabbed the wrong view]]

**Step 3 — Mass Email.** **Next** opens Mass Email: the recipient summary, the template, and the send option (immediately, or Schedule Later). The template is chosen through **Select Template**, with the current choice beside it as a link that previews it. A daily send counter — *"Emails sent today: 0 / 1000"* — sits in the footer.

![[43-mass-email.jpg|Mass Email. Note the To line collapses to "…& 94 more"]]

**Select Template here lists only invitation templates** — the Invitation-type rows from Setup ▸ Templates, nothing else, because every email this step can send is an invitation.

![[44-select-template.jpg|One row, because one invitation template exists. The second column is the folder, not the module]]

**Send** sends, and three things happen at once.

![[60-invite-sent-toast.jpg|"Invitation sent successfully — Recipients are listed under Invited below."]]

First, the toast. Second, the recipients appear under **Invited**, each with their module, invite status and when the invite was sent, and the strip above the table splits them into **Invited / Registered / Not Registered**.

![[45-invited-section.jpg|The Invited related list after a send. Everyone starts Not Registered]]

Third — and this is easy to miss — **an Email source-tracking link is created**. Before the first invite, **View Registration Link** holds the default link and nothing else, with source tracking off:

![[46-registration-link-empty.jpg|Before any invite: the default link, tracking off, no table]]

After the send, tracking is on and the table holds an **Email** row, created by the user who sent, with its own visited and registered counts:

![[47-registration-link-email-source.jpg|After the send. The channel CRM invites arrive through is now tracked like any other source]]

> NOTE: That is what makes "Registration by Source" on the completed record able to say *Email* at all. A source row is created once — sending a second batch does not add a second Email row.

### Re-inviting

Anyone in the Invited list who has not registered can be invited again, either per person or per module, from the same Mass Email screen (`isReInvite`). The difference is that the template starts empty rather than defaulting to the invitation template, so a second nudge is not silently identical to the first.

### Polls before the webinar

Polls are written in advance. **Create Poll** takes a question, a type and the options.

![[48-polls-pre.jpg|Create Poll. The poll is authored before the session and answered during it]]

**Q&A** exists as a related list but is empty with a line saying so: *"Q&A will be available after the webinar is completed."* Recordings and Session Files are likewise empty.

## 8. A webinar that has happened

Same record, same rail. What changes is that every empty panel now has content, and three panels appear that did not exist before. **Before the webinar the record collects; after the webinar it reports.**

![[49-completed-overview.jpg|A completed webinar. The pill by the title reads "— Completed"]]

| | Scheduled | Completed |
|---|---|---|
| Header actions | Start Webinar, Send Invite, View Registration Link | Edit, Actions (no Start, no Send Invite) |
| Registration & Attendance Summary | Registrations only | Registrations, attendees, absentees, and the module/source breakdowns |
| Attendees and Registrants List | — | Six tabs: All Attendees, All Absentees, All Registrants, Approved, Unapproved, Denied |
| Polls | Questions only | Questions with how the room answered |
| Q&A | "available after the webinar is completed" | Every question, who asked it, and the answer |
| Recordings / Session Files | Empty | The recording and whatever was shared |
| Webinar Revenue | Absent | ROI, pipeline, Deals Won, Deals in Pipeline |

### Registration and attendance

The summary band leads with three numbers — **Total Registration**, **Total Attendees**, **Total Absentees**, each with its percentage — then the breakdowns: attendance by module, attendance by source, registration by module, registration by source, and a daily registration trend with the peak day.

![[50-registration-summary.jpg|The three headline numbers, then the pies. Every chart has a Pie / Bar switch]]

![[51-registration-by-source.jpg|Registration by Source. This is the panel the Email source-tracking link feeds]]

### The people

**Attendees and Registrants List** is the panel a rep actually works from. Six tabs across the top with counts; the table gives name, email, the CRM module the person came from, their source, their poll count, whether they asked a question, when they registered and their **Webinar Status** — *Attended* or *Not Attended*.

![[52-attendees-list.jpg|One row per person. Module and Source are the two columns that make this a CRM screen rather than a webinar export]]

> USECASE: This is the "who do I call first" answer from the introduction. Jay sorts to *Attended*, filters to the module that matters, and the people who asked questions are marked in the Q&A column — a lead who sat through the hour and asked about minimum portfolio size is at the top of Monday's list, with their CRM history one click away.

> NOTE: **Mock defect.** The sample registrant rows carry sources LinkedIn / Twitter / Direct on a webinar whose only real source is Email, and the tab counts (13 attendees, 6 absentees, 14 registrants) do not reconcile with the 30 / 15 / 15 in the summary above, nor with the 11 rows the table paginates. Sample data, not behaviour to reproduce.

### Polls and Q&A

Polls now show the results per option. Q&A lists each question with who asked it, which module they came from, and the host's answer.

![[53-polls-completed.jpg|Polls with the room's answers]]

![[54-qa.jpg|Q&A. Every question is attached to the person who asked it, which is what makes it followable]]

> NOTE: **Mock content, not spec.** The Q&A transcript is written as software-pricing questions ("What does the Enterprise plan cost per seat?"), which contradicts the wealth-management example used elsewhere. The structure is the point: question, asker, module, answer.

### Webinar Revenue

The panel that justifies the integration to a sales leader. It is **collapsed by default** — click the band to open it.

![[55-revenue-roi.jpg|Webinar ROI, the pipeline split, Deals Won by source, and the Deals Won table]]

**Webinar ROI** is six figures: **Cost** (the Webinar Cost from the create form), **Revenue (Won)**, **ROI %**, **In Pipeline**, **Cost / Attendee**, **Revenue / Attendee**. Below it, **Pipeline by Stage** and **Deals Won by Source**, then **Deals Won** — deal name, amount, stage, account, contact — and a **Deals in Pipeline** table under it.

> NOTE: Cost is the only input a user provides; every other figure derives from it and from the attributed deals. A webinar saved with no Webinar Cost reports no ROI and no cost per attendee.

> OPEN: Which deals qualify as influenced, and over what window, is not modelled. The attribution model splits revenue across webinars, but what makes a deal eligible in the first place — the contact attended, or registered, or was merely invited — is undecided and it changes every number in this panel.

## 9. On-demand webinars

An on-demand webinar has no start time: a recording sits behind a registration form and people watch when they like. The form reflects that.

![[35-ondemand-form.jpg|On-demand. Video File replaces Webinar Duration, and Allow video play/pause sits between the file and the Organizer]]

What changes when **Webinar Type** is **OnDemand Webinar**:

- **Video File** replaces Webinar Duration — *From Zoho Webinar Recordings*, *Upload Files / Documents*, *Zoho WorkDrive*, *Other Cloud Services*.
- **Allow video play/pause** appears, on by default, positioned directly under Video File and above Organizer — the setting sits with the file it governs.
- **Repeat Webinar** and **Co-Organizer** are gone.
- **Reminders and Follow-Ups are gone.** There is no start time to remind anyone about.
- Registration Setup is otherwise identical, including Registration Form and Customize Registration Page.

**Without Registration** is the other branch of the same field, and it is worth seeing once: the whole registration block disappears and is replaced by join rules — **Who can Join** (Anyone can Join / Only Authenticated Users can Join), the country restriction, and one **Send thank you email to attendees** with its own template slot. There are no registrants on such a webinar, so there is nothing to confirm, remind or follow up in two directions.

![[36-without-registration.jpg|Without Registration. No form, no moderation, no reminders — one thank-you email]]

The completed on-demand record reports the same way as a completed live one, including revenue.

![[56-ondemand-completed.jpg|A completed on-demand webinar. Same reporting, no session-time concepts]]

> OPEN: **Send Invite on an on-demand webinar** is not settled. The header still offers it, and inviting people to watch a recording is reasonable — but the invitation template's calendar links and "starts in" content do not apply. Decide whether the invitation is a different email for this type.

## 10. The emails

### Where templates live

The webinar's default set lives in **Modules and Fields ▸ Zoho Webinar ▸ Preferences**, and Setup ▸ Templates lists them under the **Zoho Webinar** module.

![[57-templates-list.jpg|Setup ▸ Templates filtered to Zoho Webinar. Six rows named "Default" plus the invitation]]

The shipped set is eight lifecycle emails, and only one of them is editable in CRM:

| Row name | Subject | Type |
|---|---|---|
| Webinar Invitation Template | Sent when you invite CRM records to a webinar | Invitation |
| Default | `Registration Confirmation for ${Campaigns.Title}` | Confirmation |
| Default | `Reminder to join - ${Campaigns.Title}` | 1st Reminder |
| Default | `Reminder to join - ${Campaigns.Title}` | 2nd Reminder |
| Default | `Reminder to join - ${Campaigns.Title}` | 3rd Reminder |
| Default | `Thank you for attending ${Campaigns.Title}` | Attendees Follow-up |
| Default | `We missed you at ${Campaigns.Title}` | Absentees Follow-up |

The six **Default** rows are Zoho Webinar's own templates, listed here for visibility rather than owned by CRM: they are read-only in the list, with no pencil. Clicking one previews it, and **Edit** in that preview opens **Zoho Webinar's own editor in a new browser tab**, with its own `meeting.zoho.com` address bar, because the template belongs to the other product. Saving there hands the template back (`window.opener.zwSlotTemplateSaved`) and closes the tab.

![[65-template-preview-row.jpg|A Default row previewed. Edit leaves CRM]]

> NOTE: The **Webinar Cancelled** template is deliberately not in this list, and the invitation is the only row CRM edits in place. If you are adding a row here, the question to answer first is which product owns it.

### Creating one

**+ New Template** opens **Create Email Template**: **Select Module**, and — only when the module is Zoho Webinar — an **Email Type**. Next opens the gallery on that type.

![[66-create-email-template-dialog.jpg|Create Email Template. Email Type only appears for Zoho Webinar, because no other module's templates carry a lifecycle type]]

The gallery is the **Email Notifications** screen: a rail of the eight lifecycle emails on the left, and for the selected one its **Quick Templates** Default, any **Custom Templates** saved for it, and the six **Basic** layouts.

![[58-template-gallery.jpg|The gallery on Send Invite. The rail picks the use case, and the use case stamps the type]]

![[59-template-gallery-reminder.jpg|The same screen on Reminder 1. The standing paragraph under the title explains what the screen is for]]

Selecting a card makes that template the live one for the email, and **replaces the row** in the Templates list rather than adding a second — one row per lifecycle email, always. Picking a Basic layout opens the editor.

![[61-template-editor.jpg|The editor. Name and subject are real inputs, blank with placeholders, because nothing should be named for you]]

![[64-save-template.jpg|Save asks for the name and the folder. Both are required; saving without either is refused inline]]

### The type rules — the part to get right

A template's **type** decides what it may link to and what it must carry. These come straight out of `TPL_TYPE_LINKS` and `TPL_REQUIRED_LINK`; saving a template without its required link is refused.

| Type | May link to | Must contain |
|---|---|---|
| Webinar Invitation | Web URL, Email, Registration Link, all four Add To Calendar links | **Registration Link** |
| Confirmation Email | Web URL, Join URL, Cancel Registration, calendars | **Join URL** |
| 1st / 2nd / 3rd Reminder | Web URL, Join URL, Cancel Registration, calendars | **Join URL** |
| Attendees Follow-up | Web URL, Join URL, Recording Link, calendars | **Recording Link** |
| Absentees Follow-up | Web URL, Join URL, Recording Link, calendars | **Recording Link** |
| None | all of the above | nothing |

![[63-insert-link.jpg|Insert Link offers only the link types the template's own type allows]]

The reasoning is worth stating because it generalises: **an invitation goes to a CRM record** — someone who has not registered yet, so there is no registration to draw from, and the only useful link is the one that lets them register. **Every later email goes to a registrant**, so a per-person Join URL exists and a Registration Link would be meaningless.

### Merge fields

Typing `#` in the editor opens the merge-field picker. The sources it offers follow the same rule:

- **Webinar Invitation**: Webinar Details, Users, Organization.
- **Every later email**: **Registrations** as well, listed first — the registrant's own name, email, timezone, Join URL, Cancel Registration, Add To Calendar links, Handouts and the rest.

![[62-merge-fields.jpg|A confirmation template's picker. Registrations is present and selected by default]]

![[67-merge-field-modules.jpg|The source switcher. Registrations, Webinar Details, Users, Organization]]

> NOTE: **Known gap, pre-existing.** `tplMergeModules()` leads with Registrations for anything that is not a Webinar Invitation, including a plain Contacts template created from this screen — so a non-webinar template offers registrant fields rather than its own module's. It is out of scope for the webinar flows but it will look like a bug the first time somebody creates a Contacts template here.

## 11. Attribution

One person can attend three webinars before a deal closes. Without a rule, all three webinars report the whole deal and the year's webinar revenue reads three times what was actually sold. The attribution model is that rule, chosen once in setup and applied everywhere revenue appears.

> USECASE: A business owner attends Northline's March outlook webinar and does nothing, attends again in June and books a discovery call, then attends in September and signs — $12,000 of first-year fees. Three webinars, one deal. March found them, September closed them, June is the one that made them pick up the phone, and there is no true answer. Pick a rule or the totals are fiction.

The six models, with the copy the UI carries for each:

| Model | What it does | The A → B → C example on the card |
|---|---|---|
| First Webinar Interaction | 100% of the deal revenue to the earliest webinar attended | Attends A → B → C, deal closes: **A gets 100%** |
| Last Webinar Interaction | 100% to the most recent webinar attended | Attends A → B → C, deal closes: **C gets 100%** |
| **Linear** (default) | Splits revenue equally across every webinar attended | Attends A → B → C → D: **25% each** |
| Increasing Time Decay | Later webinars get more credit than earlier ones | Best when the last few touchpoints matter most |
| Decreasing Time Decay | Earlier webinars get more credit than later ones | Best when early awareness matters most |
| Position-Based | First and last get 40% each, the middle shares 20% | Best for U-shaped journeys |

Two facts to build against: attribution is **optional** — the step says so, and it can be enabled later from the enabled panel — and **changing the model recalculates every revenue figure in the product** against the new rule, rather than applying only to deals closed from then on.

> OPEN: Whether a model change is retroactive is stated as an assumption here, not observed. The mock does not recalculate anything. Confirm before building, because the alternative — freezing attribution per deal at close time — is a different data model.

## 12. Things we still need to decide

### Blocking

**Two template types require a link the product does not produce.** Attendees Follow-up and Absentees Follow-up must both carry a **Recording Link**, and saving without it is refused — but nothing in the flow guarantees a recording exists. *Automatic session recording* is a preference that can be switched off, and **Include Recording for Attendees / Absentees** are both **off by default** on the create form. So a webinar can legitimately be configured to send a follow-up that must contain a link to a recording that was never made. Decide which gives: the requirement, the default, or the link resolving to something graceful when there is no recording.

### Product

- **What a co-organiser can do** — edit, start, see registrants, appear on the registration page — and whether an invited co-organiser is emailed at all.
- **Custom registration pages**: whether the picklist lists saved page templates by name, where one is authored, and what happens when a custom page and a custom form disagree about the fields.
- **Send Invite on on-demand webinars**: keep it, and with which email?
- **Which deals count as influenced by a webinar**, and over what window. This decides every figure in Webinar Revenue.
- **Disconnecting the integration**: what happens to synced webinars, pushed registrants and attribution history.
- **Webinar Cancelled**: the template type exists, but nothing in the flows cancels a webinar or sends it.

### Engineering

- **Save validation** beyond the title: past dates, zero registration limits, non-numeric cost, on-demand with no video file.
- **Whether an attribution model change recalculates history** (see above).
- **Source rows are created once** — confirm the intended behaviour when invites are sent from two different modules, or on two different days.
- **Merge sources for non-webinar templates created from the gallery** (`tplMergeModules()` leads with Registrations regardless of module).
- **Daily mass-email limit**: the footer shows *0 / 1000*. Where that limit comes from, and what happens at it, is not modelled.

### Design

- The **Select Template** dialog is inconsistent: from a create-form slot the folder control is a static *Zoho Webinar* label, and from Send Invite it is an **All Templates** dropdown. Pick one.
- **Webinar Category vs Webinar Type** as two list columns reads as redundant on on-demand rows.
- The **eye** on Customize Registration Page appears only on hover, which is invisible to a keyboard or touch user.

### Assumptions this document makes

1. A webinar record is a CRM record in a real module, with layouts, sharing and field-level permissions behaving as CRM's do. The mock shows the chrome but does not model permissions.
2. Registrant → CRM record creation is the *Push Webinar Registrants to CRM* setting, and nothing else creates records.
3. The six **Default** rows in Setup ▸ Templates are Zoho Webinar's templates surfaced read-only, not copies owned by CRM.
4. Counts on the completed record (attendees, absentees, registrants) come from Zoho Webinar and are not recomputed in CRM.

### Mock defects — do not reproduce

- The **Details panel** on every webinar record shows the same hardcoded values (*Test Webinar*, *XYZ*, *Leads Form*, *1000*).
- The **registrant list's sources** include LinkedIn / Twitter / Direct on a webinar whose only source is Email, and the **tab counts do not reconcile** with the summary or the rows.
- **Webinar Duration** lists **1 hr twice** (the option list starts `1 hr, 1 hr, 2 hr…`).
- The **Q&A transcript** is SaaS-pricing content on a wealth-management example.
- Several stub `alert()` calls remain from earlier work (Visit Webinar module, Notify Suriya, Add Meeting, Search CRM users). They freeze the renderer until dismissed; do not wire real actions to them.

## 13. Appendix A — every field in the create form

Pulled from the DOM, in the order the form shows them, with the picklist values verbatim. Duplicate option values have been collapsed except where noted in the mock-defect list.

### Live webinar, With Registration (the default form)

This is the full form. `Webinar title` is the only required field.

| Field | Type | Required | Default | Options / notes |
|---|---|---|---|---|
| Webinar title | Text | **yes** | — | placeholder `Enter webinar title` |
| Webinar Type | Picklist | no | Live Webinar | Live Webinar, OnDemand Webinar |
| Webinar Date & Time | Picklist | no | 10:00 AM | 9:00 AM, 10:00 AM, 11:00 AM, 12:00 PM, 1:00 PM, 2:00 PM |
| Webinar Duration | Picklist | no | 1 hr | 1 hr, 2 hr, 3 hr, 4 hr, 5 hr, 6 hr, 7 hr, 8 hr, 9 hr, 10 hr, 11 hr, 12 hr, 13 hr, 14 hr, 15 hr, 16 hr, 17 hr, 18 hr, 19 hr, 20 hr, 21 hr, 22 hr, 23 hr, 24 hr, 00 min, 15 min, 30 min, 45 min |
| Webinar Timezone | Picklist | no | (-6) Central | (-5) Eastern, (-6) Central, (-7) Mountain, (-8) Pacific, (+0) UTC, (+5:30) IST |
| Webinar Owner | Picklist | no | Rao Priya | Rao Priya, Jay Acme, Mark Acme, Suriya |
| Organizer | Picklist | no | Jayasuriya | Jayasuriya, Morrison Troy |
| Repeat Webinar | Compound control | no | Repeat Webinar None ✎ | see the section above |
| Co-Organizer | Compound control | no | Co-Organizer + Add co-organisers | see the section above |
| Webinar Cost | Text | no | — | placeholder `0.00` |
| Description | Textarea | no | — |  |
| Registration Type | Picklist | no | With Registration | With Registration, Without Registration |
| Registration Form | Picklist | no | Default Form | Default FormPreview, Real Estate FormPreview, Stock Trading FormPreview, + Create New Form |
| Customize Registration Page | Picklist | no | Standard Template | Standard Template, Custom Created |
| Moderation Type | Picklist | no | Automatic Moderation | Automatic Moderation, Manual Moderation |
| Set Registration Limit | Text | no | — |  |
| Push Webinar Registrants to CRM | Checkbox | no | off |  |
| Allow/deny registrants from specific countries | Picklist | no | No Restrictions | No Restrictions, Allow registrants from Countries, Block registrants from Countries |
| Allow/Block Specific Domains | Picklist | no | No Restriction | No Restriction, Allow specific email domains, Block specific email domains |
| Post_Registration Custom Redirection | Text | no | — | placeholder `https://` |
| Allow access to join link only through mail | Checkbox | no | on |  |
| Allow only authenticated Zoho Users with a Zoho account | Checkbox | no | off |  |
| Send Confirmation to Registrants | Checkbox | no | on |  |
| Confirmation Email Template | Compound control | no | Confirmation Email Template Select TemplateWebinar Confirmat | see the section above |
| 1st Reminder | Picklist | no | 15 mins before the webinar | 2 mins before the webinar, 5 mins before the webinar, 10 mins before the webinar, 15 mins before the webinar, 30 mins before the webinar, 1 hour before the webinar, 2 hours before the webinar, 6 hours before the webinar, 12 hours before the webinar, 1 day before the webinar, 1 week before the webinar |
| 1st Reminder Template | Compound control | no | 1st Reminder Template Select Template1st Reminder Template | see the section above |
| 2nd Reminder | Picklist | no | None | None, 2 mins before the webinar, 5 mins before the webinar, 10 mins before the webinar, 15 mins before the webinar, 30 mins before the webinar, 1 hour before the webinar, 2 hours before the webinar, 6 hours before the webinar, 12 hours before the webinar, 1 day before the webinar, 1 week before the webinar |
| 3rd Reminder | Picklist | no | None | None, 2 mins before the webinar, 5 mins before the webinar, 10 mins before the webinar, 15 mins before the webinar, 30 mins before the webinar, 1 hour before the webinar, 2 hours before the webinar, 6 hours before the webinar, 12 hours before the webinar, 1 day before the webinar, 1 week before the webinar |
| Send Follow-up Email to Attendees | Picklist | no | 2 mins after the webinar ends | None, 2 mins after the webinar ends, 5 mins after the webinar ends, 10 mins after the webinar ends, 15 mins after the webinar ends, 1 hour after the webinar ends, 2 hours after the webinar ends, 6 hours after the webinar ends, 1 day after the webinar ends |
| Send Follow-up Email to Absentees | Picklist | no | 2 mins after the webinar ends | None, 2 mins after the webinar ends, 5 mins after the webinar ends, 10 mins after the webinar ends, 15 mins after the webinar ends, 1 hour after the webinar ends, 2 hours after the webinar ends, 6 hours after the webinar ends, 1 day after the webinar ends |
| Attendees Follow-up Template | Compound control | no | Attendees Follow-up Template Select TemplateAttendees Follow | see the section above |
| Absentees Follow-up Template | Compound control | no | Absentees Follow-up Template Select TemplateAbsentees Follow | see the section above |
| Include Recording for Attendees | Checkbox | no | off |  |
| Include Recording for Absentees | Checkbox | no | off |  |

### On-demand webinar

Differences from the list above are described in [On-demand webinars](#9-on-demand-webinars). Note the Webinar Type default below reads *Live Webinar* because the state was set programmatically for the capture; through the UI the button reads *OnDemand Webinar*.

| Field | Type | Required | Default | Options / notes |
|---|---|---|---|---|
| Webinar title | Text | **yes** | Lead Webinar | placeholder `Enter webinar title` |
| Webinar Type | Picklist | no | Live Webinar | Live Webinar, OnDemand Webinar |
| Webinar Date & Time | Picklist | no | 10:00 AM | 9:00 AM, 10:00 AM, 11:00 AM, 12:00 PM, 1:00 PM, 2:00 PM |
| Video File | Picklist | no | Choose File | From Zoho Webinar Recordings, Upload Files / Documents, Zoho WorkDrive, Other Cloud Services |
| Webinar Timezone | Picklist | no | (-6) Central | (-5) Eastern, (-6) Central, (-7) Mountain, (-8) Pacific, (+0) UTC, (+5:30) IST |
| Allow video play/pause | Checkbox | no | on |  |
| Webinar Owner | Picklist | no | Rao Priya | Rao Priya, Jay Acme, Mark Acme, Suriya |
| Organizer | Picklist | no | Jayasuriya | Jayasuriya, Morrison Troy |
| Webinar Cost | Text | no | — | placeholder `0.00` |
| Description | Textarea | no | — |  |
| Registration Type | Picklist | no | With Registration | With Registration, Without Registration |
| Registration Form | Picklist | no | Default Form | Default FormPreview, Real Estate FormPreview, Stock Trading FormPreview, + Create New Form |
| Customize Registration Page | Picklist | no | Standard Template | Standard Template, Custom Created |
| Moderation Type | Picklist | no | Automatic Moderation | Automatic Moderation, Manual Moderation |
| Set Registration Limit | Text | no | — |  |
| Push Webinar Registrants to CRM | Checkbox | no | off |  |
| Allow/deny registrants from specific countries | Picklist | no | No Restrictions | No Restrictions, Allow registrants from Countries, Block registrants from Countries |
| Allow/Block Specific Domains | Picklist | no | No Restriction | No Restriction, Allow specific email domains, Block specific email domains |
| Post_Registration Custom Redirection | Text | no | — | placeholder `https://` |
| Allow access to join link only through mail | Checkbox | no | on |  |
| Allow only authenticated Zoho Users with a Zoho account | Checkbox | no | off |  |
| Send Confirmation to Registrants | Checkbox | no | on |  |
| Confirmation Email Template | Compound control | no | Confirmation Email Template Select TemplateWebinar Confirmat | see the section above |

### Without Registration

Registration Setup collapses to access rules and a single thank-you email.

| Field | Type | Required | Default | Options / notes |
|---|---|---|---|---|
| Webinar title | Text | **yes** | — | placeholder `Enter webinar title` |
| Webinar Type | Picklist | no | Live Webinar | Live Webinar, OnDemand Webinar |
| Webinar Date & Time | Picklist | no | 10:00 AM | 9:00 AM, 10:00 AM, 11:00 AM, 12:00 PM, 1:00 PM, 2:00 PM |
| Webinar Duration | Picklist | no | 1 hr | 1 hr, 2 hr, 3 hr, 4 hr, 5 hr, 6 hr, 7 hr, 8 hr, 9 hr, 10 hr, 11 hr, 12 hr, 13 hr, 14 hr, 15 hr, 16 hr, 17 hr, 18 hr, 19 hr, 20 hr, 21 hr, 22 hr, 23 hr, 24 hr, 00 min, 15 min, 30 min, 45 min |
| Webinar Timezone | Picklist | no | (-6) Central | (-5) Eastern, (-6) Central, (-7) Mountain, (-8) Pacific, (+0) UTC, (+5:30) IST |
| Webinar Owner | Picklist | no | Rao Priya | Rao Priya, Jay Acme, Mark Acme, Suriya |
| Organizer | Picklist | no | Jayasuriya | Jayasuriya, Morrison Troy |
| Repeat Webinar | Compound control | no | Repeat Webinar None ✎ | see the section above |
| Co-Organizer | Compound control | no | Co-Organizer + Add co-organisers | see the section above |
| Webinar Cost | Text | no | — | placeholder `0.00` |
| Description | Textarea | no | — |  |
| Registration Type | Picklist | no | With Registration | With Registration, Without Registration |
| Allow only authenticated Zoho Users with a Zoho account | Checkbox | no | on |  |
| Who can Join | Picklist | no | Anyone can Join | Anyone can Join, Only Authenticated Users can Join |
| Allow/deny registrants from specific countries | Picklist | no | None | None, Allow registrants from Countries, Block registrants from Countries |
| Send thank you email to attendees | Picklist | no | 2 minutes after webinar ends | 2 minutes after webinar ends, 5 mins after webinar ends, 10 mins after webinar ends |
| Thank You Email Template | Compound control | no | Thank You Email Template Select TemplateAttendees Follow-up  | see the section above |

## 14. Appendix B — integration settings, templates and directories

### Integration setup (the four-step wizard)

| Step | Field | Type | Default | Options / notes |
|---|---|---|---|---|
| 1 | Email | Text | `jonamsuriya@gmail.com` (mock) | The Zoho account being connected |
| 1 | Organisation | Picklist | Acme Corp Webinars | Acme Corp Webinars, ClientCo Marketing, Consulting Practice. Rule shown under the field: *"Only one organisation can be connected to CRM at a time."* |
| 2 | Sync past webinars? | Radio | **Yes** | Yes / No. Backed by a hidden input `setup-sync-past-select` holding `yes`/`no` |
| 3 | Who Can Participate From CRM | Checkbox list + search | Leads, Contacts (locked on) | Leads\*, Contacts\*, Vendors, Donors, Volunteers, Members, Students, Alumni, Partners, Speakers, Referrals, Patients, Subscribers |
| 4 | Enable Deal Revenue Attribution | Toggle | on | Turning it off hides the model cards |
| 4 | Revenue Attribution Type | Cards (single select) | **Linear** | First Webinar Interaction, Last Webinar Interaction, Linear, Increasing Time Decay, Decreasing Time Decay, Position-Based |

Footer buttons per step: **Cancel** + **Next** on steps 1–3, **Cancel** + **Enable Integration** on step 4.

> NOTE: `INVITE_MODULES` — the list Send Invite's dropdown draws from — is `["Leads","Contacts","Vendors","Custom Module 1"]`, and it is intersected with the participating list. So *Custom Module 1* can never be switched on from step 3 (it is not in `IM_MODULES`), and the Send Invite dropdown offers Leads and Contacts until Vendors is ticked. Two lists that have to agree is the kind of thing that rots; consider one source.

### Template types and keys

| Use case key | Rail label | Default template name | Email Type in the list |
|---|---|---|---|
| `sendInvite` | Send Invite | Send Invite Template | Invitation |
| `confirmation` | Registration Confirmation | Webinar Confirmation Template | Confirmation |
| `reminder1` | Reminder 1 | 1st Reminder Template | 1st Reminder |
| `reminder2` | Reminder 2 | 2nd Reminder Template | 2nd Reminder |
| `reminder3` | Reminder 3 | 3rd Reminder Template | 3rd Reminder |
| `attendeesFollowup` | Attendees Follow-up | Attendees Follow-up Template | Attendees Follow-up |
| `absenteesFollowup` | Absentees Follow-up | Absentees Follow-up Template | Absentees Follow-up |
| `cancellation` | Webinar Cancelled | Webinar Cancelled Template | Webinar Cancelled |

### Merge sources, verbatim

**Webinar Details** — Webinar Title, Webinar Date & Time, Webinar Organiser, Webinar Duration, Description.

**Registrations** — Registration Id, Country, Created By, Created Time, Email, First Name, Modified By, Timezone, Add To Google Calendar, Add To Yahoo Calendar, Add To Outlook Calendar, Add To Zoho Calendar, Add To Calendar, Join URL, Handouts, Cancel Registration, Audio Details, Registration URL, Full Name, Last Name, Abuse Email, iOS app URL.

**Leads** — Lead Id, Lead Owner, Company, First Name, Last Name, Title, Email, Phone, Mobile, Lead Source, Industry, City, State, Country.

**Contacts** — Contact Id, Contact Owner, Account Name, First Name, Last Name, Title, Email, Phone, Mobile, Department, Mailing City, Mailing State, Mailing Country.

Plus **Users** and **Organization** on every type.

### Link types a template can insert

Web URL, Email, Registration Link, Join URL, Cancel Registration, Recording Link, Add To Calendar, Add To Google Calendar, Add To Yahoo Calendar, Add To Outlook Calendar, Add To Zoho Calendar — filtered per type by the table in [The emails](#10-the-emails).

### Co-organiser directories (mock data)

| Source | People |
|---|---|
| CRM users | Rao Priya, Mann Michael, Jayasuriya, Morrison Troy |
| Webinar users | Rao Priya, Jayasuriya, Luxe Martin, Suriya, Mark Acme |

Rao Priya and Jayasuriya appear in both on purpose — that is what makes the duplicate error reachable.

### Registration page field sets

| | Standard Template | Custom Created |
|---|---|---|
| Fields | First Name\*, Last Name\*, Email Address\* | First Name\*, Last Name\*, Email Address\*, Phone Number\*, Company, Portfolio Size |

### Where each flow starts, for testing

| Flow | Entry |
|---|---|
| Marketplace card | `openSettingsModal(); integOpenZoho()` |
| Integration intro / setup / enabled panel | `integShowPanel('integ-intro-panel' / 'integ-setup-panel' / 'integ-enabled-panel')`, then `setupStep(n)` |
| Create form | `goToForm()` |
| Webinar list | `goToList()` |
| A webinar record | `openWebinarDetail(record, isCompleted, hasInvited)` |
| Setup ▸ Templates | `openSettingsModal(); openTemplatesPage(); tplPagePickModule('Zoho Webinar')` |
| Template gallery | `openUsecaseGallery('<use case key>')` |
| Add Co-organisers panel | `coOrgOpen(document.querySelector('#coOrgGroup .coorg-add'))` |
| Registration page preview | `rpPreview(event, 'standard' \| 'custom')` |

The screenshots in this document were captured with `docs/prd/master/shoot.mjs` against `http://localhost:8090/webinar.html`; `shots.json` holds the click path for every figure, so any screen here can be reproduced exactly.
