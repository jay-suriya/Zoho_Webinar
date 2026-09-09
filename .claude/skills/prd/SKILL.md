---
name: prd
description: Write the developer-facing PRD for a Zoho CRM ⇌ <product> integration by walking the HTML mock flow by flow (webinar.html, mock-reference.html, or any single-file prototype). Produces one readable, screenshot-led narrative document delivered as BOTH a self-contained .html and a .docx, built from a single markdown source — why the integration exists, the settings page, the creation flow, each record state, and the supporting flows. Use whenever the user asks for a PRD, product requirements, a requirements doc, a spec, or developer documentation for something built in the mock.
---

# PRD — the developer's primary build document

This PRD is what a developer keeps open while building the feature. If they have to open
the mock to answer a question, the PRD has failed. If they *won't* read it because it
reads like a database schema, it has failed just as badly.

**It is written by analysing the mock, flow by flow, in the browser.** The mock is the
specification. `.claude/CLAUDE.md` gives you basic context only — persona, vocabulary, a
few decisions — never the requirements themselves. Anything you cannot see in the mock is
an open question, not a sentence you write from memory.

The structure is a **framework**: the same skeleton serves Zoho Webinar today and any
future integration (Survey, Backstage, Bookings…). Only the product name and the record
states change.

---

## 1. What you deliver

Two files, generated from one source. Nothing is authored by hand in a hosted editor.

```
docs/prd/<integration-slug>/
  prd-source.md      ← THE SOURCE. Narrative markdown with image markers. Edit only this.
  prd.html           ← output 1: one self-contained file, every screenshot inlined as base64
  <Doc Title>.docx   ← output 2: real Heading styles, embedded images, tables
  screens/           ← full-resolution screenshots, numbered in reading order
  screens-web/       ← the same screenshots re-encoded for embedding (see §7)
  build_prd.py       ← source → prd.html      (copy from this skill directory)
  build_docx.py      ← source → .docx         (copy from this skill directory)
```

Both scripts live in this skill's directory. **Copy them into the PRD folder at the start
of the job**, then run them from there.

```bash
cp .claude/skills/prd/build_prd.py .claude/skills/prd/build_docx.py docs/prd/<slug>/
cd docs/prd/<slug>
python3 build_prd.py     # → prd.html
python3 build_docx.py    # → <Doc Title>.docx
```

Hand over both files with their absolute paths. The user decides where they go — Writer,
Confluence, email, the repo. **Do not author into Zoho Writer.** That was tried and
abandoned: the MCP caps a create-document payload at roughly 15 KB, exposes no append or
insert-content tool, and cannot upload an image at all, so a single illustrated document
is unreachable through it. If the user wants it in Writer, they import `prd.html`
(`File > Import > From Computer`) in one action — say so once and leave it to them.

> Do not reach for a converter for the .docx. `textutil` is usually the only one on the
> machine and it **silently drops every image** — you get a 30 KB text-only file whether
> the HTML uses base64 or file paths. `build_docx.py` writes the OOXML package directly
> with the standard library. Don't install pandoc or LibreOffice for this.

---

## 2. Voice and shape — read this before writing a word

A developer reads a PRD once, front to back, to understand a feature. Write for that
read. The reference the team works from is the *Messages Workflow Doc* style: prose that
explains the flow in order, with a screenshot directly under the sentence that describes
it.

**Write like a person explaining the product to a new colleague.**

- **Narrative, in the order the user meets things.** Turning it on → creating the thing →
  the list → before the event → after the event → the variants → the supporting flows.
  Not: every field of every screen in DOM order.
- **Say what a thing is *for* before you say what it contains.** "Manual Moderation is
  what creates the approve/deny queue on the record" beats "Moderation Type: picklist,
  two values".
- **Explain the *why* whenever the mock reveals it.** Reasoning is what makes a spec
  readable: *"An invitation goes to a CRM record — someone who hasn't registered yet, so
  there's no registration to draw from. Every later email goes to a registrant, so
  per-person values become available."*
- **Flag the traps.** Fields that aren't what they look like deserve a sentence:
  *"Webinar Cost looks like a throwaway field with a `$` prefix. It isn't — it's the input
  to the entire ROI panel."*
