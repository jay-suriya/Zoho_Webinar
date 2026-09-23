# 06 — Lifecycle emails and their templates

Eight emails surround a webinar. Each is a **template type**, and the type decides two things:
which links the template may carry, and which link it **must** carry. Get those rules wrong and
you ship an invitation nobody can register from.

**Out of scope:** CRM's email template editor itself. You are adding template *types* and their
rules, not a new editor.

---

## The eight emails

| # | Email | When it goes out | To |
|---|---|---|---|
| 1 | **Webinar Invitation** | when you invite CRM records | CRM records — *before anyone has registered* |
| 2 | **Confirmation Email** | the moment somebody registers | the registrant |
| 3 | **1st Reminder** | at the interval set on the webinar | registrants |
| 4 | **2nd Reminder** | ditto | registrants |
| 5 | **3rd Reminder** | ditto | registrants |
| 6 | **Attendees Follow-up** | after the session | everyone who attended |
| 7 | **Absentees Follow-up** | after the session | registrants who did not turn up |
| 8 | **Webinar Cancelled** | if the webinar is called off | registrants |

**The invitation is the odd one out, and the reason matters.** It goes to a CRM record *before
that person is a registrant*, so it cannot merge registrant fields and cannot carry a Join URL
— there is no registration to join yet. Everything from the confirmation onwards addresses a
registrant and can.

**6 and 7 are a partition of the registrants**, decided by attendance. Every registrant gets
exactly one of them.

---

## Link rules — the part to get right

**`TPL_TYPE_LINKS` — which links a type may insert.** Insert Link and Insert Button offer only
these, per type:

| Type | Allowed links |
|---|---|
| **Webinar Invitation** | Web URL, Email, **Registration Link**, Add To Calendar, Add To Google Calendar, Add To Yahoo Calendar, Add To Outlook Calendar, Add To Zoho Calendar |
| **Confirmation Email** | Web URL, **Join URL**, Cancel Registration, + all five calendar links |
| **1st / 2nd / 3rd Reminder** | Web URL, **Join URL**, Cancel Registration, + all five calendar links |
| **Attendees Follow-up** | Web URL, Join URL, **Recording Link**, + all five calendar links |
| **Absentees Follow-up** | Web URL, Join URL, **Recording Link**, + all five calendar links |
| **Webinar Cancelled** | **Web URL, Email — and nothing else** |
| **None** | everything: Web URL, Email, Registration Link, Join URL, Cancel Registration, Recording Link, + all five calendar links |

The five calendar links are always: `Add To Calendar`, `Add To Google Calendar`,
`Add To Yahoo Calendar`, `Add To Outlook Calendar`, `Add To Zoho Calendar`.

**`TPL_REQUIRED_LINK` — what a type must contain, enforced on save:**

| Type | Required link |
|---|---|
| Webinar Invitation | **Registration Link** |
| Confirmation Email | **Join URL** |
| 1st Reminder | **Join URL** |
| 2nd Reminder | **Join URL** |
| 3rd Reminder | **Join URL** |
| Attendees Follow-up | **Recording Link** |
| Absentees Follow-up | **Recording Link** |
| Webinar Cancelled | *(none)* |
| None | *(none)* |

**Saving a template that lacks its required link is refused.** That is the only content
validation on a template.

### Why the rules are shaped this way

- **The invitation gets Registration Link and not Join URL** because its reader has not
  registered. Offering a join link to somebody with no registration is a dead end.
- **Confirmation and reminders get Join URL and Cancel Registration** because their reader *has*
  registered — they can join, and they can change their mind.
- **Follow-ups get Recording Link** because the session is over; the only thing left to offer is
  the recording. They keep Join URL as an allowed link, but it is not what they are for.
- **Webinar Cancelled gets almost nothing.** There is nothing to join, register for or watch.
  Two links only.

---

## Merge fields

`#` in the editor opens the merge-field picker. Its **source list depends on the type**:

**Webinar Invitation** offers, in order:

```
Webinar Details · Users · Organization        (+ the recipient module's own fields)
```

**Every later email adds `Registrations` above Webinar Details**, because it addresses a
registrant rather than a CRM record:

```
Registrations · Webinar Details · Users · Organization
```

### The sources, verbatim

**Webinar Details** — `Webinar Title`, `Webinar Date & Time`, `Webinar Organiser`,
`Webinar Duration`, `Description`

**Registrations** — `Registration Id`, `Country`, `Created By`, `Created Time`, `Email`,
`First Name`, `Modified By`, `Timezone`, `Add To Google Calendar`, `Add To Yahoo Calendar`,
`Add To Outlook Calendar`, `Add To Zoho Calendar`, `Add To Calendar`, `Join URL`, `Handouts`,
`Cancel Registration`, `Audio Details`, `Registration URL`, `Full Name`, `Last Name`,
`Abuse Email`, `iOS app URL`

**Users** — `User Id`, `User Name`, `Email`, `Role`, `Profile`

**Organization** — `Company Name`, `Website`, `Phone`, `Street`, `City`, `State`, `Country`

**General** — `Current Date`, `Current Time`, `Unsubscribe Link`, `View in Browser`

Recipient-module sources carry that module's own fields — Leads offers `Lead Id`,
`Lead Owner`, `Company`, `First Name`, `Last Name`, `Title`, `Email`, `Phone`, `Mobile`,
`Lead Source`, `Industry`, `City`, `State`, `Country`; Contacts offers the equivalent with
`Account Name`, `Department` and mailing address fields.

