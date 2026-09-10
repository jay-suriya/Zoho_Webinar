# PRD — current master flow

`prd.html` is the built document; open it in a browser (it is self-contained, images
inlined as base64). Everything else here is the source.

    prd-source.md     the text. Markers are documented at the top of build_prd.py
    screens/          2x PNG captures, straight from the mock
    screens-web/      the same shots at 1700px JPEG, which is what gets embedded
    shoot.mjs         the screenshot driver
    build_prd.py      prd-source.md + screens-web/ -> prd.html

## Rebuilding after a mock change

    python3 -m http.server 8090        # from the repo root, so the mock is served
    node shoot.mjs shots.json          # re-capture whatever changed
    for f in screens/*.png; do b=$(basename "$f" .png); \
      sips -Z 1700 -s format jpeg -s formatOptions 72 "$f" --out "screens-web/$b.jpg"; done
    PRD_IMAGES=screens-web PRD_OUT=prd.html python3 build_prd.py

## The screenshot driver

`shoot.mjs` launches headless Chrome on port 9333, drives the page over the DevTools
protocol and writes PNGs. It needs no npm packages — Node 22+ has a global `WebSocket`.

A shot is `{file, steps[], wait, stepWait}`; each step is JavaScript evaluated in the
page. Helpers injected after every load:

    __click(text, tag)        click the element whose trimmed text equals `text`
    __clickContains(text)     ... or contains it
    __clickRelated(label)     click a related-list item on the webinar detail page
    __scrollDetail(px)        scroll #react-detail-root (the detail page's scroller)
    __scrollForm(px)          scroll .form-page-body (the create form's scroller)
    __pick(label, option)     set a .cs-btn picklist by its label and option text

`node shoot.mjs --eval "expr"` evaluates one expression and prints it — how the entry
points below were found.

Ways into each area, for writing new shots:

    openSettingsModal()                      Setup
    mpSetupWebinar()                         Marketplace > Zoho > For webinars > Set up
    integShowPanel('integ-setup-panel')      a specific integration panel
    goToList() / goToForm()                  webinar list / create form
    openWebinarDetail(record, isCompleted, hasInvited)

Record shapes for `openWebinarDetail` are in `webinar.html` on the list rows —
search for `onclick="openWebinarDetail(`.

## Gotchas that cost time

- Helpers are injected inside a JS template literal, so a `\s` in a regex there
  collapses to `s`. Avoid regexes in the injected helpers.
- Both the detail page and the create form scroll an inner element, not the window.
  `window.scrollTo` silently does nothing.
- The create form's five sections fit in ~770px of scroll: Preferences, Reminders and
  Follow-Ups all land in the same screenful.
- `Webinar Revenue` on a completed webinar is collapsed by default — click its band
  before capturing, or the shot is the Details panel underneath.
- Identical file sizes across shots almost always mean a step silently failed. Compare
  md5s before trusting a batch.
