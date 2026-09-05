# Zoho Webinar ⇌ Zoho CRM Integration — PRD

Source of truth: `webinar.html`, walked at `http://localhost:8090/webinar.html`.
Every statement below traces to something observed in that mock. Where the mock is silent,
the item appears in *Open questions and assumptions* rather than in the body.

**Figure convention.** Lines in the form *Figure N — caption* are **placeholders for screenshots that
still have to be inserted in Writer**. The image for each one is `docs/prd/zoho-webinar/screens/`, file
named in Appendix A. Insert each at its placeholder with `Insert > Image`, then caption it with
`Insert > References > Captions` (object type *Figure*) so the numbers renumber themselves.

## Index

1. **Why CRM–Webinar integration** — orientation for a developer who has never used Zoho Webinar.
   - What Zoho Webinar is
   - Who uses it and for what
   - What Zoho Webinar lacks on its own
   - How CRM solves it
   - Where it shows up inside CRM
2. **Integration** — the settings surface, in the order a user meets it.
   - Where it lives and who sets it up
   - Introduction page, before enabling
   - Account states the mock models (Cases 1–5)
   - Setup page: connection details
   - Zoho Webinar Invite Modules
   - Webinar Deal Attribution
   - Enabled state, re-configuration and the Save bar
3. **Create webinar** — the most implementation-heavy flow.
   - Entry points and page chrome
   - Webinar Details
   - Registration Setup
   - Preferences
   - Reminders
   - Follow-Ups
   - Validation and save behaviour
4. **Scheduled webinar — live**
   - List page
   - Detail page
   - Registration Link and source tracking
   - Send Invite flow
   - Registrants and attendance
5. **Scheduled webinar — on demand** — what differs.
6. **Completed webinar** — what differs.
7. **Completed webinar — on demand** — what differs.
8. **Supporting flows**
   - Email templates: where they live, and the two lists
   - Create Email Template → Gallery → editor → Save
   - Template type → allowed links → required link
   - Merge fields
   - Registration forms and push-to-CRM
9. **Appendices** — screen inventory, field reference, open questions and assumptions.

---

# 1. Why CRM–Webinar integration

## 1.1 What Zoho Webinar is

Zoho Webinar is Zoho's webinar product: you schedule a session (title, date/time, duration,
organiser), publish a registration form, people sign up, they attend or they don't, and the
product emails them along the way — invitation, confirmation, reminders, follow-ups. It also
captures what happened in the room: polls, Q&A, recordings and session files.

In this integration it is delivered through the **Zoho Meetings** marketplace listing, which
covers two products from one login: *For webinars* and *For online meetings* (Figure 46).
This PRD covers the webinar half only.

## 1.2 Who uses it and for what

The mock models one persona: **a sales rep who is also the CRM admin for this integration**.
The demonstration data implies the kinds of teams the product is aimed at:

- **Demand-generation teams** running product webinars to build pipeline — the mock's
  *Product Reveal Webinar*, with 318 registrations, 241 attendees and a revenue panel tying
  the session to closed deals.
- **Vertical sales teams** running topic sessions for a named segment — the mock's
  *Real Estate Webinar*, with a Real Estate registration form.
- **Teams running series or recurring sessions** — two *Recurrent Webinar* occurrences appear
  in the list with a repeat marker.
- **Teams publishing evergreen content** — the mock's *On Demand Webinar*, watched after the
  fact rather than live.

## 1.3 What Zoho Webinar lacks on its own

Read off what the integration adds, the gaps it is closing are:

- Registrants live in the webinar product, not in the CRM, so the rep works from an exported
  list that is stale the moment it is exported. The intro page states the intent plainly:
  *"Recipients come straight from CRM, so the invite always goes to current data."*
- Nothing connects attendance to pipeline. Whether a webinar produced revenue is a manual
  reconciliation.
- Invites go to a list the rep maintains, not to the Leads, Contacts or custom-module records
  they already work with.
- Follow-up is decoupled from the CRM record, so who attended and who missed it is not visible
  where the rep works.

## 1.4 How CRM solves it

The introduction page states the integration's own four-step claim (Figure 47):

| # | Step | What it means |
|---|---|---|
| 1 | Create the webinar in CRM | Scheduled from the Zoho Webinar module, with its registration form and lifecycle emails |
| 2 | Invite your records | Recipients picked from the modules the admin allows — Leads, Contacts or a custom module |
| 3 | Registrants come back | Registrations, joins and no-shows land on the webinar, and can be pushed into CRM as records |
| 4 | See the revenue | Attendance is tied to the deals it influenced, using the chosen attribution model |

And the four reasons it gives for enabling: no exporting lists · attendance on the record ·
emails handled for you · proof it worked.

## 1.5 Where it shows up inside CRM

| Surface | Path | What it is |
|---|---|---|
| Zoho Webinar module | Left nav ▸ Zoho Webinar | A CRM module: list views, records, filters, Create Webinar |
| Integration settings | Setup ▸ Marketplace ▸ Zoho ▸ Zoho Meetings ▸ For webinars | Introduction, setup and enabled states |
| Module configuration | Setup ▸ Customization ▸ Modules and Fields ▸ Zoho Webinar | Layouts, Fields, Buttons, **Preferences** (the lifecycle emails), **Registration Form**, Summary |
| Templates | Setup ▸ Customization ▸ Templates ▸ Email, module filter *Zoho Webinar* | The webinar template set |

---

# 2. Integration

## 2.1 Where it lives and who sets it up

**Path:** Settings (gear) → Setup Home → **Marketplace ▸ Zoho** → the **Zoho Meetings** card →
**For webinars** → *Set up* (`mpSetupWebinar()`).

The Zoho Meetings card carries two independent halves and says so:
*"One Zoho Meetings login connects both. Set up one or both independently."*

| Half | Blurb on the card | Action |
|---|---|---|
| For webinars | Sync registrants, track attendance, convert attendees to leads. | Set up |
| For online meetings | Instant & scheduled meetings, audio/video & screen sharing, recording and management. | Set up |

*Figure 46 — Marketplace ▸ Zoho, the Zoho Meetings card and its two halves.*

The page carries a **DEMO** case switcher (`#case-switcher`) at top right. It is a mock affordance
for demonstrating account states, not a product control — see §2.3.

## 2.2 Introduction page, before enabling

*Set up* opens the introduction panel (`#integ-intro-panel`), **not** the setup form. Header:
**Zoho Webinar Integration** with a **NOT ENABLED** pill, and **Enable Integration** at top right.

Sections, in order:

1. **Hero** — a two-way CRM ⇌ Webinar graphic and the line *"Run your webinars from inside CRM"*,
   with the sub-line *"Invite the records you already work with, let registrations and attendance
   flow back onto the webinar, and see which webinars actually closed deals — without exporting a
   single list."*
2. **How it works** — the four numbered cards in §1.4.
3. **Why teams enable it** — four cards: No exporting lists · Attendance on the record ·
   Emails handled for you · Proof it worked.
4. **When you enable, this integration will** — four ticked commitments:
   - Connect your Zoho Webinar organisation to this CRM account.
   - Add a Zoho Webinar module, with its registrants, attendance and recordings.
   - Let you choose which modules a webinar invite can be sent to.
   - Optionally sync your past webinars, and attribute deal revenue to them.

*Figure 47 — Introduction page, NOT ENABLED. Figure 48 — the "When you enable" commitments.*

**Behaviour to build:** the introduction page renders the same in every account state. The account
state is evaluated only when **Enable Integration** is pressed.

## 2.3 Account states the mock models (Cases 1–5)

Five states, selected in the mock through the DEMO switcher. In production these are the outcomes
of looking up the signed-in user's Zoho Webinar account.

| Case | Switcher label | What Enable Integration produces | Actions offered |
|---|---|---|---|
| 1 | No account | *Select Organization* dialog reporting no account found under the email (`#integ-case1-modal`) | Per Figure 11 |
| 2 | Single org | Straight to the setup page with the single organisation pre-filled | Enable Integration |
| 3 | Multiple orgs | Setup page with an **Organisation** dropdown to pick from (`#integ-setup-panel`) | Enable Integration |
| 4 | Not an admin | **Insufficient Permission in Webinar** dialog (`#integ-case4-modal`) | Cancel · **Notify Super Admin** |
| 5 | Trial expired | **Trial Expired** dialog (`#integ-case5-modal`) | Close (×) only — no action button |

**Case 4 — Insufficient Permission in Webinar** (Figure 53). Shows Email and **Role: Member**, then:
*"A Zoho Webinar account was found under this email, but you're a **Member** of the organisation —
not an Admin. Only Webinar Admins can connect the organisation to Zoho CRM."* Followed by
*"What to do next: Ask your Webinar Super Admin (Suriya) to either complete this setup on your
behalf, or promote your account to Admin so you can complete it yourself."*
The Super Admin's name is rendered into the copy, so the build needs it from the lookup.

**Case 5 — Trial Expired** (Figure 54). Shows Email and **Status: Trial expired**, then:
*"Your Zoho Webinar trial ended on **June 28, 2026**. Upgrade to a paid plan to reconnect this
account and resume syncing data with Zoho CRM."* Then *"What to do next: Renew or upgrade your Zoho
Webinar subscription, then come back here to complete the integration."*
The expiry date is rendered into the copy. **This dialog is a dead end in the mock** — no upgrade
link, only the × — see open questions.