- **Give the reader a model to hold.** One good compression beats three tables:
  *"Before the webinar the page collects; after the webinar it reports."*
- **Address the reader directly** ("you"), keep sentences medium-length, and use contractions.
  No marketing language, no "seamlessly", no restating the heading in the first sentence.
- **Sample use cases**, sparingly — two or three in the whole document, at the points where
  a feature's purpose isn't obvious from its mechanics. A short concrete scenario with a
  real person doing a real thing.

**Tables only where they genuinely help.** A table earns its place for: a rule set
(template type → allowed links → required link), a state comparison (scheduled vs
completed vs on-demand), a set of options each needing a one-line gloss (the six
attribution models), and the appendix field reference. Everything else is prose with a
screenshot. As a calibration: the rewrite that worked went from 40+ tables to 12.

**Aim for a document a developer will actually finish.** The Zoho Webinar PRD landed at
~7,650 words and 49 figures — around a 30-minute read for a feature of that size.

### Callouts

Three kinds, and they carry real weight — don't decorate with them.

| Marker | Renders as | Use it for |
|---|---|---|
| `> NOTE:` | Note (amber) | A dependency, a default worth remembering, a rule stated in the UI |
| `> USECASE:` | Sample use case (blue) | A concrete scenario showing why a feature exists |
| `> OPEN:` | Open question (red) | Something the mock doesn't settle — inline, where the reader hits it |

Put open questions **both** inline where they arise *and* collected in the
"Things we still need to decide" section. The inline one stops a developer building on
sand; the collected one is what gets taken to a meeting.

---

## 3. How to analyse the mock (this is the actual work)

1. **Serve and open it.** `python3 -m http.server 8090` in the repo, then
   `http://localhost:8090/<mock>.html?v=1` — always cache-bust with `?v=N`; these mocks
   send no cache headers and Chrome serves stale copies.
2. **Walk every flow like a user**, with the browser tools — click through, don't read
   source and guess. For each flow, record the click path that reaches it.
3. **Exhaust the states.** For every screen: empty, filled, error, validation-blocked,
   permission-denied, enabled/disabled, before/after save. Trigger each one and screenshot
   it. States are where developers lose days.
4. **Open every dialog and dropdown.** Expand every picklist and write down its values in
   the order shown.
5. **Actually trigger the validation.** Press Save with the required field empty and
   screenshot the real message. Never paraphrase an error you haven't seen.
6. **Pull rule sets out of the page's own JS** rather than inferring them. This is the
   single highest-value trick in the whole job — one call got the complete
   template-type → links → required-link matrix:

```js
// in the browser, via the javascript tool
Object.keys(window).filter(k => /^TPL_|LINK|REQUIRED|TYPE|MERGE/i.test(k))
// then read the ones that look like data
JSON.stringify({TPL_TYPE_LINKS, TPL_REQUIRED_LINK, TPL_MERGE_SOURCES}, null, 1)
```

Also useful: `document.getElementById('<panel>').innerText` for a whole panel's copy, and
`[...select.options].map(o => o.text)` for verbatim picklist values in UI order.

7. **Use source only to confirm what you saw**, and to find what the UI hides:

```bash
grep -n 'id="[a-z0-9-]*\(page\|panel\|modal\|overlay\|list\)"' <mock>.html
grep -n '<option' <mock>.html                     # picklist values, verbatim
grep -n 'function [a-zA-Z]*\(open\|show\|render\|save\|send\|create\)' <mock>.html
grep -n 'function [A-Z][A-Za-z]*(' <mock>.html    # React components
```

8. **Read `.claude/CLAUDE.md` and `git log` for context only** — vocabulary, persona, and
   the *why* behind a decision worth quoting. Never let them substitute for looking. And
   when the mock contradicts them, **the mock wins** — note the divergence.
9. **Confirm the index with the user before writing the body** — show the outline, get a
   yes. Ask at most three further questions, and only where the answer changes the
   document.

---

## 4. The index — required shape

Flow-ordered, not screen-ordered. Worked example — Zoho Webinar. Reuse the shape; swap the
product and its record states:

```
1.  Introduction                       what it is, why the gap exists, what this closes
2.  Turning the integration on         entry point → intro page → account states → settings
3.  Creating a <thing>                 the form, section by section, then what blocks a save
4.  The <thing> list                   views, columns, and how to read a row
5.  A <thing> that hasn't happened yet the pre-event record and its flows
6.  A <thing> that has happened        the post-event record, and what changed
7.  <Variant> <things>                 on-demand / recurring / whatever the product has
8.  The emails                         templates, the type rules, merge fields
9.  Things we still need to decide     grouped by product / engineering / design
10. Appendix: full field reference     every field, every default, every picklist value
```

Section titles should sound like a person wrote them. "A webinar that hasn't happened yet"
tells a developer what they're about to read; "Scheduled webinar — live" makes them work
it out.

Open the document with a one-paragraph statement of provenance — that it was written by
walking the mock, that every screenshot is real, and that gaps are marked rather than
guessed — then the table of contents.

---

## 5. What each part must contain

**Introduction.** What the product is, in plain sentences. Then the gap: what it can't do
while it lives outside CRM (registrants stranded, no link to pipeline, manual exports).
Then what this integration closes, as a short list. Then one screenshot of the module
sitting in CRM, so the reader knows where they are.

**Turning it on.** The exact navigation path. The introduction page *before* the settings,
if the product has one. Then **every account state the mock models** — no account, one org,
several orgs, insufficient permission, expired trial — each with its real dialog copy and
what the user can do about it. Then each settings section with its purpose, its default,
and its downstream effect ("this drives the module dropdown in Send Invite"). Then the
enabled state and what changes in it.

**Creating a thing.** Entry point and page chrome. Then each section in form order, but
**lead with the fields that surprise** — compound controls, fields that drive something
far away, defaults that ship on. Don't table every field here; that's the appendix. Close
with what blocks a save, and the exact message.

