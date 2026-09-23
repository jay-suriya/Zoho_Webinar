# 07 — What is genuinely undecided

Everything here is unspecified in the source material. **Do not resolve any of the Blocking
items by guessing** — each one changes what the code does in a way that is expensive to undo.

For the rest, a reasonable default is suggested. Take it, and say in your handoff that you did.

---

## Blocking — work cannot be finished without an answer

### 1. Webinar Cost means two contradictory things

Its tooltip reads *"This is the amount attendees will be charged to register for this
webinar"* — i.e. **revenue**. The ROI panel uses it as **what the webinar cost to run**: the
denominator, in a tile labelled `Cost`, beside a separate `Revenue (Won)` tile fed by closed
deals.

Both cannot be true.

**The ROI arithmetic is self-consistent** — `(16800 − 2500) / 2500 = +572%`, and both
per-attendee tiles divide by attendees — which makes the **tooltip the more likely error**.
But a paid webinar genuinely does have a ticket price, and if that is what this field is,
the ROI panel is missing its cost input entirely.

Affects: file 03 (the field), file 05 (every ROI tile), file 01 (the formulas).

### 2. Time Decay has no curve

`Increasing Time Decay` and `Decreasing Time Decay` state a *direction* and nothing else. No
decay function, no half-life, no worked example. They cannot be implemented as written.

They also **read inverted** against the usual meaning of the term: "Increasing Time Decay"
gives *more* credit to *earlier* webinars, where time decay conventionally favours the recent.
Decide whether the names or the descriptions are wrong before implementing either.

Affects: file 02, file 05.

### 3. Attributed share vs full amount in Deals Won

With Linear, a deal influenced by three webinars contributes a third of its amount to each.
**Whether the Deals Won table shows the deal's full value or its attributed share is
unspecified** — and the two give ROI figures three times apart in that example.

The headline number of the entire feature depends on this.

Affects: file 05, file 01.

### 4. Push to CRM has no deduplication rule

When a registrant's email already matches an existing Lead or Contact, it is unspecified
whether the existing record is **updated**, a **duplicate created**, or the registrant
**skipped**.

This is the feature that most justifies the integration; shipping it with the wrong answer
pollutes the CRM database, which is worse than not shipping it.

Affects: file 03.

---

## Product decisions

| # | Question | Suggested default |
|---|---|---|
| 5 | Should **Push Webinar Registrants to CRM** default to on? It is the feature that most justifies the integration and it ships unchecked. | Raise it; do not change the default unilaterally |
| 6 | **Re-inviting** a record already invited — allowed, resends, or refused? | Allow, and resend; show the previous send date |
| 7 | Does **attribution count attendance or registration**? File 05 divides by attendees, implying attendance, but a no-show who watched the recording was arguably influenced too | Attendance |
| 8 | What happens to **already-invited records when a module is turned off** in Who Can Participate? | Existing invites stand; the module simply stops being offered |
| 9 | Does an **on-demand** webinar really get no reminders and no follow-ups? It still has a date and still takes registrations, so its registrant gets a confirmation and nothing else | Confirm — it looks like a consequence of reusing the live form's visibility rules |
| 10 | **Send failure** in Mass Email — no template chosen, no recipients left after Remove ALL, a transport error — has no modelled state | Block send with an inline reason; never fail silently |
| 11 | **Removing every selected record** in the picker's step 2 — is Next blocked, or does it return to the record table? | Block Next, keep the user where they are |
| 12 | **No invitation templates exist** — does Select Template offer inline creation, or does the flow stall? | Offer `+ Create Template` in the empty state |
| 13 | **Cancel on re-entry**: Cancel returns to the introduction page, but for an already-enabled integration it should arguably return to the enabled panel | Return to the enabled panel when enabled |
| 14 | The three **blocking modals have no stated exit** — only the not-an-admin modal's button is named | All three dismiss back to the Marketplace card |
| 15 | **Save on the enabled page** has no success or failure state; the dirty-state bar is named, its outcome is not | Toast on success; keep the bar and show the reason on failure |

---

## Engineering

| # | Item |
|---|---|
| 16 | **Attendance Count / Attend. Rate must distinguish "not yet known" from zero.** The list view renders `—`, not `0`. Do not store either as `0` |
| 17 | The record page **scrolls an inner element**, capped ~2820px scheduled / ~3812px completed. Reaching content past the cap is done through the related-list rail |
| 18 | **All summary-chart drill-downs currently return 0 records** while their charts show non-zero counts. They are not wired to data |
| 19 | **Webinar Revenue is collapsed by default and absent from the rail** — the feature's headline numbers have no shortcut. Deliberate, but worth revisiting |
| 20 | **Guard every ROI division**: zero attendees, zero or empty cost. Render the tile empty, never `∞` or `NaN` |
| 21 | **Session Files has no upload, size limit, type restriction or delete.** All four are needed |
| 22 | **No action on a Q&A question** — no convert-to-task, no assign, no mark-answered — while the transcript deliberately contains unanswered ones |

---

## Design

| # | Item |
|---|---|
| 23 | **`Next` does nothing before `Add`** in the Send Invite picker — no error, no movement. Disable Next until a selection is committed, or drop Add. **Do not ship the silent version** |
| 24 | The **Actions menu clips** at the right edge of the viewport on a narrow record page |
| 25 | The **Registration & Attendance Summary keeps its name on a scheduled record** where there is no attendance data |
| 26 | **No back navigation in the setup wizard.** Only Cancel and Next exist, yet every answered step stays on screen with its fields live — a user can see an earlier answer but has no way to return to it |
| 27 | **No Cancel or discard on the create form.** Only Save is modelled |
| 28 | **Manage Config has no stated exit** — what closes it, whether it can be cancelled |

---

## Assumptions this spec makes

- **The three account-blocking cases are driven by a demo switcher in the source material.**
  Real behaviour is assumed to come from the user's Zoho Webinar account state and CRM role.
- **Field lists, types, defaults and option lists were extracted from the source prototype's
  DOM and its own constants**, not transcribed by hand. Where a control is custom — Repeat
  Webinar, template slots — the type column says so rather than guessing a primitive.
- **Sample values are placeholders.** Names (`Rao Priya`, `Jayasuriya`), counts, amounts and
  dates illustrate shape only. The one exception is the ROI worked example in file 01, which is
  a consistent set deliberately included so you can test your arithmetic against it.
- **API names are not specified anywhere in this set.** Fields are named by their UI label
  because that is what the source material carries. Agree the API names with whoever owns the
  module schema before building; do not derive them mechanically from the labels.

---

## Sample data that is wrong — do not reproduce

The prototype's numbers do not reconcile. **Build the relationships, not these values.**

| Where | The contradiction |
|---|---|
| Completed summary | Overview says 30 registered / 15 attended / 15 absent; tabs say 13 attendees, 6 absentees, 14 registrants; the table paginates "1 – 10 of 11 records"; module segments total 15 and 10 |
| Q&A | Tab counts sum to 19 against a stated 21 participants |
| Polls | Option counts do not sum to Total Votes, and both polls report identical figures |
| Webinar Revenue | Pipeline by Stage shows 9 Closed Won against 7 rows in the Deals Won table |
| Invited | "Invite Sent on" reads `Matchendran on Jan 28, 2022` — a user and a date unrelated to the record's 2025 data |
| Registrant list | A webinar whose only channel is Email still carries rows sourced LinkedIn, Twitter and Direct |

The correct relationships:

```
attendees + absentees          = registrants
Σ chart segments               = the total that chart is of
Σ Deals Won amounts            = Revenue (Won)
Pipeline by Stage "Closed Won" = row count of Deals Won
```
