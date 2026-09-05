# Zoho Webinar ⇌ Zoho CRM Integration — PRD outline (for approval)

Target Writer document: **test webinar prd**
Source of truth: `webinar.html` walked at http://localhost:8090/webinar.html

## Index

1. **Why CRM–Webinar integration**
   - What Zoho Webinar is
   - Who uses it and for what
   - What Zoho Webinar lacks on its own
   - How CRM solves it
   - Where it shows up inside CRM
2. **Integration**
   - Where it lives and who sets it up (Setup ▸ Marketplace ▸ Zoho ▸ Zoho Meetings ▸ For webinars)
   - Introduction page, before enabling (hero · How it works ×4 · Why teams enable it ×4 · what enabling does)
   - Account states the mock models — Case 1 no account · Case 2 single org · Case 3 multiple orgs · Case 4 not an admin · Case 5 trial expired
   - Setup page: Email · Organisation · Sync past webinars
   - Zoho Webinar Invite Modules (chips + search + Standard/Custom groups; drives the Send Invite module picker)
   - Webinar Deal Attribution (toggle on by default; First / Last Interaction, **Linear = default**, Increasing / Decreasing Time Decay, Position-Based)
   - Enabled state, re-configuration and Save bar
3. **Create webinar**
   - Entry points and layout switcher (Standard ▾ · Edit Page Layout · Cancel / Save & New / Save)
   - Webinar Details — every field, type, default, picklist values
   - Registration Setup — With/Without Registration and everything it reveals or hides
   - Preferences
   - Reminders (1st–3rd + their templates)
   - Follow-Ups (attendees / absentees + recording inclusion)
   - Validation and save behaviour (title required)
4. **Scheduled webinar — live**
   - List page (views, columns, filters, Create Webinar)
   - Detail page (header actions, Overview/Timeline, related lists, registration & attendance summary)
   - Send Invite flow: module picker → record picker → selection bar → Mass Email → Select Template
   - Registrants and attendance
5. **Scheduled webinar — on demand** (what differs)
6. **Completed webinar** (what differs)
7. **Completed webinar — on demand** (what differs)
8. **Supporting flows**
   - Email templates: Setup ▸ Templates, the Zoho Webinar module, the 7 defaults
   - Create Email Template → Template Gallery → editor → Save
   - Template type → allowed links → required link (save-time validation)
   - Merge fields (Webinar Details / Users / Organization; Registrations on every post-invite email)
9. **Appendices** — screen inventory · field reference · open questions and assumptions

## Screens captured so far (13)

| # | File | Screen |
|---|---|---|
| 1 | 01-webinar-list.jpg | Zoho Webinar module list, 6 records, all views |
| 2 | 02-scheduled-live-detail.jpg | Scheduled live webinar detail — header actions + registration summary |
| 3 | 03-send-invite-record-picker.jpg | Send Invite — module dropdown + view dropdown + record table |
| 4 | 04-send-invite-records-selected.jpg | Send Invite — 2 records selected, Remove ALL / Next |
| 5 | 05-mass-email.jpg | Mass Email — To, Select Template, From, warnings, Send Options |
| 6 | 06-select-template.jpg | Select Template — All Templates, search, + Create Template |
| 7 | 07-create-webinar-details-registration.jpg | Create Webinar — Webinar Details + Registration Setup |
| 8 | 08-create-webinar-preferences-reminders-followups.jpg | Create Webinar — Preferences, Reminders, Follow-Ups |
| 9 | 09-marketplace-zoho.jpg | Marketplace ▸ Zoho, Zoho Meetings card, DEMO case switcher |
| 10 | 10-integration-intro.jpg | Integration introduction page, NOT ENABLED |
| 11 | 11-integration-case1-no-account.jpg | Case 1 — Select Organization, no account found |
| 12 | 12-integration-setup-connection-invite-modules.jpg | Setup — Email/Org/Sync + Invite Modules |
| 13 | 13-integration-setup-attribution.jpg | Setup — Deal Attribution, Linear pre-selected |

Still to capture: on-demand + completed detail pages, Templates page and the 7 defaults,
Create Email Template → gallery → editor → required-link error, merge-field panel,
enabled-state integration page, Cases 3–5.

## Field data already extracted

`create-fields.md` — every Create Webinar label, control type, default and picklist values,
parsed from the markup. Needs a pass in the browser to fix two parser artefacts (section
attribution lags one row; the Duration row absorbs nested dropdowns).
