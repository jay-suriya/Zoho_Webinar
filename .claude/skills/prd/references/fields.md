# Fields — extract them, never type them

The rule: **a field table is read out of the running prototype, not written from
memory.** A typed table is wrong the first time the mock changes, and nobody can tell
which entries are stale.

A first pass on an earlier PRD wrote *"Picklist (29 options)"*. That is the failure this
file exists to prevent. **List the twenty-nine options.**

---

## What every field needs

| Field | Type | Required | Default | Options |
|---|---|---|---|---|

- **Type** — named explicitly: text, textarea/multiline, picklist, multi-select, radio,
  checkbox, toggle, date, time, date+time, file, lookup, user-lookup, number, currency.
- **Required** — yes/no, from the actual marker in the DOM, not from what looks sensible.
- **Default** — what the field reads before anyone touches it.
- **Options** — **every option, verbatim, in the order the product shows them.** Never a
  count, never "etc.", never a truncated list.

Then restate the same fields as a **glossary**, type in parentheses, so the reader gets
meaning as well as shape:

> **Message Content** — what the message says (Multiline text)
> **Message Received From** — who sent it (LookUp)

---

## How to extract

Run JS in the page and read the DOM. `scripts/shoot.mjs --eval "expr"` evaluates one
expression against the served prototype and prints the result — that is the fastest way
to pull a table without a browser session.

```bash
python3 -m http.server 8090          # from the project root
node scripts/shoot.mjs --eval "document.querySelectorAll('.form-row').length"
```

### Worked example — this project's mock (`webinar.html`)

The create form is hand-written HTML with a consistent shape:

| What | Selector |
|---|---|
| A row of the form | `.form-row` |
| One field within a row | `.form-group` |
| A custom picklist | `.cs-wrap` → `.cs-btn` (the closed control) + `.cs-dd` (dropdown) |
| The options | `.cs-opt` (180 of them across the mock) |
| Required marker | `.req` |

So the whole create form comes out in one expression:

```js
[...document.querySelectorAll('#createForm .form-group')].map(g => ({
  label:    g.querySelector('label')?.textContent.trim(),
  required: !!g.querySelector('.req'),
  type:     g.querySelector('.cs-wrap') ? 'picklist'
          : g.querySelector('textarea')  ? 'textarea'
          : g.querySelector('input')?.type || 'text',
  default:  g.querySelector('.cs-btn')?.textContent.trim()
          || g.querySelector('input')?.value || '',
  options:  [...g.querySelectorAll('.cs-opt')].map(o => o.textContent.trim())
}))
```

**Adapt the selectors to the prototype in front of you** — the method transfers, the
class names do not. On a React surface, read the rendered DOM the same way; the compiled
`React.createElement` source is harder to read than the output it produces.

### Rule sets live in the source, not the DOM

Constants that drive behaviour are read from the prototype's own JS, so the document
cannot drift from them. In this mock: `TPL_TYPE_LINKS`, `TPL_REQUIRED_LINK`,
`TPL_MERGE_SOURCES`, `IM_MODULES`, `CO_ORG_DIRECTORY`, `RP_FIELDS`.

```bash
node scripts/shoot.mjs --eval "JSON.stringify(TPL_TYPE_LINKS)"
```

---

## Traps

- **Variant forms.** One form often has several shapes — live vs on-demand, with vs
  without registration. Each variant needs its own table; a field that only appears in
  one of them is exactly the thing a developer will miss. Switch the form and re-extract;
  don't reason about what *should* change.
- **Options that depend on another field.** The 2nd and 3rd reminder picklists in this
  mock carry **None** on top of the same eleven intervals the 1st offers — which is what
  lets a webinar send fewer than three reminders. Capture the dependency in prose, and
  give the dependent field its own row.
- **Hidden-until-revealed fields.** Reveal them first, then extract. A field behind a
  toggle is still a field.
- **The default is not always the first option.** Read what the control actually shows.
- **React renders a tick late.** An `--eval` that reads the DOM immediately after a click
  gets the previous state. Return a Promise and wait ~1.2s.

## Check before you ship a table

- Every picklist has its options listed in full, in product order.
- Every variant of the form has its own table.
- Required and default are read from the DOM, not assumed.
- Re-run the extraction after any change to the prototype — a table is a claim about the
  current build.
