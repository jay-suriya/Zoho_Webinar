# 03 — Create Webinar: the form and everything inside it

**Where it starts:** the **Create Webinar** button on the list page.

Five sections in a single scroll — **Webinar Details**, **Registration Setup**,
**Preferences**, **Reminders**, **Follow-Ups**. **63 fields in total; 42 render in the default
configuration.** The rest are revealed by the branches below.

**Only one field is required: Webinar Title.** Saving without it is refused and the field is
marked. Nothing else blocks a save.

---

## The two branches that restructure the form

Everything else in this file hangs off these.

| Picklist | Values | Effect |
|---|---|---|
| **Webinar Type** | `Live Webinar` *(default)* / `OnDemand Webinar` | what the session *is* |
| **Registration Type** | `With Registration` *(default)* / `Without Registration` | whether registrants exist at all |

Remember: **not visible means not rendered.** Switching a branch removes fields from the DOM.

> Switching a branch must clear every dependent control belonging to the previous one, not
> merely hide the row it sat in. A value typed into a field that is then hidden must not
> silently survive into the saved record.

---

## Webinar Details

In flow order. `L` = Live + With Registration, `W` = Live + Without Registration,
`O` = On-Demand.

| Field | Type | Req | Default | L | W | O |
|---|---|---|---|---|---|---|
| Webinar Title | Text | **Yes** | placeholder `Enter webinar title` | ✓ | ✓ | ✓ |
| Webinar Type | Picklist | No | `Live Webinar` | ✓ | ✓ | ✓ |
| Webinar Date & Time | Date input + time picklist | No | today, `10:00 AM` | ✓ | ✓ | ✓ |
| Webinar Duration | Compound picklist, hours + minutes | No | `1 hr` + `00 min` | ✓ | ✓ | — |
| Video File | Picklist (source chooser) | No | — | — | — | ✓ |
| Webinar Timezone | Picklist | No | `(-6) Central` | ✓ | ✓ | ✓ |
| Allow video play/pause | Checkbox | No | checked | — | — | ✓ |
| Webinar Owner | Picklist w/ search + user-lookup button | No | `Rao Priya` | ✓ | ✓ | ✓ |
| Organizer | Picklist w/ search | No | `Jayasuriya` | ✓ | ✓ | ✓ |
| Repeat Webinar | Custom control → modal | No | off | ✓ | ✓ | — |
| Co-Organizer | Picklist w/ search | No | `None` | ✓ | ✓ | — |
| Webinar Cost | Text, `$` prefix, info icon | No | placeholder `0.00` | ✓ | ✓ | ✓ |
| Description | Textarea | No | empty | ✓ | ✓ | ✓ |

### Options, verbatim

```
Webinar Type        Live Webinar · OnDemand Webinar
Webinar Date & Time 9:00 AM · 10:00 AM · 11:00 AM · 12:00 PM · 1:00 PM · 2:00 PM
Webinar Duration    hours: 1 hr … 24 hr        minutes: 00 min · 15 min · 30 min · 45 min
Video File          From Zoho Webinar Recordings · Upload Files / Documents ·
                    Zoho WorkDrive · Other Cloud Services
Webinar Timezone    (-5) Eastern · (-6) Central · (-7) Mountain · (-8) Pacific ·
                    (+0) UTC · (+5:30) IST
Webinar Owner       Rao Priya · Jay Acme · Mark Acme · Suriya
Organizer           Jayasuriya · Morrison Troy
```

> The Owner and Organizer option lists are placeholders standing in for real user directories.
> The *fact that they are two different directories* is the specification; the names are not.

### Webinar Owner and Organizer are different things

**Owner is a CRM concept.** Every CRM record has one, and it drives record-level sharing,
assignment rules and "My Webinars" filters. **Organizer is the webinar's host** — the person
who actually runs the session. Separate fields, separate directories, and they must not be
collapsed into one.

