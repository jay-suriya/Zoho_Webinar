# 08 — Decisions already made, and what was rejected

Read this before renaming anything or "improving" a label. Most of what follows looks
arbitrary until you know what it replaced.

---

## Naming rules

### 1. Keep the product's vocabulary in the label

If the user sees a phrase on the record, in the list view, in filters and on the calendar, the
control that acts on it must contain those words. A label that reads better in isolation and
leaves this screen as the only place in CRM calling the thing something else is worse, however
elegant.

### 2. Name the decision, not the data structure

**"Zoho Webinar Invite Modules" → "Modules You Can Invite" → "Who Can Participate From CRM".**

The first named the data structure. The second read as a category rather than a choice. The
third names the decision being made — *who is in the room, and that they come from CRM*.

The heading and subline then swapped jobs: the heading carries the intent, the subline the
mechanism.

> **The word "invite" is deliberately absent from that section's heading and subline.**
> Mechanically the setting gates who can be invited, but the section states intent. Do not
> reintroduce it.

### 3. Name what the button does, not what the page is about

**The introduction page's action reads `Setup`, not `Enable Integration`.** It does not enable
anything — it opens the wizard, and enabling happens at the end of that. The old label promised
an outcome one click too early.

### 4. "Email Type", not "Template Type"

The field names *which lifecycle email this template is*. "Template Type" restated the noun
already in the dialog's title.

---

## Structural decisions

### The account check belongs at the marketplace card

Originally the card always opened the introduction page and the account check ran on *that*
page's Setup button — so a user who could not have the integration was shown a page selling it
to them first. The check now runs before anything is rendered, with a second copy on the
introduction page's button as a guard.

### Wizard steps accumulate rather than replace

Replacing each step with the next meant a decision could not be re-read while the next one was
being made. Answered steps now stay on screen, and only the step in play shows its buttons — a
pair of buttons under a settled section suggests it is still open.

### The steps are shown and hidden in place, not routed

Deliberate: the final action reads every answer out of the DOM, so every earlier field has to
still exist at the end. If you rebuild this as a router, carry the answers in state instead.

### Who Can Participate lists only person-shaped modules

Accounts, Potentials, Cases, Campaigns and Meetings were removed: a company, a deal, a ticket,
a campaign and an event cannot attend a webinar. What replaced them are the modules a business
builds to hold *people* — Vendors, Donors, Volunteers, Members, Students, Alumni, Partners,
Speakers, Referrals, Patients, Subscribers.

**Any module added here in future must pass the same test.**

> Known consequence: the Send Invite module list is intersected with this one. A module present
> in one and not the other silently cannot be invited. Keep the two lists in step.

### Sync past webinars is radios, not a picklist

A binary question behind a click hides one of its two answers.

### Webinar Cancelled is listed last

It is the eighth row, after Absentees Follow-up, matching the order of the gallery's rail. The
list shows all eight lifecycle emails from the start, and the cancellation email sits at the end
because it only goes out if the webinar is called off.

Previously it had no row at all and appeared at the *top* the first time something was selected
for it, because new rows were unshifted.

### One row per lifecycle email

A row stands for *the email*, not for *a template*. Selecting a custom renames the row; it never
adds a second. Two rows for one email reads as though both are live.

### Email Type is a subline segment, not a column

A column that exists for one module leaves a hole in the table for every other module. The type
reads as the tail of the row's own subline instead, and non-webinar rows simply have no third
segment.

**This removed the ability to filter by email type.** That was the accepted cost.

### A new webinar has no registration sources

A brand-new webinar charts nothing, because it has no channels yet. The first source is created
by the first Send Invite. Seeding defaults would chart registrations from channels that do not
exist.

### On-demand: Allow video play/pause sits under Video File

Moved out of a row of its own so the right column reads **Video File → Allow video play/pause →
Organizer**, putting the setting next to the file it governs rather than two rows away.

---

## Rejected, with the reason

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

### The co-organiser field — four rounds, one lesson

It was built as a tabbed dropdown, then a modal, then a chips-and-action control, then a
multi-select panel, and finally deleted in favour of **a plain copy of the Organizer picklist**.

Each round treated the new instruction as an *addition* to the last reading rather than a
*correction* of it. The original brief was "a picklist with search, like Organizer".

> **When a request names an existing control to copy, copy it and stop.**

---

## Traps that cost real time

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

## The verification habit

Every structural change to a form or record page was checked three ways before being called
done, and the same habit will serve you:

1. **Row tops run contiguously** — no gap where a container closed early.
2. **The variant actually switched** — count the visible fields, do not assume the branch fired.
3. **The value survived the round trip** — read it back after the change, not before.
