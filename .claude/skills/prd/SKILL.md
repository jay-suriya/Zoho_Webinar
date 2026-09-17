---
name: prd
description: Write a developer-facing PRD by walking a built prototype flow by flow — asking the user for the document's indexes first, then explaining each one in flow order with screenshots, full field tables (type, required, default, every option verbatim), and a flowchart per flow. Delivered as markdown + self-contained HTML + .docx for import into Zoho Writer. Use whenever the user asks for a PRD, product requirements, a requirements doc, a spec, a build specification, or developer documentation for something built as a mock or prototype.
---

# PRD — the developer's build document

The PRD is what a developer keeps open while building. Two ways it fails:

- **They have to open the mock to answer a question.** → the **self-sufficiency rule** below.
- **They won't read it**, because it reads like a schema dump rather than a walkthrough.

Both are avoidable. The rest of this file is how.

---

## Before you write anything — three questions, in this order

**1. Is there a reference document to follow?**
ALWAYS ASK. Never assume, never skip it. If the user names one, read it *first* and
match its conventions — they override the defaults in `references/structure.md`.

> Zoho Writer docs refuse WebFetch with an "unsupported browser" wall. Drive a real
> signed-in Chrome instead (`mcp__claude-in-chrome__*`), then `get_page_text` and scroll.
> Writer virtualizes its pages, so one `get_page_text` returns only what has rendered —
> scroll in batches and read as you go.

**2. What are the indexes and sub-indexes?**
ASK THE USER. **Do not invent the structure.** The index list the user gives is the
document's skeleton and the contents page. Confirm the list back before writing.

**3. What is the prototype, and where does each flow start?**
Read the project's own `CLAUDE.md` and design rules first; ask only about what is
missing. The prototype is the source of truth — see below.

---

## The two rules everything else follows from

### The self-sufficiency rule

**Every flow must be understandable from the document alone.** A developer must never
need to open the mock to answer: *what fields does this step have, what type is each,
what are the options, what blocks a save?* If they have to, the document has failed.

This is the test. Apply it to each section before you call it done.

### Written from the prototype, never from memory

Every assertion must be checkable against the running prototype. Field tables are
**extracted from the DOM**; rule sets are **read from the prototype's own constants**.
Never type a field list by hand, and never write "picklist (29 options)" — list the
twenty-nine options.

---

## Document shape

```
Title
Design link (Figma or equivalent)        ← before anything else
1. Contents                              ← the user's index list, hyperlinked
2. Opening trio                          ← always these three, in this order
     What is <product>                   – a small intro
     Who uses it                         – range of customers, purpose of usage
     Why this integration, and what it solves
3…n One section per index                ← explained AS A FLOW
     Things we still need to decide
     Appendices                          ← extracted, never typed
```

**Sections follow the user's index order. Sub-indexes are the sub-headings, in the order
given.** Full detail, including house style: `references/structure.md`.

---

## How a section is written

**The governing rule: the explanation follows the flow.** A section is a walkthrough in
the order a user moves through the product — not a catalogue of controls. If an index
contains several flows, **each flow gets its own heading** and is finished before the
next begins.

Every flow carries:

| | |
|---|---|
| **Screenshots** | at every step, placed where the reader reaches it |
| **A flowchart** | so the whole path is visible at once → `references/flowcharts.md` |
| **The fields** | `Field \| Type \| Required \| Default \| Options`, inline in the flow → `references/fields.md` |
| **The rules** | what's enforced, what's refused, what blocks a save, error strings verbatim |
| **The why** | what each step does *and why it is shaped that way* |
| **Callouts** | `> NOTE:` `> OPEN:` `> USECASE:` — only where there is something real to say |

A picklist is documented **twice over**: its options listed as text (searchable,
diffable) *and* a screenshot with the dropdown **open**.

---

## Workflow

1. **Ask the three questions above.** Confirm the index list before writing.
2. **Walk the prototype flow by flow**, in index order. For each flow record both:
   - the click path for every screenshot → `shots.json`
   - the steps, branches and conditions → the flowchart brief
3. **Extract the fields** for each step from the DOM — name, type, required, default,
   every option verbatim. See `references/fields.md`.
4. **Capture the screenshots** — see `references/capture.md`. **Compare md5s every run:
   identical hashes mean a step silently failed.**
5. **Generate the flowcharts** via the flowchart agent. Save chart source next to the
   image so a chart can be regenerated, not redrawn.
6. **Write `prd-source.md`** in flow order, each figure/table/chart at the step it
   belongs to. Markers: `references/markers.md`.
7. **Extract the appendices** from the DOM and the prototype's constants.
8. **Build:**
   ```bash
   PRD_IMAGES=screens-web PRD_OUT=prd.html python3 scripts/build_prd.py
   PRD_IMAGES=screens-web python3 scripts/build_docx.py
   ```
9. **Deliver to Zoho Writer.** Default: hand over the `.docx` to import
   (`File > Import`) — it carries real Heading styles, so the contents stay clickable.
   Alternatives if asked: deploy `prd.html` and import by URL, or the `zoho-writer` MCP
   (note its ~15 KB create-from-text limit).
10. **Run the self-sufficiency test** on a section you did not just write. Then say
    plainly what is unverified.

---

## Output layout

```
docs/prd/<name>/
  prd-source.md     THE SOURCE — the document itself
  prd.html          self-contained, figures inlined
  *.docx            for Writer / Word
  screens/          full-size PNG captures
  screens-web/      downscaled JPEGs — what actually gets embedded
  shots.json        the click path for every figure
  charts/           flowchart sources + rendered images
  README.md         how to rebuild, and the traps hit on this project
```

The build scripts live in **this skill**, not in the output folder — they were copied
forward four times before and never once diverged. Don't fork them again.

## References

- `references/structure.md` — section skeleton, flow anatomy, house style
- `references/fields.md` — extracting fields, types and options from the DOM
- `references/flowcharts.md` — briefing the flowchart agent, chart conventions
- `references/capture.md` — driving a prototype, capturing figures, the trap list
- `references/markers.md` — the source markup language
