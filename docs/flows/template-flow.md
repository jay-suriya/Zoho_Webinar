# Template flow — branch `templates-flow`

How an email template is browsed, created, edited and saved in the mock, and how the
four entry points converge on one editor. Derived from `webinar.html`; function names are
given so the chart can be checked against the code.

On this branch templates live in **Setup ▸ Templates**. (On `template-flow-fixes` they
live in the module instead, under Zoho Webinar ▸ Preferences — a different chart.)

## Browse, create, edit

```mermaid
flowchart TD
  classDef entry fill:#F0F1FF,stroke:#A3ACFF,color:#202123
  classDef screen fill:#FFFFFF,stroke:#C5C4D3,color:#202123
  classDef editor fill:#181B34,stroke:#181B34,color:#FFFFFF
  classDef gate fill:#FFF2F3,stroke:#FF4D5B,color:#202123
  classDef store fill:#E9FBF4,stroke:#19B171,color:#202123

  E1["Setup ▸ Templates<br/><i>openTemplatesPage()</i>"]:::entry
  E2["Modules and Fields ▸<br/>Zoho Webinar ▸ Preferences<br/><i>8 lifecycle rows</i>"]:::entry
  E3["Create Webinar form<br/><i>Confirmation · Reminders 1-3 ·<br/>Attendees / Absentees Follow-up</i>"]:::entry
  E4["Webinar ▸ Send Invite ▸<br/>Mass Email"]:::entry

  L1["Template list<br/><i>TPLPAGE_CREATED + TPLPAGE_ROWS<br/>+ TPLPAGE_WEBINAR_ROWS</i>"]:::screen
  PV["Preview (read-only)<br/><i>openTemplatePreview(key)</i>"]:::screen
  P3["Select Template<br/><i>openSlotTemplatePicker(slot)</i><br/>filtered to TPL_SLOT_TYPE[slot]"]:::screen
  P4["Select Template<br/><i>SelectTemplateModal</i><br/>invitation templates"]:::screen

  CT["Create Email Template<br/><i>Select Module + Template Type</i>"]:::screen
  GAL["Template Gallery<br/><i>Basic × 6 layouts</i>"]:::screen
  ED["Editor — name, subject,<br/>Insert Link, merge fields<br/><i>type-scoped</i>"]:::editor

  E1 --> L1
  L1 -- "click a name" --> PV
  PV -- "pencil" --> ED
  L1 -- "+ New Template" --> CT
  CT -- "Next" --> GAL

  E2 -- "Customise Template" --> PV

  E3 -- "Select Template" --> P3
  P3 -- "+ Create Template<br/>type implied, no module dialog" --> GAL

  E4 -- "Select Template" --> P4
  P4 -- "+ Create Template<br/><i>openInviteTemplateGallery()</i>" --> GAL

  GAL -- "pick a layout<br/><i>tgPick(i)</i>" --> ED
```

## Saving

```mermaid
flowchart TD
  classDef screen fill:#FFFFFF,stroke:#C5C4D3,color:#202123
  classDef editor fill:#181B34,stroke:#181B34,color:#FFFFFF
  classDef gate fill:#FFF2F3,stroke:#FF4D5B,color:#202123
  classDef store fill:#E9FBF4,stroke:#19B171,color:#202123

  ED["Editor · Save<br/><i>tplSaveClick()</i>"]:::editor
  G1{"Carries the link<br/>its type requires?<br/><i>TPL_REQUIRED_LINK</i>"}:::gate
  ERR["Refused inline<br/><i>“must contain a Join URL”</i>"]:::gate
  DLG["Save Template<br/>Template Name + Save To folder<br/><i>+ New Folder</i>"]:::screen
  G2{"Name and folder<br/>both given?"}:::gate
  G3{"Where was it<br/>created from?"}:::gate

  S1["WEBINAR_CREATED<br/>→ back to the slot picker"]:::store
  S2["WEBINAR_CREATED<br/>→ back to Send Invite, selected"]:::store
  S3["MODULE_TEMPLATES + TPLPAGE_CREATED<br/>→ top of the Templates list"]:::store

  ED --> G1
  G1 -- "no" --> ERR --> ED
  G1 -- "yes" --> DLG --> G2
  G2 -- "no" --> DLG
  G2 -- "yes" --> G3
  G3 -- "create-webinar step<br/><i>_ctSlot</i>" --> S1
  G3 -- "Send Invite<br/><i>_ctFromInvite</i>" --> S2
  G3 -- "Setup ▸ Templates" --> S3
```

## What the type decides

The template type is stamped when the template is created and never asked again. It
governs what the editor offers and what the save refuses.

| Type | May link to | Must contain | Merge categories |
|---|---|---|---|
| Webinar Invitation | Web URL, Email, Registration Link, calendars | Registration Link | Webinar Details, Users, Organization |
| Confirmation Email | Web URL, Join URL, Cancel Registration, calendars | Join URL | **Registrations**, Webinar Details, Users, Organization |
| 1st / 2nd / 3rd Reminder | Web URL, Join URL, Cancel Registration, calendars | Join URL | **Registrations**, Webinar Details, Users, Organization |
| Attendees / Absentees Follow-up | Web URL, Join URL, Recording Link, calendars | Recording Link | **Registrations**, Webinar Details, Users, Organization |
| Webinar Cancelled | Web URL, Email | — | **Registrations**, Webinar Details, Users, Organization |
| None | all of the above | — | as above |

Registrations is absent from the invitation because at invite time nobody has registered
yet (`tplMergeModules()`).