## 2.4 Setup page: connection details

Header: **Zoho Meetings Integration for Webinar**, with a sub-line that varies by case. In Case 3 it
reads *"You're an admin in multiple Webinar organisations. Pick the one to connect to Zoho CRM."*

| Field | Type | Mandatory | Default | Options / range | Visibility & dependency | Validation | Notes for the developer |
|---|---|---|---|---|---|---|---|
| Email | Read-only text | — | Signed-in user's Zoho Webinar email (`jonamsuriya@gmail.com` in the mock) | — | Always | — | Not editable; identifies the account being connected |
| Organisation | Dropdown | Yes | First organisation (`Acme Corp Webinars`) | Acme Corp Webinars, ClientCo Marketing, Consulting Practice | Always; a chooser only when the user is admin in more than one org | — | Helper text: *"Only one organisation can be connected to CRM at a time."* |
| Sync past webinars? | Dropdown | Yes | **Yes** | Yes, No | Always | — | Decides whether historical webinars are imported as records; the intro page calls this optional |

*Figure 49 — Setup page under Case 3, with the Organisation chooser.*

## 2.5 Zoho Webinar Invite Modules

**Why it exists:** it decides which CRM modules a webinar invite may be sent to, and it directly
drives the module dropdown in Send Invite (§4.4). Turn a module off here and it disappears there.

Sub-heading: *"Choose the modules from which records can be invited to a webinar."*

Controls:

- **Select all** / **Clear** links, top right of the section.
- A **chip row** showing the current selection, each chip removable with ×, prefixed by a count
  (`3 selected:`).
- A **Search modules** box.
- A grouped checkbox list, in two groups:

| Group | Modules offered (UI order) |
|---|---|
| STANDARD | Leads, Contacts, Accounts, Potentials, Vendors, Cases, Campaigns, Meetings |
| CUSTOM | Custom Module 1, Donor Management, Donations, Volunteers, Nonprofits Campaigns, Community Budgets, Customer Visits, Referral, AI Creative Module, Org test, Untitless, AjB |

**Default selection:** Leads, Contacts, Custom Module 1 (3 selected).

**Eligibility rule, stated in the UI:** *"Modules without an email field can't receive invites and
aren't listed."* The list is therefore filtered server-side by the presence of an email field.

*Figure 12 — Invite Modules in the setup page. Figure 51 — the same picker in the enabled state.*

## 2.6 Webinar Deal Attribution

Section copy: *"Webinar Deal Attribution tells you which webinars actually helped close your deals.
It connects your webinar attendees to the CRM deals they influenced and shows how much revenue each
webinar contributed."*

| Field | Type | Mandatory | Default | Options / range | Visibility & dependency | Validation | Notes for the developer |
|---|---|---|---|---|---|---|---|
| Enable Deal Revenue Attribution | Toggle | — | **On** | On / Off | Always | — | Off hides the model chooser |
| Choose the Revenue Attribution Type | Card radio group | Yes when the toggle is on | **Linear** | Six models, below | Only while the toggle is on | — | Selected card gets a green tick and a coloured border; each card has an info (ⓘ) affordance and a small bar-chart illustration of the split |

The six models, verbatim with their descriptions:

| Model | Description in the UI |
|---|---|
| First Webinar Interaction | Attributes 100% of the deal revenue to the earliest webinar attended. |
| Last Webinar Interaction | Attributes 100% of the deal revenue to the most recent webinar attended. |
| **Linear** (default) | Distributes the deal revenue equally across all webinars attended. |
| Increasing Time Decay | Assigns more credit to earlier webinars and gradually less to later ones. |
| Decreasing Time Decay | Assigns more credit to the most recent webinars and gradually less to earlier ones. |
| Position-Based | Gives 40% to first, 40% to last, 20% split across in-between webinars. |

*Figure 50 — Deal Attribution with Linear pre-selected.*

The chosen model is what the record-level **Webinar Revenue** panel reports against (§6.3).

## 2.7 Enabled state, re-configuration and the Save bar

Pressing **Enable Integration** at the foot of the setup page:

1. Shows a success toast: **"Integration was enabled successfully"** with a **Visit Webinar module**
   link.
2. Swaps the panel for the enabled panel (`#integ-enabled-panel`).

What changes in the enabled state (Figure 51):

| Element | Not enabled | Enabled |
|---|---|---|
| Status pill | NOT ENABLED | **ACTIVE** |
| Top-right actions | Enable Integration | **Deactivate** · **Help** |
| Email / Organisation | Editable dropdown (org) | Read-only fields |
| Sync past webinars? | Present | **Not shown** |
| Invite Modules | Editable | Editable |
| Deal Attribution | Editable | Editable |
| Footer | Enable Integration button | Dirty-state Save bar |

**Save bar behaviour:** it is absent until something changes. Changing any control — ticking a module,
for instance — pins a bar to the bottom of the panel reading **"● You have unsaved changes"** with
**Cancel** and **Save** (Figure 52). Ticking *Accounts* moved the chip row to `4 selected:` and added
an *Accounts ×* chip immediately, so the chip row tracks the pending state rather than the saved one.

---

# 3. Create webinar

## 3.1 Entry points and page chrome

**Entry point:** Zoho Webinar module list ▸ **Create Webinar** (primary button, top right).

The form is a full-page CRM create form, not a modal. Chrome:

| Element | Position | Behaviour |
|---|---|---|
| **Create Webinar** title | Top left | — |
| **Standard ▾** | Beside the title | Layout switcher |
| **Edit Page Layout** | Beside the switcher | Link to layout editor |
| **Cancel** | Top right | Leaves the form |
| **Save & New** | Top right | Save and open a fresh form |
| **Save** | Top right, primary | Save and leave |

Five sections in order: **Webinar Details** → **Registration Setup** → **Preferences** →
**Reminders** → **Follow-Ups**.

*Figure 55 — Webinar Details and Registration Setup. Figure 56 — Preferences, Reminders and Follow-Ups.*

## 3.2 Webinar Details

| Field | Type | Mandatory | Default | Options / range | Visibility & dependency | Validation | Notes for the developer |
|---|---|---|---|---|---|---|---|
| Webinar title | Single-line text | **Yes** (red asterisk) | Empty | — | Always | Blocks save when empty; inline error **"Webinar title cannot be empty"** | Placeholder *Enter webinar title*; becomes the record name |
| Webinar Type | Picklist | No | **Live Webinar** | Live Webinar, OnDemand Webinar | Always | — | Drives which record state the saved webinar lands in (§5) |
| Webinar Date & Time | Compound: date input + time picklist + timezone picklist | No | Today's date · **10:00 AM** · **(-6) Central** | Time: 9:00 AM, 10:00 AM, 11:00 AM, 12:00 PM, 1:00 PM, 2:00 PM · Timezone: (-5) Eastern, (-6) Central, (-7) Mountain, (-8) Pacific, (+0) UTC, (+5:30) IST | Always | — | Three controls, not one. The date is a native date input; the timezone sits on its own row below |
| Webinar Duration | Two picklists: hours + minutes | No | **1 hr** · **00 min** | Hours 1–24 hr · Minutes 00, 15, 30, 45 min | Always | — | Two separate controls |
| Webinar Owner | Picklist + lookup button | No | **Rao Priya** | Rao Priya, Jay Acme, Mark Acme, Suriya | Always | — | The trailing icon opens a user lookup |
| Organizer | Picklist | No | **Jayasuriya** | Jayasuriya, Morrison Troy | Always | — | Distinct from Webinar Owner: owner is the CRM record owner, organiser is the webinar host |
| Co-Organizer | Picklist | No | **None** | None, Jayasuriya, Morrison Troy | Always | — | Record detail pages show multiple co-organisers, so treat as multi-select in the data model |
| Repeat Webinar | Button (`None`) + edit (✎) icon | No | **None** | Set through the Repeat dialog | Always | — | Opens `#repeatModal` (`openRepeatModal()`); a repeat schedule is what produces the *Recurrent Webinar* records in the list |
| Webinar Cost | Text with `$` prefix and info icon | No | Empty | — | Always | — | Placeholder *0.00*; feeds **Cost**, **Cost / Attendee** and **ROI** in the Webinar Revenue panel (§6.3) |
| Description | Multi-line text | No | Empty | — | Always | — | — |

**Repeat dialog (`#repeatModal`).** Reached from the ✎ beside Repeat Webinar. Its own controls
(frequency None/Daily/Weekly/Monthly/Yearly/Custom, an interval 1–7, a unit days/weeks/months, an
ordinal first/second/third/fourth/last, a weekday, a start time and a duration) are the source of the
recurrence. **Note:** an earlier parse of the markup mis-attributed these options to the *Absentees
Follow-up Template* field; they belong to this dialog.

When Repeat is set, two further fields appear in the mock's markup and are documented as
recurrence-only:

| Field | Type | Default | Options |
|---|---|---|---|
| Registration Mode | Picklist | Register and attend each event individually | Register and attend each event individually · Register once and attend any event |
| Open Registration for | Picklist | All Webinars | All Webinars · Only selected number of occurrences (then 1–6 occurrences) |

## 3.3 Registration Setup