Both use the same shell: a picklist whose dropdown has a **sticky search box** at the top
filtering the options, with an empty state when nothing matches. Owner additionally has a
user-lookup icon button beside the field.

> The search box must stop click and keydown from propagating. Without that, typing in it
> reaches the picklist trigger behind and closes the dropdown on the first keystroke.

> A dropdown containing a search box needs a minimum width of its own (~230px). Inheriting the
> narrow width of its trigger clips the search field to something like `Search u…`.

### Webinar Cost

`$` prefix inside the field, an info icon at the right. Tooltip, verbatim:

> "This is the amount attendees will be charged to register for this webinar."

**This field is the denominator of every ROI figure in file 05.** A cost of `2500` produces
Cost `$2,500`, ROI `+572%`, Cost/Attendee `$167`, Revenue/Attendee `$1,120`.

> **The tooltip and the ROI panel contradict each other** — one says revenue charged to
> attendees, the other treats it as expenditure. This is blocking; see file 07. The `$` is
> hard-coded and the field has no numeric validation, which also needs resolving.

### Repeat Webinar → modal

Opens its own modal. Fields:

| Field | Options |
|---|---|
| Repeat Type | *(recurrence pattern)* |
| Repeat Ends | `On` *(a date)* / `After` *n* `Webinars` |
| Registration Mode | `Register and attend each event individually` · `Register once and attend any event` |
| Open Registration for | `All Webinars` · `Only selected number of occurrences` → `1`–`6 occurrences` |

**Registration Mode is the one that matters downstream.** *Register once and attend any event*
means one registrant record spans every occurrence; *individually* means a registrant per
occurrence. That changes what the Invited and registrant lists contain for a recurring series.

A recurring webinar appears in the list view as **one row per occurrence**.

### Co-Organizer

A plain picklist with search — **the same control as Organizer**, with two differences: the
default is `None`, and `None` is in the option list.

> **Read this before changing this field.** It has been rebuilt four times: as a tabbed
> dropdown, as a modal, as a chips-and-action control, and finally as a copy of Organizer. Each
> round treated the new instruction as an addition rather than a correction. The brief was "a
> picklist with search, like Organizer". **When a request names an existing control to copy,
> copy it and stop.**
>
> A richer multi-select panel — two source directories, invite-by-email with `+`/`−` rows,
> duplicate detection across both halves — was built and then deleted. If multi-select
> co-organisers come back as a requirement, that history is in the repo, but it is not what
> this spec asks for.

---

## Registration Setup — `With Registration`

| Field | Type | Req | Default | L | W | O |
|---|---|---|---|---|---|---|
| Registration Type | Picklist | No | `With Registration` | ✓ | ✓ | ✓ |
| Registration Form | Picklist | No | `Default Form` | ✓ | — | ✓ |
| Customize Registration Page | Picklist | No | `Standard Template` | ✓ | — | ✓ |
| Moderation Type | Picklist | No | `Automatic Moderation` | ✓ | — | ✓ |
| Set Registration Limit | Text | No | empty | ✓ | — | ✓ |
| Push Webinar Registrants to CRM | Checkbox + `Manage Config` | No | **unchecked** | ✓ | — | ✓ |
| Allow/deny registrants from specific countries | Picklist | No | `No Restrictions` | ✓ | ✓ | ✓ |
| Select Allowed Countries | Multi-select | No | — | *revealed* | *revealed* | *revealed* |
| Allow/Block Specific Domains | Picklist | No | `No Restriction` | ✓ | — | ✓ |
| Add Allowed Domains | Text | No | — | *revealed* | *revealed* | *revealed* |
| Post_Registration Custom Redirection | Text | No | placeholder `https://` | ✓ | — | ✓ |
| Post Redirection URL | Text | No | — | *revealed* | *revealed* | *revealed* |
| Allow access to join link only through mail | Checkbox | No | **checked** | ✓ | — | ✓ |
| Allow only authenticated Zoho Users with a Zoho account | Checkbox | No | unchecked | ✓ | ✓ | ✓ |
| Send Confirmation to Registrants | Checkbox | No | **checked** | ✓ | — | ✓ |
| Confirmation Email Template | Template picker | No | `Webinar Confirmation Template` | ✓ | — | ✓ |

