# Capturing figures

`scripts/shoot.mjs` launches headless Chrome, drives the page over the DevTools protocol
with `Runtime.evaluate`, and writes PNGs. No dependencies — Node 22+ has a global
`WebSocket` and `fetch`.

```bash
python3 -m http.server 8090                    # from the project root
node scripts/shoot.mjs shots.json              # capture every shot
node scripts/shoot.mjs --eval "expr"           # evaluate one expression, print it
BASE=http://localhost:8090/other.html node scripts/shoot.mjs shots.json
```

`--eval` is how you find entry points. Use it before writing any shot.

## shots.json

A declarative list of figures and the click path to each:

```json
[
  { "file": "01-marketplace-zoho.png",
    "steps": ["openSettingsModal();integOpenZoho()",
              "integShowPanel('integ-grid-panel')"] },
  { "file": "02-intro-hero.png",
    "steps": ["openSettingsModal();integOpenZoho()", "mpSetupWebinar()"] }
]
```

Each step is JS evaluated in the page, in order, from a fresh load. **Steps are absolute,
not relative** — every shot replays the whole path from the start, so one broken figure
never corrupts the next.

Injected helpers: `__click`, `__clickRelated`, `__scrollDetail`, `__scrollForm`, `__pick`.

## Downscale, then build

Full-size 2× PNGs make a document nobody can open. Embed the web copies:

```bash
for f in screens/*.png; do b=$(basename "$f" .png); \
  sips -Z 1400 -s format jpeg -s formatOptions 55 "$f" --out "screens-web/$b.jpg"; done
```

## *** Verify every run: compare md5s ***

**Identical md5s across a batch mean a step silently failed** — the page never changed
and you captured the same screen several times. Nothing errors; the files just look
plausible.

```bash
md5 screens/*.png | awk '{print $NF}' | sort | uniq -d
```

Any output at all is a problem. This is the single most valuable check here.

---

## Traps

General, and worth checking on any prototype:

- **React renders a tick late.** An `--eval` reading `innerText` immediately after a call
  returns `""`. Return a Promise and wait ~1.2s.
- **Modal dialogs freeze the renderer.** `alert()`, `confirm()` and `prompt()` block
  every subsequent command until dismissed by hand — it has cost a frozen tab and a dead
  `Runtime.evaluate` here before. Never click a control that raises one while driving.
- **Inner scrollers.** Pages that scroll an inner element ignore `window.scrollTo`. Set
  `scrollTop` on the actual scroller.
- **Smooth scrolling races the screenshot.** If a call scrolls the target into view, set
  `scrollTop` explicitly rather than trusting where the animation landed.
- **Multi-step controls.** A picker that commits before it advances needs both clicks.

Specific to this project's mock (`webinar.html`) — these cost real time:

- `openSettingsModal()` alone shows the settings grid, not the integration panels. Follow
  it with `integOpenZoho()`.
- `setupStep(n)` smooth-scrolls the new step into view, so the setup panel is already
  scrolled when the shot is taken. Set `scrollTop` for a top-of-step shot.
- The create form's scroller maxes out around **770px** — Preferences, Reminders and
  Follow-Ups all land in one screenful.
- The completed record's scroller maxes out around **3812px**. Use the related-list rail
  (`__clickRelated`) to reach Polls and Q&A. **Webinar Revenue is not in the rail** —
  scroll to ~1380 after clicking its band. It is also **collapsed by default**, so a
  naive shot captures the panel beneath it.
- The Send Invite picker has two internal steps: tick the rows, **Add** (commits, step 2),
  then **Next** (opens Mass Email). Clicking Next first does nothing.
- A `\s` regex inside an injected template literal collapses to `s`. Escape it.

## Capturing options

A picklist is documented twice — options as text *and* a screenshot with the dropdown
**open**. So the shot's last step opens the control:

```json
{ "file": "12-webinar-type-open.png",
  "steps": ["openCreateWebinar()", "__click('#webinarType .cs-btn')"] }
```

Check the dropdown is actually open in the resulting image. An option list that renders
off-screen or clipped is worse than no screenshot, because it looks complete.

## Record what you learn

Every project grows its own trap list. Put it in the output folder's `README.md` as you
go — the traps above were all discovered the expensive way, and writing them down is the
only reason they are not rediscovered each time.