| Field | Type | Mandatory | Default | Options / range | Visibility & dependency | Validation | Notes for the developer |
|---|---|---|---|---|---|---|---|
| Registration Type | Picklist | No | **With Registration** | With Registration, Without Registration | Always | — | *Without Registration* is what removes the registration form and the confirmation email from the lifecycle |
| Registration Form | Picklist | No | **Default Form** | Default Form, Real Estate Form, Stock Trading Form (each with a *Preview* affordance), **+ Create New Form** | Only with *With Registration* | — | *+ Create New Form* opens the form builder (`#formBuilderModal`); Preview opens `#rfPreviewOverlay` |
| Moderation Type | Picklist | No | **Automatic Moderation** | Automatic Moderation, Manual Moderation | Only with *With Registration* | — | *Manual Moderation* is what produces the Approved / Unapproved / Denied registrant queues and the **Waiting for Approval** tile (§4.2) |
| Set Registration Limit | Text (number) | No | Empty | — | Only with *With Registration* | — | Empty means no cap. When set, the detail page shows *n / limit* and *"n seats left"* |
| Push Webinar Registrants to CRM | Checkbox | No | **Off** | On / Off | Always | — | Labelled *Push to CRM* on the record and in the list filters. On the detail page it renders with a **Manage Configuration** link |
| Allow/deny registrants from specific countries | Picklist | No | **No Restrictions** | No Restrictions, Allow registrants from Countries, Block registrants from Countries | Always | — | Either non-default value reveals a **Select Allowed Countries** multi-select (country tags, `renderCountryTags()`) |
| Allow/Block Specific Domains | Picklist | No | **No Restriction** | No Restriction, Allow specific email domains, Block specific email domains | Always | — | Either non-default value reveals an **Add Allowed Domains** entry (`#domainModal`) |
| Post_Registration Custom Redirection | Text (URL) | No | Empty | — | Always | — | Placeholder `https://`. When set, a **Post Redirection URL** field follows |
| Allow access to join link only through mail | Checkbox | No | **On** | On / Off | Always | — | One of only three controls that ship on by default |
| Confirmation Email Template | Template picker | No | **Webinar Confirmation Template** | Chosen through Select Template | Only with *With Registration* | — | See §8 for the picker and its type scoping |
| Who can Join | Picklist | No | **Anyone can Join** | Anyone can Join, Only Authenticated Users can Join | Always | — | Corresponds to the module field *Allow only authenticated Zoho Users with a Zoho account* |

## 3.4 Preferences

Eight checkboxes in a two-column grid. **Three ship on**; the rest ship off.

| Field | Type | Default | Notes for the developer |
|---|---|---|---|
| Allow attendees to ask questions | Checkbox | Off | Gates the Q&A related list having any content |
| Allow anonymous questions | Checkbox | Off | Presumed dependent on the field above — the mock does not enforce it (open question) |
| Show questions to all | Checkbox | Off | — |
| Automatic session recording | Checkbox | **On** | The recording is what the Recording Link in follow-up templates points at |
| Video recording | Checkbox | **On** | — |
| Display attendee list to all | Checkbox | Off | — |
| Use Emoji reactions | Checkbox | **On** | — |
| Post webinar Re-direction | Checkbox | Off | Ticking it is what reveals a **Post Redirection URL** field |

**Correction to note:** an earlier parse placed *Thank You Email Template*, *Post Redirection URL* and
*Auto Reply for questions* in this section. In the running form, Preferences contains these eight
checkboxes and nothing else.

## 3.5 Reminders

| Field | Type | Mandatory | Default | Options / range | Visibility & dependency | Validation | Notes for the developer |
|---|---|---|---|---|---|---|---|
| 1st Reminder | Picklist | No | **15 mins before the webinar** | 2 mins, 5 mins, 10 mins, 15 mins, 30 mins before the webinar · 1 hour, 2 hours, 6 hours, 12 hours before · 1 day before · 1 week before | Always | — | The only reminder that is on by default |
| 1st Reminder Template | Template picker | No | **1st Reminder Template** | Chosen through **Select Template** | Only while 1st Reminder ≠ None | — | Renders as a *Select Template* button plus the chosen template as a link |
| 2nd Reminder | Picklist | No | **None** | None, then the same offsets as above | Always | — | — |
| 2nd Reminder Template | Template picker | No | 2nd Reminder Template | Chosen through Select Template | **Only while 2nd Reminder ≠ None** — absent in the default state | — | Confirmed: with 2nd Reminder = None, no template row renders |
| 3rd Reminder | Picklist | No | **None** | None, then the same offsets | Always | — | — |
| 3rd Reminder Template | Template picker | No | 3rd Reminder Template | Chosen through Select Template | Only while 3rd Reminder ≠ None | — | — |

## 3.6 Follow-Ups

| Field | Type | Mandatory | Default | Options / range | Visibility & dependency | Validation | Notes for the developer |
|---|---|---|---|---|---|---|---|
| Send Follow-up Email to Attendees | Picklist | No | **2 mins after the webinar ends** | None · 2 mins, 5 mins, 10 mins, 15 mins after the webinar ends · 1 hour, 2 hours, 6 hours after · 1 day after | Always | — | On by default |
| Attendees Follow-up Template | Template picker | No | **Attendees Follow-up Template** | Chosen through Select Template | Only while the offset ≠ None | — | Type *Attendees Follow-up*, so it must carry a Recording Link (§8.3) |
| Send Follow-up Email to Absentees | Picklist | No | **2 mins after the webinar ends** | Same as above | Always | — | On by default |
| Absentees Follow-up Template | Template picker | No | **Absentees Follow-up Template** | Chosen through Select Template | Only while the offset ≠ None | — | Type *Absentees Follow-up* |
| Include Recording for Attendees | Checkbox | No | Off | On / Off | Always | — | — |
| Include Recording for Absentees | Checkbox | No | Off | On / Off | Always | — | — |

Which of the two follow-ups a registrant receives is decided by whether they attended — the
*Webinar Status* on the registrant row (§4.5).

## 3.7 Validation and save behaviour

**Only one field blocks save: Webinar title.** Pressing **Save** with it empty (Figure 57):

1. The page scrolls to the top of the form.
2. The title input takes an error border and focus.
3. An inline message appears beneath it, in red: **"Webinar title cannot be empty"**.
4. Nothing is saved and the user stays on the form.

No other field in any of the five sections blocks save in the mock — every other control has a usable
default. **Save & New** and **Save** share this validation.

What the mock does *not* demonstrate, and so must be settled before build: what the saved record is
named beyond the title, which list view the user lands on, and whether a toast confirms the save.
These are open questions.

---

# 4. Scheduled webinar — live

The reference record: **Real Estate Webinar**, Scheduled, Mon Aug 11 2025 11:00 AM IST, 1 hr 30 mins.

## 4.1 List page

**Path:** left nav ▸ **Zoho Webinar**.

**Views** (tabs across the top, each with a pin affordance): All Webinars · **My Webinars** (the
default) · Scheduled Webinars · Completed Webinars · Today's Webinars · Ongoing Webinars (carries a
live dot) · On Demand Webinars.

**Toolbar:** Filter · Sort · four view-mode icons (list, kanban, canvas, chart) · a ⋮ overflow · a
play control · a ▼ control · **Create Webinar** (primary) · a ⋮ record-actions menu.

**Columns**, in order: Webinar Name · Webinar Category · Webinar Date & Time · Registration Count ·
Attendance Count · Attend. Rate · Webinar Duration · Organiser · Webinar Type.

**Rows** — the six the mock ships, which are also the four record states this PRD documents:

| Webinar Name | Webinar Category | Date & Time | Reg. | Att. | Rate | Duration | Type |
|---|---|---|---|---|---|---|---|
| Real Estate Webinar | Scheduled Webinar | Mon, Aug 11 2025 11:00 AM IST | 142 | — | — | 1 hr 30 mins | Live Webinar |
| Recurrent Webinar ⟳ | Scheduled Webinar | Tue, Sep 2 2025 10:00 AM IST | 89 | — | — | 1 hr 0 mins | Live Webinar |
| Recurrent Webinar ⟳ | Scheduled Webinar | Tue, Sep 9 2025 10:00 AM IST | 61 | — | — | 1 hr 0 mins | Live Webinar |
| Contact Webinar | Completed Webinar | Mon, Aug 11 2025 11:00 AM IST | 203 | 157 | 77% | 1 hr 30 mins | Live Webinar |
| Product Reveal Webinar | Completed Webinar | Wed, Sep 3 2025 02:00 PM IST | 318 | 241 | 76% | 1 hr 0 mins | Live Webinar |
| On Demand Webinar | On-Demand Webinar | Mon, Mar 10 2025 10:00 AM IST | 184 | 131 | 71% | 1 hr 0 mins | On-Demand Webinar |

Reading rules for the build:

- **Webinar Category** is the *state* (Scheduled / Completed / On-Demand) and is colour-coded;
  **Webinar Type** is the *kind* chosen at creation (Live / On-Demand). A record can be
  Category = Completed while Type = Live Webinar.
- **Attendance Count** and **Attend. Rate** are empty (`—`) for scheduled records: they only exist
  once the session has happened.
- The recurrence marker (⟳) sits beside the name, and each occurrence is its own row and its own record.