*revealed* = rendered only once its parent field is set to a value that needs it.

```
Registration Type     With Registration · Without Registration
Registration Form     Default Form · Real Estate Form · Stock Trading Form · + Create New Form
Customize Reg. Page   Standard Template · Custom Created
Moderation Type       Automatic Moderation · Manual Moderation
Countries             No Restrictions · Allow registrants from Countries ·
                      Block registrants from Countries
Domains               No Restriction · Allow specific email domains ·
                      Block specific email domains
```

**Moderation Type matters downstream:** *Waiting for Approval* on the record's summary band
(file 04) only means anything under `Manual Moderation`.

### Registration Form vs Customize Registration Page

Two adjacent picklists in the same column, and they are constantly confused:

- **Registration Form** — *which fields are collected* from a registrant.
- **Customize Registration Page** — *how the public page looks*.

**Registration Form.** Each option row reveals a **Preview** tag on hover, opening the form
builder's preview. `+ Create New Form` is the last option and **opens a form builder rather
than selecting anything** — a create action living inside a picklist.

**Customize Registration Page.** Each option reveals an **eye icon on hover** which opens a
full-screen preview of the public registration page. The eye must call `stopPropagation` — it
previews, it does not select the option.

The preview renders the page as a registrant sees it, and **reads the title, date and time
currently on the form**, so it reflects the webinar being created rather than fixed sample
text. It has a desktop/mobile toggle; mobile narrows the card to 420px and stacks its two
columns.

Field sets per option:

| | Standard Template | Custom Created |
|---|---|---|
| First Name | required | required |
| Last Name | required | required |
| Email Address | required | required |
| Phone Number | — | required |
| Company | — | optional |
| Portfolio Size | — | optional |

**The row follows Registration Form's visibility** — `Without Registration` removes it, since
there is no registration page to customize.

### Push Webinar Registrants to CRM

Checkbox plus a **Manage Config** link beside the label. **Off by default.**

**This is the field that closes the loop.** Somebody who registers from the public link —
found the webinar on LinkedIn, was forwarded it, arrived from a tweet — does not exist in CRM.
Ticked, they are created as CRM records automatically and the re-import step disappears.

**Manage Config** opens the field mapping: which registration-form field lands in which CRM
field, and which module the new record is created in.

> It ships **unchecked**, which leaves the loop open unless somebody closes it. Given this is
> the single feature that most justifies the whole integration, that default is worth
> challenging — file 07.
>
> **Deduplication is not modelled at all.** When a registrant's email already matches a Lead or
> Contact, whether the existing record is updated, a duplicate created, or the registrant
> skipped is unspecified. Blocking; file 07.

---

## Registration Setup — `Without Registration`

Choosing it **removes the entire registration apparatus** — every field above except
Registration Type — and reveals three others:

| Revealed | Type | Options | Why |
|---|---|---|---|
| Who can Join | Picklist | `Anyone can Join` · `Only Authenticated Users can Join` | with no registrant list, access is decided here |
| Send thank you email to attendees | Picklist | `2 minutes after webinar ends` · `5 mins after webinar ends` · `10 mins after webinar ends` | replaces the confirmation/reminder chain |
| Thank You Email Template | Template picker | — | its template |

**It also removes the whole reminder and follow-up chain** — 1st/2nd/3rd Reminder and their
templates, both Follow-ups and their templates, and both Include Recording settings. Those
emails address a *registrant*, and there are none. Only the thank-you survives.

---

## Preferences, Reminders and Follow-Ups

