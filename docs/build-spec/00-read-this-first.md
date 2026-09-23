# Build: Zoho Webinar as a module inside Zoho CRM

You are working in the Zoho CRM codebase. This spec set covers **one feature, end to end**:
a new **Zoho Webinar module** in CRM, its settings, its record pages, and every operation a
user performs on it.

**Everything you need is in these documents. There is nothing else to read.** There is no
mock, no Figma and no running prototype available to you — every field, option, rule and
error string you need is written out here verbatim. Where a value is a placeholder rather
than a specification, it says so.

## What you are building

A CRM module called **Zoho Webinar**, plus:

1. A **Marketplace integration** that turns the module on and carries two settings that change
   how the rest of the feature behaves.
2. A **create form** with 63 fields across five sections, restructured by two picklists.
3. A **record page** with two distinct states — scheduled and completed — that differ in their
   header actions, their summary band, and one whole extra section.
4. **Send Invite**, which is the flow that connects the webinar to CRM's own records.
5. A **lifecycle email system** of eight template types with per-type link rules.

## Scope fence

**In scope:** everything in files 01–07 of this set.

**Out of scope — do not touch:**

- CRM's existing **Mass Email** compose step. Send Invite hands off to it. It already works and
  must keep working exactly as it does today; you supply the recipient list and the template,
  and nothing more.
- CRM's **email template editor** itself. You add template *types* and the rules that govern
  them (file 06), not a new editor.
- CRM's **list view shell**, filters, sort and column chooser. The Webinar module uses the
  standard one; you define its columns, not the mechanism.
- The **Zoho Webinar product's own surfaces** — the session runtime, the broadcast UI, the
  recording pipeline. CRM links to them and reads from them. It does not reimplement them.
- Standard CRM record actions (Clone, Share, Delete, Print Preview, Add Related List,
  Create Button, Create Client Script, View Followers). They come free with being a module.
  Only **Cancel Webinar** is yours (file 04).

## The one idea behind the whole feature

Zoho Webinar on its own cannot see CRM, and that costs four things. Every decision in these
documents traces back to removing one of them:

1. **The audience has to be rebuilt.** The people you want at the webinar are already Leads and
   Contacts. Without this, you export to CSV and re-import into a separate tool, and the list
   starts drifting from CRM the moment it is made.
   → *Who Can Participate From CRM* (file 02) and *Send Invite* (file 04).
2. **The results have to be carried back by hand.** Registrations and attendance land in the
   webinar tool; getting them onto the CRM record is another export and import.
   → *Push Webinar Registrants to CRM* (file 03) and the *Invited* related list (file 05).
3. **Nobody can answer "did it make money?"** The cost sits in one system and the deals in
   another, and no one joins them.
   → *Webinar Cost* (file 03), *attribution* (file 02) and *Webinar Revenue* (file 05).
4. **It is a second product to operate.** Different UI, different login, different conventions.
   → The whole thing being a CRM module rather than an embedded app.

If a decision you have to make is not covered here, resolve it in favour of whichever option
removes one of those four costs. That is the tie-breaker.

## Rules of engagement

**Build it as a real module, not a page.** Zoho Webinar gets a module record, a list view, a
record detail page, related lists, an owner, layouts and templates — the same furniture as
Leads. Anything you are tempted to special-case is probably something the module system
already does; use the module system.

**Derived values are derived, never stored.** Attendance rate, ROI, absentee counts, seats
left — all of these are computed from their inputs at read time. File 07 gives every formula.
Storing them creates two sources of truth that drift.

**"Not yet known" is not zero.** A webinar that has not happened has *no* attendance, which is
a different state from an attendance of zero. The list view renders an em dash for it. Do not
collapse the two into `0` anywhere — not in the model, not in the UI.

**Visibility means not rendered.** Throughout these documents, a field that is not visible in
a given configuration is **absent from the DOM**, not present-and-disabled. This matters: the
create form has 63 fields and only 42 render in the default configuration.

**Quote the product's own words.** Every label, option and error string in these documents is
verbatim. Do not improve the wording. If a label reads awkwardly, file 08 is where that gets
raised — several of them are awkward on purpose, because the same words appear elsewhere in
CRM and consistency beats elegance.

## The files

| File | What it covers |
|---|---|
| `01-module-and-data-model.md` | The module itself, its entities, every derived value and formula |
| `02-integration-setup.md` | Marketplace, the account gate, the four-step wizard, the two settings |
| `03-create-webinar.md` | The create form: all 63 fields, both branches, every sub-flow |
| `04-scheduled-webinar.md` | The scheduled record: header, summary, Send Invite, polls, files, actions |
| `05-completed-webinar.md` | The completed record: summary, revenue, invited, polls, Q&A |
| `06-emails-and-templates.md` | The eight lifecycle emails, template types, link rules, merge fields |
| `07-open-questions.md` | What is genuinely undecided, and what must be answered before some of this can be built |
| `08-decisions.md` | Naming rules and rejected alternatives — read before you rename anything |

Read `01` first. Everything else assumes it.