**Filter sidebar** — *Filter By Fields* lists the module's filterable fields: Webinar Title, Webinar
Type, Webinar Date & Time, Webinar Duration, Organiser, Co-Organiser, Description, Registration Type,
Registration Form, Moderation Type, Set Registration Limit, Push to CRM, Allow/deny registrants from
specific countries, Allow/block specific domains, Post_Registration Custom Redirection, Allow access
to join through email, Allow only authenticated Zoho Users with a Zoho account, Send Confirmation to
Registrants, Allow attendees to ask questions, Allow anonymous questions, Show questions to all,
Automatic session recording, Video recording, Display attendee list to all, Use Emoji reactions,
Post Webinar Re-direction, Send Follow-up Email to Attendees, Send Follow-up Email to Absentees. Plus
*System Defined Filters*: Touched Records, Untouched Records, Record Action, Related Records Action.

*Figure 1 — the list page.*

**Two mock inconsistencies to resolve, not to copy:** the footer reads **Total Records 12** while six
rows render and pagination reads *1 to 10*; and the filter sidebar is headed **"Filter Invoices by"**.

## 4.2 Detail page

*Figure 26 — scheduled live detail, header and registration overview.*

**Header:** record avatar · **Real Estate Webinar** · state suffix **– Scheduled** · *Add Tags* · a
countdown pill **"⏱ Starts in 16 mins"**. Action buttons, left to right:
**Start Webinar** · **Send Invite** · **View Registration Link** · **Edit** · **Actions ▾**.

**Actions ▾** (identical across states — Figure 20): Clone · Share · Delete · Share via Cliq ·
Print Preview · Customize Business Hours · Organize Campaigns · Add Related List · Add Kiosk ✨ ·
Create Button · Create Client Script · View Followers.

**Tabs:** **Overview** (default) · Timeline.

**Related-list rail:** Notes · Invited (100) · Polls (2) · Q&A · Recordings · Session Files ·
Open Activities · Closed Activities.

**Summary card:** Webinar Date & Time · Webinar Duration · Organiser · Co - Organiser · Webinar Type.

**Registration & Attendance Summary** — in the scheduled state this shows registration only:

| Tile | Value in the mock | Notes |
|---|---|---|
| Total Registration | donut at 5%, **10 / 200**, *190 seats left* | The `/200` and seats-left line come from Set Registration Limit |
| Waiting for Approval | **5**, with a *View →* link | Only meaningful under Manual Moderation |

Then **Registration by Module** (pie: Lead 7, Contact 2, Vendor 1) · **Registration by Source** (bar,
two series *Visited* and *Registered*, across Email / LinkedIn / Twitter / Direct) · **Daily
Registration Trend** (line, with Total Registered, Peak Day and Avg / Day read-outs). Each chart has a
type switcher (Pie ▾ / Bar ▾) and a drill-in that opens a record table.

**Registrants list** — pill tabs **Approved Registrants (6)** · **Unapproved Registrants (6)** ·
**Denied Registrants (3)**; columns Last Name · Email · All Modules ▾ · All Sources ▾ · Registered
Date; footer actions **Deny All** and **Approve All**.

**Hide Details** panel — the record's stored values in two groups, *Webinar Details* (Webinar Title,
Webinar Type, Webinar Date & Time, Webinar Duration, Organiser, Co-Organiser, Repeat Webinar,
Description) and *Registration Details* (Registration Type, Registration Form, Moderation Type, Set
Registration Limit, Push to CRM with a **Manage Configuration** link, Allow/deny registrants from
specific countries).

**Related lists in the scheduled state** — the empty/pre-session variants:

| Related list | Scheduled-state content |
|---|---|
| Notes | *No records found.* · **+ Add Note** |
| Invited (100) | Pill tabs **Invited 100 · Registered 2 · Not Registered 3** and an **Invite** button. Columns Name · Email · Module · All Invite Status ▾ · Invite Sent on |
| Polls (2) | The two polls with **all vote counts at 0**, plus a **Create Poll** button |
| Q&A | Placeholder: *"Q&A will be available after the webinar is completed."* |
| Recordings | *No recordings available.* |
| Session Files | **Attach Files** · *"No files attached. Click "Attach Files" to add."* |
| Open / Closed Activities | *No records found.* · **+ Add Activity** |

**There is no Webinar Revenue panel in the scheduled state** — it appears only once attendance exists.

**Known mock defect:** the *Hide Details* panel renders static placeholder content (*Test Webinar*,
*Live Webinar*, *XYZ*, *1000*) on every record rather than that record's values. Build it from the record.

## 4.3 Registration Link and source tracking

**Entry point:** header ▸ **View Registration Link**. Opens the **Registration Link** modal (Figure 27).

| Element | Type | Default | Notes |
|---|---|---|---|
| Default Registration Link | Read-only link | `https://meet.zoho.com/qyat-ceg-zml` | With a **copy** icon and an **embed code** (`<>`) icon |
| Enable Source Tracking for Registration Link | Toggle | **Off** | Off hides everything below |
| Create New Source Tracking Link | Button | — | Only while the toggle is on |
| Source tracking table | Table | Empty | Columns Source Name · Created By · Visited Count · Registered Count · Actions. Empty state: *"No source tracking links created yet."* |

**Create New Source Tracking Link** (Figure 29) is a nested dialog: *"Enter a name for the source to
track registrations from different channels."* One field, **Source Name** (placeholder *e.g. Twitter*),
with **Cancel** and **Add**; Add is disabled until a name is entered.

On Add, a row appears (Figure 30) carrying Source Name, **Created By** as *"<user> on <date/time>"*,
a Visited Count, a Registered Count, and three row actions: copy · embed code · an enable toggle
(on by default). The two counts are what feed the *Visited / Registered* series in Registration by Source.

*Figures 27–30 — the registration link modal, source tracking off/on, the create dialog and a created row.*

## 4.4 Send Invite flow

**Entry point:** header ▸ **Send Invite**. Two steps — there is no separate module-chooser step; the
record picker opens directly with a module dropdown in it.

**Step 1 — Record picker** (Figure 3). A **module dropdown** (populated from Invite Modules, §2.5),
then a **view dropdown**, then the record table with checkbox selection. Selecting records raises a
selection bar with **Remove ALL** and **Next** (Figure 4).

**Step 2 — Mass Email** (Figure 5). The CRM Mass Email compose step: **To** (the chosen records),
**Select Template** (with the chosen template shown beside it as a preview link), **From**, sending
warnings, and **Send Options**. The *"Sent later, automatically"* section is deliberately not present
in this flow.

**Select Template** (Figure 6) lists **All Templates** with a search box and **+ Create Template**.
Creating from here skips the module + type dialog, because the step already implies the type is
*Webinar Invitation* (§8.2).

**Dependency to respect:** the module dropdown in Step 1 offers exactly the modules ticked in Invite
Modules. A module removed there must vanish here.

## 4.5 Registrants and attendance

Two related but distinct lists, and the difference matters:

| | **Registrants list** / Attendees and Registrants List | **Invited** related list |
|---|---|---|
| Who is in it | Everyone who signed up, from any source | Only CRM records the rep invited from CRM |
| Keyed on | A registration | A CRM record |
| Status shown | Approved / Unapproved / Denied, then Attended / Not Attended | Invite Status (Registered / Not Registered) and Webinar Status (Attended / Not Attended) |
| Extra column | Source (Email, Twitter, LinkedIn, Direct) | **Invite Sent on** — *"<user> on <date> at <time>"* |
| Module column | Present, and may be blank for someone not in CRM | Always a module |

A registrant not in CRM shows `—` in the module column (the mock's *Pooja Iyer*, *Sathish Babu*,
*Deepak Menon*, *Anitha Raj*), which is exactly the population *Push Webinar Registrants to CRM* and
the registration forms (§8.5) exist to convert.

---

# 5. Scheduled webinar — on demand

The reference record: **On Demand Webinar**, Webinar Type *On-Demand Webinar*, Mon Mar 10 2025
10:00 AM IST, 1 hr 0 mins. Header state suffix reads **– On Demand**.

Everything in §4.2 holds unless listed here.

## 5.1 What differs from scheduled live

| Aspect | Scheduled live | On demand |
|---|---|---|
| Header state suffix | – Scheduled | **– On Demand** |
| Countdown pill | *Starts in 16 mins* | **None** |
| Header action buttons | Start Webinar · Send Invite · View Registration Link · Edit · Actions | **Edit · Actions only** |
| Related-list rail | Notes · Invited · Polls · Q&A · Recordings · Session Files · Activities | **Notes · Invited · Q&A · Activities** — no Polls, no Recordings, no Session Files |
| Registration Overview | Donut *n / limit* + Waiting for Approval | **Three tiles: Total Registration 30 · Total Attendees 15 (50%) · Total Absentees 15 (50%)** |
| Charts | Registration by Module / by Source / Daily Trend | Adds **Attendance by Module** and **Attendance by Source** |
| Registrant list | Registrants list, 3 approval tabs | **Attendees and Registrants List**, 6 tabs (§5.2) |
| Q&A | *"Q&A will be available after the webinar is completed."* | Questions present, **but no Host replies** |
| Webinar Revenue | Absent | **Present** (§6.3) |