| Field | Type | L | W | O |
|---|---|---|---|---|
| Allow attendees to ask questions | Checkbox | ✓ | ✓ | ✓ |
| Allow anonymous questions | Checkbox | ✓ | ✓ | — |
| Show questions to all | Checkbox | ✓ | ✓ | — |
| Auto Reply for questions | Checkbox | *revealed* | *revealed* | *revealed* |
| Automatic session recording | Checkbox | ✓ | ✓ | — |
| Video recording | Checkbox | ✓ | ✓ | — |
| Display attendee list to all | Checkbox | ✓ | ✓ | — |
| Use Emoji reactions | Checkbox | ✓ | ✓ | — |
| Post webinar Re-direction | Checkbox | ✓ | ✓ | ✓ |
| 1st Reminder | Picklist | ✓ | — | — |
| 1st Reminder Template | Template picker | ✓ | — | — |
| 2nd Reminder | Picklist | ✓ | — | — |
| 2nd Reminder Template | Template picker | *revealed* | — | — |
| 3rd Reminder | Picklist | ✓ | — | — |
| 3rd Reminder Template | Template picker | *revealed* | — | — |
| Send Follow-up Email to Attendees | Picklist | ✓ | — | — |
| Send Follow-up Email to Absentees | Picklist | ✓ | — | — |
| Attendees Follow-up Template | Template picker | ✓ | — | — |
| Absentees Follow-up Template | Template picker | ✓ | — | — |
| Include Recording for Attendees | Checkbox, unchecked | ✓ | — | — |
| Include Recording for Absentees | Checkbox, unchecked | ✓ | — | — |

*Auto Reply for questions* is revealed by *Allow attendees to ask questions*.

### Reminder intervals — exact lists

**1st Reminder** — 11 options, default `15 mins before the webinar`, **no None**:

```
2 mins · 5 mins · 10 mins · 15 mins · 30 mins · 1 hour · 2 hours · 6 hours · 12 hours ·
1 day · 1 week      — all suffixed "before the webinar"
```

**2nd and 3rd Reminder** — 12 options: **`None`** plus the same eleven. **Both default to
`None`.**

**That is how a webinar sends fewer than three reminders.** There is no separate "number of
reminders" setting. And because the 1st has no `None`, **at least one reminder always goes out
on a registration webinar**.

### Follow-up intervals

**Send Follow-up to Attendees / Absentees** — 9 options each, default
`2 mins after the webinar ends`:

```
None · 2 mins · 5 mins · 10 mins · 15 mins · 1 hour · 2 hours · 6 hours · 1 day
       — all suffixed "after the webinar ends"
```

Note the gaps: there is no 30 mins and no 12 hours here, unlike the reminder list. Use the
list as written.

### Template slots

Every reminder and follow-up has its own template slot, chosen through a **Select Template**
dialog. The slot shows the chosen template's name as a preview link beside the button.

The dialog lists only templates of the matching type (file 06), and offers **+ Create
Template**, which hands off to Zoho Webinar's own editor rather than CRM's. File 06 covers
what comes back.

---

## Layout notes that were got wrong once

- **Webinar Timezone needs its own row with a label.** It was stacked under the date+time box
  inside the same form group, which left it with no label at all and floated the "Webinar Date
  & Time" label vertically between two controls. Give it a row, with an empty right-hand cell
  so the label column keeps the width every other row uses.
- **On-demand: `Allow video play/pause` belongs in the Timezone row's empty right cell**, so
  the right column reads **Video File → Allow video play/pause → Organizer**. It previously sat
  in a row of its own two rows below the file it governs.
- **Check row spacing after any structural change.** Comparing the top of consecutive rows is
  the quick test; a gap means something above closed early.

---

## Saving

**Webinar Title empty → refused**, field marked, nothing else happens. It is the only
validation on the form.

On success the record is created with `Webinar Category = Scheduled Webinar` and the user
lands on its record page (file 04).

> There is no Cancel or discard modelled on this form. File 07.
