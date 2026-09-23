# 02 — The integration: marketplace, the gate, the wizard

Turning the feature on. Done once, by an admin. **Nothing in the Zoho Webinar module exists
until this completes** — the module is not in the left rail, the list view is unreachable, and
no webinar can be created.

Two of the four wizard steps set values that change how the rest of the product behaves, which
is why they get their own sections below.

---

## Where it starts

`Setup → Marketplace → Zoho → the Zoho Meetings card → For webinars › Set up`

The Zoho Meetings card carries two halves — **For webinars** and **For online meetings** —
each with its own `Set up` button, and a note reading *"One Zoho Meetings login connects both.
Set up one or both independently."* You are building the webinars half only. The meetings half
already exists; leave it alone.

---

## The account gate — this comes first

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

## The introduction page

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

## The wizard

**Setup** opens a four-step wizard. Each step has **Cancel** and **Next**.

| Step | Asks | Control | Default |
|---|---|---|---|
| 1 | Email + Organisation | Text / picklist | the signed-in user's |
| 2 | Sync past webinars? | **Radio pair, Yes / No** | **Yes** |
| 3 | Who Can Participate From CRM | Checkbox list | Leads + Contacts, locked on |
| 4 | Webinar Deal Attribution | Card select, six models | **Linear** |

**Step 4's Next button reads `Enable Integration`**, because it is the last one. Pressing it
turns the integration on and lands on the enabled page.

### The steps accumulate

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

### Step 2 is radios, not a picklist

A binary question behind a click is a binary question with one answer hidden. It was a
dropdown; it is now a **Yes / No radio pair with Yes preselected**.

> Keep a hidden input carrying the `yes`/`no` value if your form serialisation wants one — and
> keep the radios and that value in step when the answer is set programmatically.

---

## Step 3 — Who Can Participate From CRM

**The single most load-bearing setting in the integration.** It is the list of CRM modules
whose records may be invited to a webinar, and it drives the module dropdown in Send Invite
(file 04). **Turn a module off here and it disappears there.** Nothing else in the product
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

### Why this list and not CRM's full module list

**Every module here is a person** — someone who can hold an email address and occupy a seat.
Accounts, Potentials, Cases, Campaigns and Meetings were deliberately removed: a company, a
deal, a ticket, a campaign and an event cannot attend a webinar. Any module added here in
future must pass the same test.

The names are what a business calls the people it holds, which is why the list runs past the
standard modules into Donors, Volunteers, Students, Alumni, Patients and Subscribers — a
non-profit, a university, a clinic and a subscription business all build a module like that.

### The heading is intent, not mechanism

Mechanically this gates who can be **invited**, not who can **attend** — anyone holding the
public registration link can still register. The section is called *Who Can Participate From
CRM* as a statement of intent. Its subline names the consequence rather than restating the
heading:

> Choose which CRM modules your participants can come from. Turn a module off and its records
> can no longer be added to a webinar.

**The word "invite" is deliberately absent from both.** Do not reintroduce it.

---

## Step 4 — Webinar Deal Attribution

A contact usually attends more than one webinar before a deal closes. This decides how that
deal's revenue is divided across them, and it is what makes the ROI figures in file 05 mean
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
> *earlier* webinars. Both are in file 07 as blocking. Do not invent a curve.

---

## The enabled page

After `Enable Integration`, the same three settings again — connection details, sync past
webinars, Who Can Participate From CRM, and Webinar Deal Attribution — now with a
**dirty-state Save bar** that appears when anything changes.

The sync answer from step 2 carries across to this page.

> Historically this page was missing the sync field entirely: the code that populated it looked
> for markup that never existed, so the function was a permanent no-op and the field simply did
> not appear after enabling. Make sure every setting from the wizard has a real control here.

**The Save bar has no specified success or failure state.** See file 07.
