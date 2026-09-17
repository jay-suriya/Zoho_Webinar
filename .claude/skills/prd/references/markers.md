# The source markup language

`prd-source.md` is the document. `scripts/build_prd.py` turns it into a self-contained
HTML; `scripts/build_docx.py` turns the same source into a `.docx` with real Heading
styles. Both read the markers below — **the source is the single source of truth, never
edit the built HTML or docx.**

## Markers

```
# / ## / ###        headings
![[file.jpg]]       figure, auto-numbered "Figure N"
![[file.jpg|cap]]   figure with an explicit caption after the number
> NOTE: text        a note callout
> OPEN: text        an open-question callout
> USECASE: text     a "Sample use case" block
| a | b |           table row (the first row of a run is the header)
- item              bullet
1. item             numbered item
blank line          paragraph break
```

Inline: `**bold**`, `*italic*`, `` `code` ``, `[text](url)`.

Callout text may continue on following `>` lines.

## Figures

- The filename resolves against `$PRD_IMAGES` (default `screens-web`), **not** the
  full-size `screens/`. Embedding 2× PNGs makes a document nobody can open.
- Numbering is automatic and sequential through the document. **Never write "Figure 12"
  in prose** — insert the figure where it belongs and let the build number it; a
  hand-written number goes stale the moment a figure is added above it.
- Captions earn their place. `![[15-coorg-field.jpg|The field reads + Add co-organisers
  until something is selected]]` tells the reader what to look at. A caption that repeats
  the preceding sentence does not.

## Flowcharts

A flowchart is embedded as an ordinary figure — it is a PNG like any other:

```
![[charts/flow-01-send-invite.png|Send Invite, end to end. Add commits the selection; Next opens Mass Email]]
```

Keep the chart **source** (`charts/flow-01-send-invite.mmd`) beside the image so the
chart can be regenerated when the flow changes rather than redrawn. See `flowcharts.md`.

## Tables

The first row of a run is the header. Escape pipes inside cells as `\|`.

Field tables use this column order, every time:

```
| Field | Type | Required | Default | Options |
```

Long option lists stay in the cell — do not truncate, do not write "etc.", do not
replace the options with a count. See `fields.md`.

## Conventions the build does not enforce

- **UI names in bold**: **Send Invite**, **Add co-organisers**.
- **Error strings verbatim, in italics**: *"Enter a name for kate.williams@zylker.com."*
- **Code, ids and constants in backticks**: `coOrgDone()`, `TPL_TYPE_LINKS`, `src|email`.
- One blank line between blocks. The build is whitespace-sensitive at block boundaries.

## Checks before building

- Every `![[...]]` resolves to a file in `$PRD_IMAGES`. A missing image fails loudly —
  do not ship a build you have not opened.
- No hand-written figure numbers in prose.
- Every table run has a header row.
- Callout prefixes are exact: `> NOTE:` not `> Note:`.
