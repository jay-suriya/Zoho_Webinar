# Template flow — branch `templates-flow`

The whole life of an email template in one chart: where you start, what you decide, where
you write it, what has to be true before it saves, where it lands, and when it gets sent.

On this branch templates live in **Setup ▸ Templates**. (On `template-flow-fixes` they
belong to the module instead, managed under Zoho Webinar ▸ Preferences — a different flow.)

```mermaid
flowchart TD
  classDef entry fill:#F0F1FF,stroke:#A3ACFF,color:#202123
  classDef ask   fill:#FFFFFF,stroke:#8C91AB,color:#202123
  classDef step  fill:#FFFFFF,stroke:#C5C4D3,color:#202123
  classDef write fill:#181B34,stroke:#181B34,color:#FFFFFF
  classDef stop  fill:#FFF2F3,stroke:#FF4D5B,color:#202123
  classDef land  fill:#E9FBF4,stroke:#19B171,color:#202123

  A["Setup ▸ Templates<br/><b>+ New Template</b>"]:::entry
  B["Zoho Webinar ▸ Preferences<br/><b>Customise Template</b>"]:::entry
  C["Create Webinar — confirmation,<br/>reminder or follow-up slot<br/><b>Select Template</b>"]:::entry
  D["Send Invite ▸ Mass Email<br/><b>Select Template</b>"]:::entry

  A --> Q
  B --> Q
  C --> Q
  D --> Q

  Q{"Write a new one,<br/>or edit one that exists?"}:::ask
  Q -- "edit an existing one" --> EX["Opens read-only<br/><i>pencil to start editing</i>"]:::step
  Q -- "write a new one" --> T{"Is the type already<br/>settled by where I came from?"}:::ask

  T -- "no — could be any email" --> M["Choose module<br/>+ template type"]:::step
  T -- "yes — the step implies it" --> GAL
  M --> GAL["Template Gallery —<br/>pick a Basic layout"]:::step

  EX --> ED
  GAL --> ED
  ED["<b>Editor</b> — name · subject · body<br/><i>the type limits which links you can insert<br/>and which merge-field groups you get</i>"]:::write

  ED -- "Save" --> G1{"Does it carry the link<br/>its type requires?"}:::ask
  G1 -- "no" --> X1["Refused —<br/>insert that link first"]:::stop
  X1 -. "back to editing" .-> ED

  G1 -- "yes" --> DLG["<b>Save Template</b><br/>Template Name<br/>Save To folder, or + New Folder"]:::step
  DLG --> G2{"Name and folder<br/>both given?"}:::ask
  G2 -- "no" --> X2["Refused —<br/>fill them in"]:::stop
  X2 -. "back to the dialog" .-> DLG

  G2 -- "yes" --> W{"Where did it start?"}:::ask
  W -- "Setup ▸ Templates" --> L1["Top of the Templates list"]:::land
  W -- "a webinar slot" --> L2["Back on that slot,<br/>ready to pick"]:::land
  W -- "Send Invite" --> L3["Back in Send Invite,<br/>already chosen"]:::land

  L1 --> USE
  L2 --> USE
  L3 --> USE
  USE["The webinar sends it<br/>at that email's moment"]:::land
```

## What the type decides

The type is stamped when the template is created and never asked again. It governs what
the editor offers, and what step 5 refuses.

| Type | May link to | Must contain | Merge-field groups |
|---|---|---|---|
| Webinar Invitation | Web URL, Email, Registration Link, calendars | Registration Link | Webinar Details, Users, Organization |
| Confirmation Email | Web URL, Join URL, Cancel Registration, calendars | Join URL | **Registrations**, Webinar Details, Users, Organization |
| 1st / 2nd / 3rd Reminder | Web URL, Join URL, Cancel Registration, calendars | Join URL | **Registrations**, Webinar Details, Users, Organization |
| Attendees / Absentees Follow-up | Web URL, Join URL, Recording Link, calendars | Recording Link | **Registrations**, Webinar Details, Users, Organization |
| Webinar Cancelled | Web URL, Email | — | **Registrations**, Webinar Details, Users, Organization |
| None | all of the above | — | as above |

Registrations is missing from the invitation because at invite time nobody has registered
yet, so there is no registrant record to merge from (`tplMergeModules()`).

## Where each step lives in the code

| Step | Function / data in `webinar.html` |
|---|---|
| 1 · Setup ▸ Templates | `openTemplatesPage()`, list from `TPLPAGE_CREATED + TPLPAGE_ROWS + TPLPAGE_WEBINAR_ROWS` |
| 1 · Preferences | rows from `WEBINAR_TEMPLATES`, button calls `openTemplatePreview(key)` |
| 1 · webinar slot | `openSlotTemplatePicker(slot)`, filtered to `TPL_SLOT_TYPE[slot]` |
| 1 · Send Invite | `SelectTemplateModal` (React) |
| 2 · module + type | `openCreateTemplateModal()` → `ctNext()` |
| 2 · type implied | `slotCreateTemplate()` / `openInviteTemplateGallery()` |
| 3 · layouts | `openTemplateGallery()`, `TG_LAYOUTS`, `tgPick(i)` |
| 4 · editor | `openNewWebinarTemplate()` / `openTemplateEditor()`; rules from `TPL_TYPE_LINKS`, `tplMergeModules()` |
| 5 · link gate | `tplSaveClick()` → `tplMissingRequiredLink()` |
| 5 · dialog + folder | `tplResetFolderPicker()`, `tplFolderList()`, `tplPickFolder()`, `tplCreateFolder()` |
| 5 · name/folder gate | `tplSaveConfirm()` → `tplMissingFolder()` |
| 6 · routing | `tplSaveConfirm()`: `_ctSlot` → slot picker, `_ctFromInvite` → Send Invite, else `MODULE_TEMPLATES` + `tplPageAddCreatedRow()` |
