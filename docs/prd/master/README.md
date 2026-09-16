# Build Specification — the current master flow

`prd.html` is the document. It is self-contained (66 screenshots inlined as base64), so it
opens in any browser and can be imported into Zoho Writer in one action
(`File > Import > From Computer`, or by URL once it is deployed).

    prd-source.md     THE SOURCE. Markers are documented at the top of build_prd.py.
    prd.html          built document, 66 figures, ~10.3k words
    *.docx            the same document with real Heading styles, for Word/Writer
    screens/          2x PNG captures straight from the mock
    screens-web/      the same shots at 1400px JPEG q55 — what actually gets embedded
    shots.json        the click path for every figure
    shoot.mjs         the screenshot driver

This supersedes `docs/prd/current/`, which describes the flow as it stood on 2026-09-10 —
before the setup wizard, the co-organiser panel and Customize Registration Page.

## Rebuilding

    python3 -m http.server 8090          # from the repo root
    node shoot.mjs shots.json            # re-capture (or a subset in its own json)
    for f in screens/*.png; do b=$(basename "$f" .png); \
      sips -Z 1400 -s format jpeg -s formatOptions 55 "$f" --out "screens-web/$b.jpg"; done
    PRD_IMAGES=screens-web PRD_OUT=prd.html python3 build_prd.py
    PRD_IMAGES=screens-web python3 build_docx.py

## Traps worth knowing (they cost time here)

- **Identical md5s across a batch mean a step silently failed.** Compare them every run.
- `openSettingsModal()` alone shows the settings grid, not the integration panels —
  follow it with `integOpenZoho()`.
- React pages render a tick after the call, so an `--eval` that reads `innerText`
  immediately gets an empty string. Return a Promise and wait ~1.2s.
- `setupStep(n)` smooth-scrolls the new step into view, so the setup panel is already
  scrolled when the screenshot is taken — set `scrollTop` explicitly for a top-of-step shot.
- The create form's scroller maxes out around 770px: Preferences, Reminders and Follow-Ups
  all land in one screenful.
- The completed record's scroller maxes out around 3812px. Use the related-list rail
  (`__clickRelated`) to reach Polls and Q&A; **Webinar Revenue is not in the rail** —
  scroll to ~1380 after clicking its band.
- The Send Invite picker has two internal steps: tick rows, **Add** (commits, step 2),
  then **Next** (opens Mass Email). Clicking Next first does nothing.