**Why the header has no Send Invite:** an on-demand webinar has no start time to invite people to,
so the mock drops both *Start Webinar* and *Send Invite*. Confirm this is intended — an on-demand
session arguably still wants an invite. See open questions.

## 5.2 Attendees and Registrants List

Six pill tabs, each with a count, replacing the scheduled state's three:

| Tab | Count in the mock |
|---|---|
| All Attendees | 9 |
| All Absentees | 5 |
| All Registrants | 14 |
| Approved Registrants | 6 |
| Unapproved Registrants | 6 |
| Denied Registrants | 3 |

Columns: Last Name · Email · All Modules ▾ · All Sources ▾ · **Polls** · **Q&A** · Registered Date ·
**Webinar Status**. Polls shows a participation count as a link (or `—`), Q&A shows *Yes* (or `—`),
and Webinar Status is a badge: green **Attended** or red **Not Attended**.

A second panel, **Top Attendees**, lists Name · Email · Source · Registered Date, filtered by an
*All Modules* dropdown.

*Figures 14–16 — on-demand detail, the attendees list, and the Invited related list.*

## 5.3 Invited related list, post-session

The Invited pill tabs gain the attendance halves that the scheduled state does not have:

**Invited 100 · Registered 2 · Not Registered 3 · Attended 1 · Not Attended 4**, and the columns add
**Webinar Status** beside Invite Status. The **Invite** button is gone.

---

# 6. Completed webinar

The reference record: **Product Reveal Webinar**, Completed, Wed Sep 3 2025 02:00 PM IST, Webinar
Type *Live Webinar*. Header state suffix **– Completed**.

## 6.1 What differs from the other states

| Aspect | Scheduled live | On demand | **Completed** |
|---|---|---|---|
| Header suffix | – Scheduled | – On Demand | **– Completed** |
| Header actions | Start · Send Invite · Registration Link · Edit · Actions | Edit · Actions | **Edit · Actions** |
| Related-list rail | full set | no Polls/Recordings/Session Files | **full set: Notes · Invited · Polls (2) · Q&A · Recordings · Session Files · Activities** |
| Registration Overview | donut + approval tile | 3 tiles | **3 tiles** (Total Registration · Total Attendees · Total Absentees) |
| Polls | present, **all counts 0**, *Create Poll* button | absent | **present with results**, no Create Poll |
| Q&A | placeholder text | questions only | **questions with Host replies** |
| Session Files | *Attach Files*, empty | absent | **4 files listed**, no Attach Files button |
| Webinar Revenue | absent | present | **present** |

The pattern for the build: **scheduled = collect, completed = report.** The same related lists change
from input affordances (Create Poll, Attach Files, Invite) to read-outs.

*Figures 21–25 — completed detail, attendees list, polls, Q&A with host replies, recordings and session files.*

## 6.2 Polls, Q&A, Recordings and Session Files

**Polls (2)** — a *Poll Answered by* filter (All Modules / Leads / Contacts / Vendors / Not in CRM),
then each poll rendered as its question, its options with vote counts, a **% Voted** and a
**Total Votes** read-out. The mock's two polls:

| Question | Options and votes | Voted | Total Votes |
|---|---|---|---|
| How would you rate this webinar? | ⭐1 Poor 42 · ⭐⭐2 Fair 31 · ⭐⭐⭐3 Good 18 · ⭐⭐⭐⭐4 Very Good 9 · ⭐⭐⭐⭐⭐5 Excellent 42 | 67.3% | 100 |
| Would you recommend us to others? | Yes, definitely 42 · Maybe 31 · No, not really 18 | 67.3% | 100 |

A participant table follows (Name · Email · Company · Phone · Owner), 23 records, so poll respondents
are resolvable back to CRM records.

**Q&A** — an *Overall Q&A* filter (Overall / Leads / Contacts / Not in CRM) and a participation
summary (*Participated in Q&A : 21 · Leads: 7 · Contacts: 7 · Not in CRM: 5*). Questions render as a
chat: asker avatar, name, time, module tag, the question, and — in the completed state only —
the **Host** reply with the host's name and time. Some questions have no reply, so replies are optional.

**Recordings** — empty in the mock: *"No recordings available."* even on a completed record whose
*Automatic session recording* preference is on by default. **This is the one gap that matters most**,
because the Attendees/Absentees Follow-up template types *require* a Recording Link (§8.3). See open questions.

**Session Files (4)** — File Name (with a type icon) · Size · Date Added:
`Webinar_Slides_Q3.pdf` 3.2 MB Sep 4 2025 · `Product_Demo_Recording.mp4` 128 MB Sep 4 2025 ·
`Attendee_Handout.docx` 0.8 MB Sep 3 2025 · `Q3_Promo_Banner.png` 1.4 MB Sep 1 2025.

## 6.3 Webinar Revenue — the attribution payoff

A collapsed section headed **Webinar Revenue**, present on completed and on-demand records only. It is
where the attribution model chosen in §2.6 becomes visible on the record.

**Webinar ROI** — six tiles:

| Tile | Value in the mock | Derivation |
|---|---|---|
| Cost | $800 | The *Webinar Cost* field from creation |
| Revenue (Won) | $16,800 | Attributed revenue from Closed Won deals |
| ROI | +2000% | (Revenue − Cost) / Cost |
| In Pipeline | $32,450 | Attributed value of open deals |
| Cost / Attendee | $53 | Cost ÷ attendees |
| Revenue / Attendee | $1,120 | Revenue ÷ attendees |

Then **Pipeline by Stage** (pie: Proposal Sent 7 · Negotiation 5 · Closed Won 9 · Closed Lost 3 ·
Waiting for Manager 4) and **Deals Won by Source** (pie: Twitter 4 · Email 3 · LinkedIn 2 · Direct 1).

Then two record tables:

- **Deals Won** — Deal Name · Amount · Stage · Account Name · Contact Name. 7 records, all *Closed Won*.
- **Deals in Pipeline** — the same columns plus **Probability**. 14 records, paginated 10 per page,
  and it includes *Closed Won* and *Closed Lost* rows at 100% / 0%.

*Figures 17–19 — the ROI tiles, Deals Won and Deals in Pipeline.*

**Two things for the build to settle:** the ROI tiles do not reconcile with the tables (the seven
Deals Won rows sum to $16,000, not the $16,800 shown), and *Deals in Pipeline* contains closed deals,
which contradicts its name. Both are open questions.

---

# 7. Completed webinar — on demand

The mock's **On Demand Webinar** record *is* the completed on-demand case: its Webinar Category is
*On-Demand Webinar*, and it carries attendance (131 of 184), absentees and a Webinar Revenue panel —
all of which only exist post-session.

The mock therefore does **not** model a distinct "not yet watched" versus "watched" on-demand state.
What is documented in §5 is the on-demand record with attendance present.

| Aspect | Completed live | Completed on demand |
|---|---|---|
| Header suffix | – Completed | – On Demand |
| Polls | Present with results | **Absent** |
| Recordings | Present (empty) | **Absent** |
| Session Files | Present, 4 files | **Absent** |
| Q&A | Questions **with Host replies** | Questions, **no Host replies** |
| Webinar Revenue | Present | Present |
| Attendance tiles | Present | Present |

**Open question:** whether an on-demand webinar genuinely has no polls, recordings or session files, or
whether the mock simply did not populate them. Given that an on-demand webinar *is* a recording, the
absence of a Recordings related list looks like a gap rather than a decision.

---

# 8. Supporting flows

## 8.1 Email templates: where they live, and the two lists

Webinar templates surface in **two places**, and they do not agree.

**A. Setup ▸ Customization ▸ Templates ▸ Email**, module filter **Zoho Webinar** (Figure 33).
Page chrome: type tabs **Email** / Inventory / Mail Merge · a module dropdown · a **Search Template**
box · **+ New Template** · a left folder rail (All Templates, Favorites, Associated Templates, Created
by me, Shared with me, Public Email Templates, Managerial templates, and named folders). Columns:
Template Name · Modified By · Last Used · Stats.

The module dropdown offers: All Modules · Contacts · Accounts · Potentials · Financial Services ·
Tasks · Meetings · Calls · **Zoho Webinar**.

Filtered to Zoho Webinar, **seven** templates, each with a one-line purpose:

| Template Name | Sub-line in the list |
|---|---|
| Webinar Invitation Template | Sent when you invite CRM records to a webinar |
| Confirmation Template | Sent as soon as someone registers |
| 1st Reminder Template | Sent before the webinar starts |
| 2nd Reminder Template | Sent before the webinar starts |
| 3rd Reminder Template | Sent before the webinar starts |
| Attendees Follow-up Template | Sent after the webinar to those who attended |
| Absentees Follow-up Template | Sent after the webinar to those who missed it |

**B. Setup ▸ Modules and Fields ▸ Zoho Webinar ▸ Preferences** (Figure 43), headed
**Customise Email Notifications** with the sub-line: *"The emails Zoho Webinar sends — from the invite
through to cancellation. They belong to this module and are managed here, not under Setup › Templates."*

Columns Template Name · Modified By · Last Used · a **Customise Template** button per row. **Eight**
templates:

