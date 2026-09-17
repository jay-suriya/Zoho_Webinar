# Structure and house style

## The skeleton

| Position | Section | Fixed? |
|---|---|---|
| — | Title, then the **design link** (Figma or equivalent) | yes |
| 1 | **Contents** — the user's index list, hyperlinked | yes |
| 2 | **The opening trio** | yes, always these three, in this order |
| 3…n | **One section per index**, explained as a flow | order = the user's |
| n+1 | **Things we still need to decide** | yes |
| n+2 | **Appendices** | yes |

### The opening trio

Always these three questions, always in this order:

1. **What is `<product>`** — the product being integrated with CRM. A small intro.
2. **Who uses it** — the range of customers, and the purpose of usage.
3. **Why this integration, and what it solves.**

Write (3) as a gap, not a feature list: what the product cannot do on its own, and what
the integration closes. If the user's product knowledge file names a persona, use it.

### Closing sections

**Things we still need to decide**, grouped:

- **Blocking** — work cannot start until this is answered
- **Product** — behaviour nobody has chosen yet
- **Engineering** — how it gets built
- **Design** — what it looks like
- **Assumptions this document makes** — state them, so a wrong one is caught early
- **Mock defects — do not reproduce** — things the prototype does that are bugs, not
  specification. Naming them is what stops a developer faithfully rebuilding a mistake.

**Appendices** — the exhaustive cross-reference, extracted per `fields.md`: every field
of every form, and the rule sets read from the prototype's own constants. The inline
tables serve the flow; the appendix serves lookup across the whole product.

---

## How a section is written

**The governing rule: the explanation follows the flow.**

A section is a walkthrough in the order a user moves through the product. Not a
catalogue of controls, not a reference table with prose around it.

- Proceed **step by step in flow order**.
- **Each step carries its screenshot**, placed where the reader reaches it.
- **If an index contains multiple flows, each flow gets its own heading**, and is
  finished before the next begins.
- **Sub-indexes are the sub-headings**, in the order the user supplied them.

### Open the section by saying how it divides

Before any detail, tell the reader the shape:

> The Trigger section is divided into four categories:
> 1. Incoming Message
> 2. Outgoing Message
> 3. When any CRM user does not respond to an incoming message
> 4. When an outgoing message sent from CRM gets no response

### Then the flowchart

A sub-section titled **`<Section> — Options Flow Diagram`**, with a line pointing at it:

> To get the complete context of the flow, please refer to the flow diagram.

See `flowcharts.md`.

### Then each step, in order

Per option or step, the same four beats every time:

1. **The name, bold.**
2. **What it does / when it fires** — and *why it is shaped that way*.
3. **`> USECASE:`** — a concrete scenario in prose ("Sample use case").
4. **The screenshot**, with any dropdown captured **open** so every option is visible.

### Then the fields

Inline, in the flow — not only in an appendix. Two forms, both:

**The table** (shape):

| Field | Type | Required | Default | Options |
|---|---|---|---|---|

**The glossary** (meaning) — type in parentheses:

> **Message Content** — what the message says (Multiline text)
> **Message Received From** — who sent it (LookUp)

### Then the rules

What is enforced, what is refused, what blocks a save. **Error strings quoted verbatim**,
in italics. Conditional UI written out explicitly under its own heading:

> **Operator behaviour**
> - If the user selects any option other than "Anyone", a text box appears.
> - After entering the value, the user must specify the module.
> - If unsure of the module, they can select Any Module.

### Callouts — only where there is something real to say

Never padded to fill the template.

- **`> NOTE:`** the implementation truth a developer would otherwise get wrong. The test:
  would someone rebuilding this from the screenshots get it wrong? Then it is a NOTE.
- **`> OPEN:`** what is not modelled or not decided.
- **`> USECASE:`** a worked example.

---

## House style

Taken from the reference PRD ("Messages Workflow Doc"). A reference doc supplied by the
user overrides all of this.

- **Contents decimal-numbered and hyperlinked**, sub-indexes indented under their index.
- **The design link sits above the contents** — one click from the top of the document.
- **Introduction** says what the thing does, then *"It can handle cases such as:"* with a
  bulleted list of real scenarios.
- **UI names in bold.** Explanatory annotation may be set apart (the reference uses blue).
- **Scope stated openly.** When you cover some of a set and not the rest, say so and why:
  > Since all the fields except "Message Sent To" and "Message Received From" follow the
  > same flow based on their field type, I will explain the flow of these two fields.
- **Close a comparison with "In short"** — one paragraph naming the single real
  difference between two similar things.
- **Editorial headings are allowed and encouraged** where they point at the hard part —
  *"The fields that surprise"*, *"The type rules — the part to get right"*,
  *"What blocks a save"*. A heading that warns is worth more than one that labels.

### Where this goes further than the reference

Deliberate additions, from the self-sufficiency rule:

- Field tables also carry **Required** and **Default**, not just name and type.
- Options are listed **as text as well as** shown in an open-dropdown screenshot, so they
  can be copied, searched and diffed.
- `> NOTE:` and `> OPEN:` callouts, and the closing "Things we still need to decide"
  section — the reference has no equivalent.

---

## Writing voice

- Say **why**, not only what. "It is not a picklist but an action" beats "this is a
  button".
- Prefer the concrete: name the field, quote the error, give the number.
- Don't restate a heading in its first sentence.
- Don't pad. A section with three real things in it is better than one with three real
  things and four filler paragraphs.
