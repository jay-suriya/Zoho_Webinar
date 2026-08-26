# Zoho Webinar — CRM Integration Mock

Single-file HTML mock of the Zoho Webinar experience inside Zoho CRM.
Screens, flow and sample data only — not production code.

## Running it

    python3 -m http.server 8090

Then open http://localhost:8090/webinar.html

## Contents

- `webinar.html` — the whole mock (markup, styles, React-in-browser screens, sample data)

## Notable flows

- **Send Invite** — opens the recipient list directly; a module dropdown in the list
  header (Leads / Contacts / Vendors / Custom Module 1) lets one invite span several
  modules. `Add` commits the ticked records into the running count (shown per module);
  `Next` moves on to the Mass Email step.
- **Mass Email** — `Webinar Invitation` is pre-selected; the name opens the template
  picker and the pencil opens the template itself.
- **Send** — shows a success message and lands on the Invited section.
- **Modules & Fields → Zoho Webinar → Preferences** — the eight lifecycle email
  templates, each with Customise Template.