| Template Name | Customise Template |
|---|---|
| Send Invite Template | Enabled |
| Webinar Confirmation Template | Enabled |
| 1st Reminder Template | Enabled |
| 2nd Reminder Template | Enabled |
| 3rd Reminder Template | Enabled |
| Attendees Follow-up Template | Enabled |
| Absentees Follow-up Template | Enabled |
| **Meetings Cancelled Template** | **Disabled** |

**The discrepancies to resolve before build** — the same set of emails is named differently in the two
places (*Webinar Invitation Template* vs *Send Invite Template*; *Confirmation Template* vs *Webinar
Confirmation Template*), Preferences carries a **Meetings Cancelled Template** that Setup ▸ Templates
does not list at all, and its *Customise Template* button is disabled with no explanation. Also note
that the Preferences copy claims these templates are *not* managed under Setup ▸ Templates, while
Setup ▸ Templates lists them.

## 8.2 Create Email Template → Gallery → editor → Save

**Step 1 — Create Email Template dialog** (Figure 34), from **+ New Template**:

| Field | Type | Mandatory | Default | Options (verbatim, UI order) |
|---|---|---|---|---|
| Select Module | Picklist | Yes | Inherited from the list filter (*Zoho Webinar*) | Zoho Webinar, Leads, Contacts, Vendors, Custom Module 1 |
| Template Type | Picklist | Yes | Webinar Invitation | **None**, Webinar Invitation, Confirmation Email, 1st Reminder, 2nd Reminder, 3rd Reminder, Attendees Follow-up, Absentees Follow-up |

Buttons: **Cancel** · **Next**.

**This dialog is skipped** when the flow already implies the type — from a Create Webinar template
slot, or from Send Invite. The type is then fixed by the calling context.

**Step 2 — Template Gallery** (Figure 35). Header **Template Gallery**, the module (*Zoho Webinar ▾*),
the chosen type as a chip (*Webinar Invitation*), and **Insert HTML / Plain Text** at top right. One
category, **Basic (6)**: Blank · One column · Two column · Two column with image 1 ·
Two column with image 2 · Three column.

**Step 3 — Editor** (Figure 36). Header shows the **type** as the title with
*"<layout> · <module>"* beneath it and the module as a chip, then **1 Attachments** · **Cancel** ·
**Preview** · **Save ▾**. Toolbar: font · size · **B** · *I* · U · link · image · align. A left
component rail (Button styles: NORMAL / ROUNDED / OVAL) and a hint: *"Type # to insert merge field."*
The body carries a type-specific placeholder — for an invitation, *"Write the webinar invitation email
here. Type # to insert a merge field."*

**Step 4 — Save** (Figure 41). **Save** opens a **Save Template** dialog: **Template Name** pre-filled
(*"Webinar Invite - Zoho Webinar"*), helper text *"Saved to Zoho Webinar Templates"*, and
**Cancel** / **Save**. Saving returns to the list the flow started from.

**Observed save behaviour to settle:** after saving, the Zoho Webinar template list still shows only
the seven defaults — the new template does not appear, and no confirmation toast is shown (Figure 42).

## 8.3 Template type → allowed links → required link

The single most important rule set in this feature. **Insert Link** and **Insert Button** offer only
the link types the template's type permits, and **Save is blocked** unless the type's required link is
present in the body.

| Template type | Allowed link types (verbatim, UI order) | Required link |
|---|---|---|
| **None** | Web URL, Email, Registration Link, Join URL, Cancel Registration, Recording Link, Add To Calendar, Add To Google Calendar, Add To Yahoo Calendar, Add To Outlook Calendar, Add To Zoho Calendar | *(none)* |
| **Webinar Invitation** | Web URL, Email, Registration Link, Add To Calendar, Add To Google/Yahoo/Outlook/Zoho Calendar | **Registration Link** |
| **Confirmation Email** | Web URL, Join URL, Cancel Registration, Add To Calendar, Add To Google/Yahoo/Outlook/Zoho Calendar | **Join URL** |
| **1st Reminder** | Web URL, Join URL, Cancel Registration, Add To Calendar, Add To Google/Yahoo/Outlook/Zoho Calendar | **Join URL** |
| **2nd Reminder** | as 1st Reminder | **Join URL** |
| **3rd Reminder** | as 1st Reminder | **Join URL** |
| **Attendees Follow-up** | Web URL, Join URL, **Recording Link**, Add To Calendar, Add To Google/Yahoo/Outlook/Zoho Calendar | **Recording Link** |
| **Absentees Follow-up** | as Attendees Follow-up | **Recording Link** |

Read from `TPL_TYPE_LINKS` and `TPL_REQUIRED_LINK` and confirmed in the UI: with type *Webinar
Invitation*, the Insert Link dropdown offered exactly eight options and **no** Join URL, Cancel
Registration or Recording Link.

**Insert Link dialog** (Figure 38). Fields adapt to the link type:

| Link Type | Fields shown | Pre-fill |
|---|---|---|
| Web URL | Link Type · **Link Address** (placeholder `https://`) · Text To Display | — |
| Registration Link | Link Type · Text To Display *(no Link Address)* | Text To Display = **"Register Now"**; helper note *"The registration page for this webinar."* |

The Link Address field disappears for system-supplied links, because the URL is resolved per
registrant at send time (Figure 40).

**Save validation** (Figure 39). Saving a *Webinar Invitation* template with no Registration Link
produces a red banner beneath the toolbar, verbatim:

> **A Webinar Invitation template must contain a Registration Link. Insert one before saving.**

The message is composed from the type name and the required link, so each of the seven types produces
its own variant. Inserting the required link and saving again succeeds.

## 8.4 Merge fields

Typing **#** in the editor body opens the merge-field picker (Figure 37): a category dropdown and the
category's fields.

**Categories on an invitation template:** Webinar Details · Users · Organization.
**On every later lifecycle email:** **Registrations** is added *above* Webinar Details, because those
emails go to a registrant rather than to a CRM record.

| Category | Fields (verbatim, UI order) |
|---|---|
| **Webinar Details** | Webinar Title, Webinar Date & Time, Webinar Organiser, Webinar Duration, Description |
| **Registrations** | Registration Id, Country, Created By, Created Time, Email, First Name, Modified By, Timezone, Add To Google Calendar, Add To Yahoo Calendar, Add To Outlook Calendar, Add To Zoho Calendar, Add To Calendar, **Join URL**, Handouts, **Cancel Registration**, Audio Details, **Registration URL**, Full Name, Last Name, Abuse Email, iOS app URL |
| **Users** | User Id, User Name, Email, Role, Profile |
| **Organization** | Company Name, Website, Phone, Street, City, State, Country |

Note that the per-registrant links (Join URL, Cancel Registration, Registration URL, the calendar
links) exist **both** as Insert Link types and as Registrations merge fields — two routes to the same
value. The mock also carries record-module sources (Leads, Contacts, Custom Module 1/2, Lead Owner and
others) for templates whose module is a CRM module rather than Zoho Webinar.

## 8.5 Registration forms and push-to-CRM

**Path:** Setup ▸ Modules and Fields ▸ **Zoho Webinar** ▸ **Registration Form** (Figure 44).

Headed **Registration Forms**, sub-line *"Forms used to collect registrant details and push them into
CRM as records."* Columns Form Name · **Push As** · Description · Created Time, plus **+ Create Form**.

| Form Name | Push As | Description | Created Time |
|---|---|---|---|
| Leads form | Leads | Default form used to register leads for a webinar | 02 Jan 2026 |
| Contacts | Contacts | Default form used to register existing contacts for a webinar | 05 Dec 2025 |

**This is the mechanism behind *Push Webinar Registrants to CRM***: the form's **Push As** value
decides which module a registrant becomes a record in. It is also what closes the gap identified in
§4.5 — registrants with no module (`—`) are the ones not yet pushed.

Note the mock's *Registration Form* picklist on the create form offers *Default Form*, *Real Estate
Form* and *Stock Trading Form*, none of which are the two forms configured here. See open questions.

## 8.6 The module's own configuration

**Path:** Setup ▸ Modules and Fields ▸ **Zoho Webinar**. The module carries a *New* badge in the
module list. Tabs: **Layouts · Layout Rules · Validation Rules · Fields · Buttons · Preferences ·
Registration Form · Summary** — Preferences opens by default.

The **Fields** tab (Figure 45) is the authoritative field-type list for the module — reproduced in
full in Appendix B.

---

# 9. Appendices

## Appendix A — Screen inventory

57 screens, numbered in reading order. Files live in `docs/prd/zoho-webinar/screens/`.

