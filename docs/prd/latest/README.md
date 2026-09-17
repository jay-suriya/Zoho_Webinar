# Zoho Webinar in Zoho CRM — PRD over the latest mock

Written from `webinar.html` at commit `15f8528` (the master file), to an index list supplied
by the user. 9.8k words, 53 figures, 4 flowcharts.

    prd-source.md     THE SOURCE. Markers are documented in the prd skill's references/markers.md
    prd.html          built document, 5.6 MB, figures inlined as base64
    *.docx            the same document with real Heading styles, for Word / Zoho Writer
    screens/          2x PNG captures
    screens-web/      the same shots at 1400px JPEG q55 — what actually gets embedded
    screens-web/charts/  the flowchart PNGs, where the build resolves them
    charts/           flowchart sources (.mmd) + rendered PNGs
    shots-new.json    click paths for the 7 figures captured for this document
    data/fields.json  the extracted field tables (63 fields x 3 variants)

Figures 01–56 were reused from `docs/prd/master/`; only the co-organiser set went stale
after `15f8528`, and co-organisers are not in this document's index. Figures 70–76 are new.

## Rebuilding

    python3 -m http.server 8090                       # from the repo root
    node ../../../.claude/skills/prd/scripts/shoot.mjs shots-new.json
    for f in screens/7*.png; do b=$(basename "$f" .png); \
      sips -Z 1400 -s format jpeg -s formatOptions 55 "$f" --out "screens-web/$b.jpg"; done
    cp charts/*.png screens-web/charts/
    PRD_IMAGES=screens-web PRD_OUT=prd.html python3 ../../../.claude/skills/prd/scripts/build_prd.py
    PRD_IMAGES=screens-web PRD_DOCX="Zoho Webinar in Zoho CRM.docx" \
      python3 ../../../.claude/skills/prd/scripts/build_docx.py

Build scripts live in the **skill** (`.claude/skills/prd/scripts/`), not here. Do not fork
them — they had already been copied forward four times, byte-identical every time.

## Traps hit on this run

- **Two of master's 66 figures were silent failures.** `60-invite-sent-toast.png` is
  byte-identical to `45-invited-section.png`, and `65-template-preview-row.png` to
  `57-templates-list.png`. The md5 check is the only thing that catches this:

      md5 screens/*.png | awk '{print $NF}' | sort | uniq -d

  Any output at all is a problem. A third duplicate appeared during this run's capture and
  was caught the same way — see the next item.
- **The Send Invite picker's two steps.** Tick rows → **Add** (commits) → **Next**.
  Clicking Add without ticking anything does nothing, and the capture came back identical
  to the picker shot. `master/shots.json`'s shot 42 has the working sequence — copy it.
- **`shots.json` covered only 58 of master's 66 figures.** Figures 60–67 have no shot
  definition at all, so they cannot be regenerated. Anything reused from that set is
  unreproducible.
- **Contents anchors.** `build_prd.py` slugifies a heading by replacing every run of
  non-alphanumerics with `-`. So `## 1.1 Who can participate from CRM` becomes
  `#1-1-who-can-participate-from-crm`, **not** `#11-...`, and `## 5.5 Q&A` becomes
  `#5-5-q-a`. Guessing this wrong silently produces a contents page where nothing
  navigates. Verify after every build:

      python3 -c "import re;h=open('prd.html').read();\
      ids=set(re.findall(r'<h[123] id=\"([^\"]+)\"',h));\
      print(sorted(set(re.findall(r'href=\"#([^\"]+)\"',h))-ids) or 'ok')"

- **Don't write raw HTML in the source.** `inline()` calls `html.escape`, so a `&nbsp;`
  used to indent the contents rendered as the literal text `&nbsp;`.
- **Markdown ordered lists restart** around interleaved sub-lists, so a `1.`-numbered
  contents rendered as 1, 1, 2, 1, 1. The contents carries its own numbers as text.
- **Webinar Revenue will not expand from a DOM click** on its band. It is collapsed by
  default and is not in the related-list rail. Master's `55-revenue-roi.png` captured it;
  reuse that rather than fighting it.
- **Field extraction gotchas** (see `data/fields.json`):
  - Preferences toggles are `.cb-item`, not `.cb-row` — miss that selector and 8 fields
    vanish silently.
  - The search box inside a `.cs-dd` counts as an `input` and turns a plain picklist into a
    false "compound" field. Exclude `input:closest('.cs-dd')`.
  - Registration Form options carry a `.rf-preview-tag` span; strip that tag only, not all
    spans, or the option text goes with it.
  - Extract with the *hidden* fields included and record visibility per variant — 63 fields
    exist, only 42 are visible in the default configuration.

## Fixed in the skill during this run

`build_docx.py` wrote a duplicate zip entry when the same figure was used twice. Each use
still gets its own relationship, but the media file is now written once.

## Zoho Writer copy

Imported 2026-09-17 by URL — `zoho-writer` MCP `Create_Document` with
`url: https://zoho-webinar-aqxbqcax.onslate.com/docs/prd/latest/prd.html`, which is why
`docs/prd/latest/` had to be merged to `master` first (Slate auto-deploys master and serves
`docs/` paths; the URL must be public for Writer to fetch it).

    https://writer.zoho.com/writer/open/wfgxzef9f2d11f3c8452d87f4e306418272f7

Writer reports 8,391 words / 1,511 sentences against the source's ~9.8k words. Whether the
figures, flowcharts and the clickable contents survived the import is **unverified** — this
machine's Chrome is not signed into Zoho.