**The list.** Views, columns, and the two or three reading rules a developer needs (which
column is state vs type, what's blank before the event and why, how recurrence appears).

**Record states.** One section per state. Write the first one fully; write the rest **as
differences**, with a comparison table. Never repeat a related-list description across
states — say what changed.

**Supporting flows.** Whatever the states depend on: templates and their type rules, merge
fields, attribution models, push-to-CRM. Rule sets go in tables.

**Things we still need to decide.** Lead with the blocking one, on its own, explained in a
short paragraph — for Zoho Webinar it was: two template types require a Recording Link
that nothing in the product produces. Then group the rest by **product / engineering /
design** so each list can go to one person. Close with the assumptions the document makes,
stated so they can be corrected rather than inherited.

**Appendix.** Every control with type, required, and default. Verbatim picklist values.
The module's own field list. Integration settings. This is where exhaustiveness belongs.

---

## 6. Screenshots — the backbone, not decoration

- **One per state that changes the UI**, and per dialog, per error, per branch.
- **Placed directly under the sentence that describes that state.** Never batched at the
  end of a section, never a wall of images.
- **Captions say what to look at**, not what the screen is called: *"Ticking one more
  module raises the unsaved-changes bar"*, not *"Invite Modules"*.
- **Number them in reading order** as `screens/NN-short-name.jpg`. Figure numbers are
  assigned automatically by the build, in document order.
- **Re-capture anything with mock chrome bleed.** These single-file mocks layer panels; a
  screenshot showing the previous page behind the current one has to be retaken from a
  fresh reload.
- A screenshot never replaces the words. The rule or field table still gets written.
- If a screen can't be reached in the mock, say so — don't substitute a lookalike.

Expect roughly 45–60 figures for a feature the size of Zoho Webinar. It's normal to
capture more than you use and drop the duplicates.

---

## 7. The build pipeline

### Source markers

`prd-source.md` is markdown plus four extras:

```
# / ## / ###          → Heading 1 / 2 / 3
![[file.jpg]]         → screenshot, auto-numbered "Figure N"
![[file.jpg|caption]] → screenshot with a caption after the figure number
> NOTE: text          → amber callout   (continues on following > lines)
> USECASE: text       → blue callout
> OPEN: text          → red callout
| a | b |             → table; first row of a run is the header
- item  /  1. item    → bullets and numbered lists
[label](#anchor)      → link in HTML; plain label in .docx
```

Inline `**bold**`, `*italic*` and `` `code` `` work in both outputs.

### Preparing the images

Re-encode once, before building. Full-resolution screenshots make the outputs needlessly
heavy, and the images render about 6in wide anyway:

```bash
mkdir -p screens-web
for f in screens/*.jpg; do
  sips -Z 1100 -s format jpeg -s formatOptions 45 "$f" --out "screens-web/$(basename "$f")" >/dev/null
done
```

For Zoho Webinar this took 3.9 MB → 2.3 MB, giving a 2.6 MB `prd.html` and a 1.37 MB
`.docx`. Watch the numbers: `sips` at a *higher* quality setting can make files bigger
than the originals.

### Verifying before you hand over

Never claim either file works without checking. `file://` is blocked in the browser tool,
so serve the HTML:

```bash
# HTML: every image actually loaded?
# open http://localhost:8090/docs/prd/<slug>/prd.html and run:
#   [...document.images].filter(i => !i.complete || i.naturalWidth === 0).length   → must be 0

# DOCX: valid package, images present, and it opens?
python3 -c "
import zipfile, xml.dom.minidom as M, re
z = zipfile.ZipFile('<Doc Title>.docx')
for n in ['word/document.xml','word/styles.xml','word/numbering.xml',
          'word/_rels/document.xml.rels','[Content_Types].xml','_rels/.rels']:
    M.parseString(z.read(n))
d = z.read('word/document.xml').decode()
print('media:', sum(1 for n in z.namelist() if n.startswith('word/media/')))
print('headings:', len(re.findall(r'w:pStyle w:val=\"Heading', d)))
print('leaked markdown:', len(re.findall(r'\[[^\]]+\]\(#', d)))
"
qlmanage -t -s 1000 -o /tmp/ql "<Doc Title>.docx"   # then read the PNG — proves it opens
```

Heading count must be non-zero (if it's 0, the style attribute is malformed), leaked
markdown must be 0, and media must equal your figure count.

---

## 8. Rules of evidence

- **The mock is the source of truth**; `.claude/CLAUDE.md` is background. Every statement
  traces to something you saw — name the anchor where it helps (`#integ-intro-panel`,
  `openSlotTemplatePicker()`, `TPL_REQUIRED_LINK`).
- **Never invent** metrics, dates, adoption numbers, research or API contracts. Unknowns
  are open questions with owners, or `TBD`.
- **Separate fact from assumption.** Behaviour the mock implies but does not show is an
  assumption in its own list, not a requirement in the body.
- **Quote UI copy verbatim** — error messages, helper text, empty states. Paraphrasing an
  error message is how a build ships the wrong string.
- **Flag mock bugs as bugs**, so nobody reproduces them: placeholder content on every
  record, a count that disagrees with the rows, a heading left over from another module,
  a link that goes nowhere. Say plainly it's a mock defect, not behaviour to copy.
- **Don't answer the product's open questions yourself.** Deciding whether on-demand
  webinars should have Send Invite is not yours to settle from a mock; record it with an
  owner.

---

## 9. Reusing this for the next integration

1. Copy the two build scripts in, and keep the §4 index shape — swap the product name and
   replace the record states with that product's states.
2. Sections 1–4 are unchanged in purpose: orientation, settings, creation, list.
3. One section per record state, first one full, rest as differences.
4. The supporting-flows section covers that integration's dependencies.
5. Keep the voice, the screenshot placement rule, the callout kinds, and the
   tables-only-where-they-earn-it discipline, so every PRD in the set reads identically.
6. If the user supplies a reference document or a richer brief, read it **first** and match
   its structure and voice over the defaults here.

---

## 10. Before handing it over

- Both files exist, and you have **verified** them (§7) rather than assumed.
- The index matches the headings in the body, in order.
- Every flow in scope has screenshots, each placed under the sentence it illustrates and
  captioned with what to look at.
- Every field in every form appears in the appendix with type, required and default;
  picklist values are verbatim and in UI order.
- Each control's purpose is stated, or listed as an open question.
- Record states are differentiated, not duplicated.
- Validation messages and UI copy are quoted exactly, from screens you actually triggered.
- Nothing invented; assumptions in their own list; mock bugs flagged as bugs.
- Open questions grouped by owner, with the blocking one called out first.

Finish by giving the user: the absolute path to the `.html`, the absolute path to the
`.docx`, the figure count and word count, and the open questions that need their answer —
with the blocking one first.