### Templates are module-scoped

**An email template belongs to a module, and its merge fields resolve against that module's
record.** A template's module must therefore match its recipient's module. This is standard CRM
behaviour and it is why the invitation's merge sources include the recipient module while the
later emails lead with Registrations.

> Known gap in the mock: the merge-source list leads with `Registrations` for anything whose
> type is not Webinar Invitation, **including plain non-webinar templates**, so a Contacts
> template offers registrant fields rather than the module's own. Scope the Registrations
> source to webinar template types only.

---

## Where templates live

**Setup ▸ Templates** lists them under the **Zoho Webinar** module. The webinar's default set
also appears under **Modules and Fields ▸ Zoho Webinar ▸ Preferences**.

### The list

Eight shipped rows, one per lifecycle email, **in lifecycle order with Webinar Cancelled
last** — it only goes out if the webinar is called off, so it belongs at the end rather than
at the top.

Each row's subline carries the module, what the email is for, and its type as a third segment:

```
Zoho Webinar · Sent when you invite CRM records to a webinar · Invitation template
```

**The Email Type is a segment of that subline, not a column.** A column that exists for one
module leaves a hole in the table for every other module. Non-webinar rows simply have no third
segment.

> This means there is no way to filter the list by email type. A filterable Email Type column
> was built and removed for the reason above. If filtering comes back as a requirement, solve it
> without a module-specific column.

### One row per lifecycle email

**Selecting a template for a use case renames the existing row; it never adds a second.** Pick
"Long-form invite" for the invitation and the Invitation row becomes *Long-form invite ·
Invitation template*. Pick the Default back and it returns to *Webinar Invitation Template*.
The count stays eight.

> Getting this wrong produces two rows for one email — the shipped row and the custom you just
> chose — which reads as though both are live. The row stands for *the email*, not for *a
> template*.

A consequence to know: **a custom template that is saved but not currently live has no row of
its own.** The list is a view of what each email is set to; the templates themselves live in the
gallery.

### Row actions

- **Clicking the name** opens a read-only **preview** (with Preview / Analytics tabs).
- **A pencil icon appears on row hover**, in the column just before the type segment, and opens
  that template in the editor.
- The **shipped defaults are read-only** and have no pencil — their pencil opens **Zoho
  Webinar's own editor in a new tab** instead (below).

---

## Creating a template

**Setup ▸ Templates → + New Template** branches on the module filter:

| Filter | Opens |
|---|---|
| **Zoho Webinar** | the **Email Notification gallery** — a rail of the eight lifecycle emails, each with its Default, its saved customs, and the Basic layouts |
| anything else *(including All Modules)* | the standard **Create Email Template** dialog |

The gallery's rail entry sets the use case, which stamps the type, which sets the required link
and the allowed link list from the start.

### The Create Email Template dialog

For non-webinar modules: **Select Module** first. When the module is **Zoho Webinar**, an
**Email Type** row appears beneath it — the type means nothing for an ordinary module, so it is
revealed rather than always shown. Its options are the eight lifecycle emails, labelled as the
list labels them.

**Next** carries the choice through: the gallery opens on that use case with its rail entry,
chip and note, and the type is stamped before the editor opens.

> The field is called **Email Type**, not "Template Type" — it names *which lifecycle email
> this is*, and "Template Type" restated the noun already in the dialog title.

### New templates start blank

Name and subject are **real, empty inputs** with placeholders `Untitled template` and
`Add a subject` — not prefilled with the type name or an invented "Webinar Invite - <Module>".

**Saving with no name is refused inline in the Save dialog** — not as a toast, because the
editor's toast renders behind that modal's scrim.

The Save dialog asks **Template Name** and **Save To**, a folder picklist of the real CRM
template folders with a separated **+ New Folder** row that takes a name inline. **A folder is
required**; saving without one is refused the same way.

> The body's "Write the … email here" prompt must be a real CSS placeholder, not grey content.
> As content, typing merges into it and it gets saved into the email.

---

## Creating a template from a create-webinar slot

`+ Create Template` inside a slot's Select Template dialog **does not open CRM's gallery**. It
opens **a new tab on Zoho Webinar's own domain** — its Email customization screen, showing the
rail of six lifecycle emails with that slot's email in bold, the Quick Templates Default, any
customs already saved for it, and the Basic layouts.

**Save hands the template back and closes the tab**: the child calls back into the opener with
the new template's name and slot, which pushes it into the created set, adds a Setup ▸ Templates
row with its Email Type, selects it for the slot, and reopens the picker on it. Then the child
closes itself.

> The child is same-origin, which is what makes the callback possible.
>
> **Never use `alert()` on the pop-up-blocked path.** A modal dialog freezes the whole renderer
> until somebody dismisses it by hand — it has cost a frozen tab here. Use a toast.

The Select Template dialog's folder dropdown is a **static "Zoho Webinar" label with no caret**
— every template it lists is a webinar template, so there is nothing to filter.

---

## What a created template must be able to reach

A template created anywhere must be selectable everywhere it is valid. Specifically: one
created inside the Send Invite flow must appear in the Select Template picker **in the step that
created it**. Push it into the Templates list at creation, not only into the editor's own state.