| Fig | File | Screen | How it is reached | What it demonstrates |
|---|---|---|---|---|
| 1 | 01-webinar-list.jpg | Zoho Webinar module list | Left nav ▸ Zoho Webinar | Views, columns, six records covering all four states |
| 2 | 02-scheduled-live-detail.jpg | Scheduled live detail | List ▸ Real Estate Webinar | Header actions and registration summary |
| 3 | 03-send-invite-record-picker.jpg | Send Invite, record picker | Detail ▸ Send Invite | Module dropdown, view dropdown, record table |
| 4 | 04-send-invite-records-selected.jpg | Send Invite, selection | Tick two records | Selection bar, Remove ALL, Next |
| 5 | 05-mass-email.jpg | Mass Email | Send Invite ▸ Next | To, Select Template, From, warnings, Send Options |
| 6 | 06-select-template.jpg | Select Template | Mass Email ▸ Select Template | All Templates, search, + Create Template |
| 7 | 07-create-webinar-details-registration.jpg | Create Webinar, top | List ▸ Create Webinar | Webinar Details + Registration Setup |
| 8 | 08-create-webinar-preferences-reminders-followups.jpg | Create Webinar, bottom | Scroll the create form | Preferences, Reminders, Follow-Ups |
| 9 | 09-marketplace-zoho.jpg | Marketplace ▸ Zoho | Setup ▸ Marketplace ▸ Zoho | Zoho Meetings card, DEMO case switcher |
| 10 | 10-integration-intro.jpg | Integration introduction | Zoho Meetings ▸ For webinars ▸ Set up | NOT ENABLED state |
| 11 | 11-integration-case1-no-account.jpg | Case 1 | Case 1 ▸ Enable Integration | Select Organization, no account found |
| 12 | 12-integration-setup-connection-invite-modules.jpg | Setup page, top | Case 2 ▸ Enable Integration | Email, Organisation, Sync + Invite Modules |
| 13 | 13-integration-setup-attribution.jpg | Setup page, bottom | Scroll the setup page | Deal Attribution, Linear pre-selected |
| 14 | 14-ondemand-detail-overview.jpg | On-demand detail | List ▸ On Demand Webinar | Attendance tiles, four charts |
| 15 | 15-ondemand-attendees-registrants-list.jpg | Attendees and Registrants List | Scroll the on-demand record | Six pill tabs, Polls/Q&A/Webinar Status columns |
| 16 | 16-ondemand-invited-related-list.jpg | Invited related list, post-session | Scroll further | Attended / Not Attended tabs, no Invite button |
| 17 | 17-webinar-revenue-roi-attribution.jpg | Webinar ROI | Expand Webinar Revenue | Six ROI tiles, Pipeline by Stage, Deals Won by Source |
| 18 | 18-webinar-revenue-deals-won.jpg | Deals Won | Scroll the revenue panel | Attributed closed-won deals |
| 19 | 19-webinar-revenue-deals-in-pipeline.jpg | Deals in Pipeline | Scroll further | Open deals with Probability |
| 20 | 20-detail-actions-menu.jpg | Actions menu | Detail ▸ Actions ▾ | The twelve record actions |
| 21 | 21-completed-detail-overview.jpg | Completed detail | List ▸ Product Reveal Webinar | Polls/Recordings/Session Files in the rail |
| 22 | 22-completed-attendees-registrants-list.jpg | Completed attendees list | Scroll the completed record | Attended / Not Attended badges, registrants not in CRM |
| 23 | 23-completed-polls.jpg | Polls with results | Scroll to Polls | Vote counts, % Voted, Total Votes |
| 24 | 24-completed-qa-with-host-replies.jpg | Q&A with Host replies | Scroll to Q&A | Host answer bubbles — completed only |
| 25 | 25-completed-recordings-session-files.jpg | Recordings and Session Files | Scroll to the foot | Empty Recordings; four session files |
| 26 | 26-scheduled-live-detail-header-registration.jpg | Scheduled live header | List ▸ Real Estate Webinar | Start/Send Invite/Registration Link, countdown pill, seats-left donut |
| 27 | 27-registration-link-modal.jpg | Registration Link modal | Detail ▸ View Registration Link | Default link, copy/embed, source-tracking toggle off |
| 28 | 28-registration-link-source-tracking-empty.jpg | Source tracking on | Toggle it on | Create button and the empty table |
| 29 | 29-create-source-tracking-link-dialog.jpg | Create source tracking link | Click Create New Source Tracking Link | Source Name, disabled Add |
| 30 | 30-source-tracking-link-created.jpg | A created tracking link | Enter a name and Add | Created By, Visited/Registered counts, row actions |
| 31 | 31-setup-templates-all-modules.jpg | Templates, all modules | Setup ▸ Templates | Page chrome, folder rail, mixed-module list |
| 32 | 32-templates-module-dropdown.jpg | Module dropdown | Click All Modules ▾ | The nine module options |
| 33 | 33-templates-zoho-webinar-7-defaults.jpg | The seven webinar defaults | Pick Zoho Webinar | Names and purpose sub-lines |
| 34 | 34-create-email-template-dialog.jpg | Create Email Template | + New Template | Select Module, Template Type |
| 35 | 35-template-gallery-basic.jpg | Template Gallery | Next | Basic (6) layouts, type chip, Insert HTML / Plain Text |
| 36 | 36-template-editor-invitation.jpg | Template editor | Pick One column | Header, toolbar, type-specific placeholder, button rail |
| 37 | 37-merge-field-picker.jpg | Merge-field picker | Type `#` in the body | Category dropdown and Webinar Details fields |
| 38 | 38-insert-link-dialog.jpg | Insert Link | Toolbar ▸ link icon | Link Type, Link Address, Text To Display |
| 39 | 39-required-link-save-error.jpg | Required-link error | Save with no Registration Link | The exact blocking message |
| 40 | 40-insert-registration-link.jpg | Registration Link selected | Set Link Type to Registration Link | Link Address gone, "Register Now" pre-filled |
| 41 | 41-save-template-dialog.jpg | Save Template | Save with the link present | Pre-filled name, "Saved to Zoho Webinar Templates" |
| 42 | 42-templates-list-after-save.jpg | List after saving | Save | The new template does not appear |
| 43 | 43-modfields-zoho-webinar-preferences.jpg | Module Preferences | Modules and Fields ▸ Zoho Webinar | Eight lifecycle emails, disabled Meetings Cancelled |
| 44 | 44-modfields-registration-forms.jpg | Registration Forms | The Registration Form tab | Push As mapping, + Create Form |
| 45 | 45-modfields-fields-tab.jpg | Fields | The Fields tab | Authoritative field types |
| 46 | 46-marketplace-zoho-meetings-card.jpg | Zoho Meetings card | Setup ▸ Marketplace ▸ Zoho | The two halves and the shared-login note |
| 47 | 47-integration-intro-not-enabled.jpg | Introduction page | For webinars ▸ Set up | Hero, How it works, Why teams enable it |
| 48 | 48-integration-intro-when-you-enable.jpg | "When you enable" | Scroll the intro | The four commitments |
| 49 | 49-integration-case3-multiple-orgs.jpg | Case 3 | Case 3 ▸ Enable Integration | Organisation chooser and its constraint |
| 50 | 50-integration-attribution-linear-default.jpg | Deal Attribution | Scroll the setup page | Six models, Linear pre-selected |
| 51 | 51-integration-enabled-active-toast.jpg | Enabled state | Enable Integration | ACTIVE pill, Deactivate, success toast, read-only connection |
| 52 | 52-integration-enabled-dirty-save-bar.jpg | Dirty state | Tick a module | "You have unsaved changes" bar, updated chip row |
| 53 | 53-integration-case4-not-an-admin.jpg | Case 4 | Case 4 ▸ Enable Integration | Insufficient Permission, Notify Super Admin |
| 54 | 54-integration-case5-trial-expired.jpg | Case 5 | Case 5 ▸ Enable Integration | Trial Expired, no action button |
| 55 | 55-create-webinar-details-registration-live.jpg | Create Webinar, top (verified) | List ▸ Create Webinar | Compound date/time, split duration, real defaults |
| 56 | 56-create-webinar-preferences-reminders-followups-live.jpg | Create Webinar, bottom (verified) | Scroll to the foot | The eight Preferences checkboxes; conditional template rows |
| 57 | 57-create-webinar-title-required-error.jpg | Title validation | Save with an empty title | The exact blocking message |

## Appendix B — Field reference

### B.1 Module fields (Setup ▸ Modules and Fields ▸ Zoho Webinar ▸ Fields)

The authoritative field/type list, verbatim and in UI order — 26 fields.

| # | Field Label | Field Type |
|---|---|---|
| 1 | Webinar Title | Single Line |
| 2 | Webinar Category | Pick List |
| 3 | Webinar Type | Pick List |
| 4 | Webinar Date & Time | Date/Time |
| 5 | Webinar Duration | Duration |
| 6 | Organiser | Lookup |
| 7 | Co-Organiser | Lookup |
| 8 | Description | Multi Line |
| 9 | Registration Type | Pick List |
| 10 | Registration Form | Pick List |
| 11 | Moderation Type | Pick List |
| 12 | Set Registration Limit | Number |
| 13 | Push to CRM | Boolean |
| 14 | Allow/deny registrants from specific countries | Multi Select |
| 15 | Allow/block specific domains | Multi Select |
| 16 | Post_Registration Custom Redirection | URL |
| 17 | Allow access to join through email | Boolean |
| 18 | Allow only authenticated Zoho Users with a Zoho account | Boolean |
| 19 | Send Confirmation to Registrants | Boolean |
| 20 | Allow attendees to ask questions | Boolean |
| 21 | Allow anonymous questions | Boolean |
| 22 | Show questions to all | Boolean |
| 23 | Automatic session recording | Boolean |
| 24 | Video recording | Boolean |
| 25 | Display attendee list to all | Boolean |
| 26 | Use Emoji reactions | Boolean |

**Note:** the list-page filter sidebar additionally offers *Post Webinar Re-direction*, *Send Follow-up
Email to Attendees* and *Send Follow-up Email to Absentees*, which the Fields tab does not list.
The create form also carries *Webinar Owner*, *Webinar Cost* and *Repeat Webinar*, likewise absent
from the Fields tab. See open questions.

### B.2 Every create-form control, one table

| Section | Field | Type | Mandatory | Default |
|---|---|---|---|---|
| Webinar Details | Webinar title | Single-line text | **Yes** | Empty |
| Webinar Details | Webinar Type | Picklist | No | Live Webinar |
| Webinar Details | Webinar Date & Time (date) | Date input | No | Today |
| Webinar Details | Webinar Date & Time (time) | Picklist | No | 10:00 AM |
| Webinar Details | Webinar Date & Time (timezone) | Picklist | No | (-6) Central |
| Webinar Details | Webinar Duration (hours) | Picklist | No | 1 hr |
| Webinar Details | Webinar Duration (minutes) | Picklist | No | 00 min |
| Webinar Details | Webinar Owner | Picklist + lookup | No | Rao Priya |
| Webinar Details | Organizer | Picklist | No | Jayasuriya |
| Webinar Details | Co-Organizer | Picklist | No | None |
| Webinar Details | Repeat Webinar | Button + dialog | No | None |
| Webinar Details | Webinar Cost | Text, `$` prefix | No | Empty |
| Webinar Details | Description | Multi-line text | No | Empty |
| Webinar Details | Registration Mode | Picklist | No | Register and attend each event individually (recurrence only) |
| Registration Setup | Open Registration for | Picklist | No | All Webinars (recurrence only) |
| Registration Setup | Registration Type | Picklist | No | With Registration |
| Registration Setup | Registration Form | Picklist | No | Default Form |
| Registration Setup | Moderation Type | Picklist | No | Automatic Moderation |
| Registration Setup | Set Registration Limit | Text (number) | No | Empty |
| Registration Setup | Push Webinar Registrants to CRM | Checkbox | No | Off |
| Registration Setup | Allow/deny registrants from specific countries | Picklist | No | No Restrictions |
| Registration Setup | Select Allowed Countries | Multi-select | No | Empty (conditional) |
| Registration Setup | Allow/Block Specific Domains | Picklist | No | No Restriction |
| Registration Setup | Add Allowed Domains | Multi-entry | No | Empty (conditional) |
| Registration Setup | Post_Registration Custom Redirection | Text (URL) | No | Empty |
| Registration Setup | Post Redirection URL | Text (URL) | No | Empty (conditional) |
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
| Reminders | 2nd Reminder Template | Template picker | No | — (hidden while None) |
| Reminders | 3rd Reminder | Picklist | No | None |
| Reminders | 3rd Reminder Template | Template picker | No | — (hidden while None) |
| Follow-Ups | Send Follow-up Email to Attendees | Picklist | No | 2 mins after the webinar ends |
| Follow-Ups | Attendees Follow-up Template | Template picker | No | Attendees Follow-up Template |
| Follow-Ups | Send Follow-up Email to Absentees | Picklist | No | 2 mins after the webinar ends |
| Follow-Ups | Absentees Follow-up Template | Template picker | No | Absentees Follow-up Template |
| Follow-Ups | Include Recording for Attendees | Checkbox | No | Off |
| Follow-Ups | Include Recording for Absentees | Checkbox | No | Off |

### B.3 Integration settings fields

| Section | Field | Type | Default |
|---|---|---|---|
| Connection | Email | Read-only text | Signed-in Webinar account |
| Connection | Organisation | Dropdown | First of the admin's orgs |
| Connection | Sync past webinars? | Dropdown (Yes/No) | **Yes** |
| Invite Modules | Module selection | Grouped checkboxes + chips | Leads, Contacts, Custom Module 1 |
| Deal Attribution | Enable Deal Revenue Attribution | Toggle | **On** |
| Deal Attribution | Revenue Attribution Type | Card radio, 6 options | **Linear** |

## Appendix C — Open questions and assumptions

Every item below is something the mock does not settle. Owner column: **PM** = product decision,
**Design** = interaction/copy decision, **Eng** = implementation/data decision.

### C.1 Blocking — these change what gets built

| # | Question | Why it matters | Owner |
|---|---|---|---|
| 1 | Recordings is empty on every record, including a completed webinar with *Automatic session recording* on. Where does a recording come from, and when? | The Attendees and Absentees Follow-up template types **require** a Recording Link. If no recording exists, either the required-link rule or the follow-up cannot work. | PM + Eng |
| 2 | Setup ▸ Templates lists **seven** templates, Module Preferences lists **eight** with different names for two of them. Which is the real set, and which names are canonical? | Two lists, two names for the same email, and a *Meetings Cancelled Template* that only one list knows about. | PM |
| 3 | Why is *Customise Template* disabled on **Meetings Cancelled Template**? | Either a permission rule, a not-yet-built screen, or a template that should not be here at all. | PM |
| 4 | Saving a new template returns to the list but the template does not appear, with no toast. Is the list meant to refresh, and what confirms the save? | A save with no visible result reads as a failure to the user. | Design + Eng |
| 5 | The *Registration Form* picklist on the create form (Default Form, Real Estate Form, Stock Trading Form) does not match the forms configured under Module ▸ Registration Form (Leads form, Contacts). Which list is authoritative? | Decides whether the picklist is driven by module configuration or is separate. | Eng |
| 6 | The Fields tab omits *Webinar Owner*, *Webinar Cost*, *Repeat Webinar*, *Post Webinar Re-direction* and both follow-up offsets, which the create form and list filters do use. Are these module fields? | Decides the data model. Webinar Cost in particular drives the whole ROI panel. | Eng |
| 7 | On-demand records have **no** Send Invite and **no** Polls, Recordings or Session Files. Intended, or unpopulated? | An on-demand webinar *is* a recording, so a missing Recordings list looks wrong. | PM |
| 8 | The mock does not model an on-demand webinar before anyone has watched it. Is there such a state, and what does the record show? | Section 7 currently documents only the with-attendance case. | PM |

### C.2 Data and calculation

| # | Question | Evidence | Owner |
|---|---|---|---|
| 9 | The ROI tiles do not reconcile with the tables: Revenue (Won) reads **$16,800** while the seven Deals Won rows sum to **$16,000**. | Figures 17–18 | Eng |
| 10 | **Deals in Pipeline** contains *Closed Won* (100%) and *Closed Lost* (0%) rows. | Figure 19 | PM + Eng |
| 11 | Are *Increasing Time Decay* and *Decreasing Time Decay* described the right way round? The UI says Increasing gives more credit to **earlier** webinars. | §2.6 | PM |
| 12 | How is *Attend. Rate* computed — attendees ÷ registrations, or ÷ approved registrations? Mock rows give 77%, 76%, 71%. | §4.1 | Eng |
| 13 | Where do the source-tracking Visited and Registered counts come from, and how do they relate to the Registration by Source chart? | §4.3 | Eng |
| 14 | The Invited related list is badged **100** but returns five rows, and the list footer says *Total Records 12* for six rows. | §4.1, §4.2 | Eng |

### C.3 Interaction and copy

| # | Question | Evidence | Owner |
|---|---|---|---|
| 15 | The **Waiting for Approval → View →** link does nothing. Where should it go — the Unapproved Registrants tab? | §4.2 | Design |
| 16 | Case 5 (Trial Expired) offers no action, only ×. Should it carry an upgrade link? | §2.3 | Design + PM |
| 17 | What does **Notify Super Admin** actually do, and what does the user see afterwards? | Case 4 | PM |
| 18 | What happens on **Deactivate** in the enabled state — is there a confirmation, and what happens to existing records? | §2.7 | PM |
| 19 | Does *Allow anonymous questions* depend on *Allow attendees to ask questions*? The mock does not enforce it. | §3.4 | Design |
| 20 | After saving a webinar, where does the user land and what confirms the save? | §3.7 | Design |
| 21 | The list filter sidebar is headed **"Filter Invoices by"**. | §4.1 | Design |
| 22 | The *Hide Details* panel shows static placeholder values on every record. | §4.2 | Eng |
| 23 | The module dropdown in Setup ▸ Templates omits **Leads**, though Leads templates exist in the list. | §8.1 | Eng |
| 24 | The Templates page **Search Template** and the Modules page search box are both inert. | §8.1, §8.6 | Eng |

### C.4 Assumptions this document makes

These are stated so they can be corrected, not treated as requirements:

1. **The DEMO case switcher is a mock affordance**, not a product control; Cases 1–5 are the outcomes
   of an account lookup at the moment *Enable Integration* is pressed.
2. **Webinar Category is derived, not entered.** No control sets it; it follows from Webinar Type and
   whether the session has happened.
3. **Which follow-up a registrant receives is decided by their Webinar Status** (Attended → Attendees
   Follow-up, Not Attended → Absentees Follow-up).
4. **Co-Organizer is multi-value**, because detail pages show two co-organisers while the create form
   offers a single-select.
5. **Registration Mode and Open Registration for are recurrence-only**, appearing once Repeat Webinar
   is set.
6. **A recurring webinar produces one record per occurrence**, since the mock's two *Recurrent Webinar*
   rows have separate dates and registration counts.
7. **The required-link validation message is templated** from the type name and required link, so all
   seven types produce the same sentence with different nouns.

