#!/usr/bin/env python3
"""Build a single self-contained HTML PRD from prd-source.md.

Markers in the source:
  # / ## / ###      headings
  ![[file.jpg]]     screenshot, embedded as base64, auto-numbered "Figure N"
  ![[file.jpg|cap]] screenshot with an explicit caption after the figure number
  > USECASE: text   "Sample use case" block (text may continue on following > lines)
  > NOTE: text      a note callout
  > OPEN: text      an open-question callout
  - item            bullet
  1. item           numbered item
  | a | b |         table row (first row of a run is the header)
  blank line        paragraph break
Inline: **bold**, *italic*, `code`.
"""
import base64, html, os, re, sys

SRC, OUT, IMGDIR = 'prd-source.md', 'prd.html', 'screens-web'
fig = 0

def inline(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t

def img(spec):
    global fig
    fig += 1
    if '|' in spec:
        fn, cap = spec.split('|', 1)
    else:
        fn, cap = spec, ''
    fn, cap = fn.strip(), cap.strip()
    p = os.path.join(IMGDIR, fn)
    if not os.path.exists(p):
        sys.exit(f'MISSING IMAGE: {fn}')
    b = base64.b64encode(open(p, 'rb').read()).decode()
    label = f'Figure {fig}' + (f' — {cap}' if cap else '')
    return (f'<figure><img alt="{html.escape(label)}" '
            f'src="data:image/jpeg;base64,{b}">'
            f'<figcaption>{inline(label)}</figcaption></figure>')

def render_call(kind, buf):
    cls = {'USECASE': 'usecase', 'NOTE': 'note', 'OPEN': 'open'}.get(kind, 'note')
    title = {'USECASE': 'Sample use case', 'NOTE': 'Note', 'OPEN': 'Open question'}.get(kind, 'Note')
    return (f'<div class="call {cls}"><p class="callt">{title}</p><p>'
            + inline(' '.join(buf)) + '</p></div>')

lines = open(SRC).read().split('\n')
body, i = [], 0
para, bullets, nums, table = [], [], [], []

def flush():
    global para, bullets, nums, table
    if para:
        body.append('<p>' + inline(' '.join(para)) + '</p>'); para = []
    if bullets:
        body.append('<ul>' + ''.join(f'<li>{inline(b)}</li>' for b in bullets) + '</ul>'); bullets = []
    if nums:
        body.append('<ol>' + ''.join(f'<li>{inline(n)}</li>' for n in nums) + '</ol>'); nums = []
    if table:
        head, rest = table[0], table[1:]
        h = ''.join(f'<th>{inline(c)}</th>' for c in head)
        rows = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rest)
        body.append(f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{rows}</tbody></table></div>')
        table = []

while i < len(lines):
    ln = lines[i]; s = ln.strip()
    if not s:
        flush()
    elif s.startswith('![['):
        flush(); body.append(img(s[3:s.index(']]')]))
    elif s.startswith('#'):
        flush()
        lvl = len(s) - len(s.lstrip('#'))
        txt = s[lvl:].strip()
        anchor = re.sub(r'[^a-z0-9]+', '-', txt.lower()).strip('-')
        body.append(f'<h{lvl} id="{anchor}">{inline(txt)}</h{lvl}>')
    elif s.startswith('>'):
        flush()
        kind, buf = None, []
        while i < len(lines) and lines[i].strip().startswith('>'):
            t = lines[i].strip()[1:].strip()
            m = re.match(r'^(USECASE|NOTE|OPEN):\s*(.*)$', t)
            if m:
                if buf: body.append(render_call(kind, buf)); buf = []
                kind, t = m.group(1), m.group(2)
            if t: buf.append(t)
            i += 1
        if buf: body.append(render_call(kind, buf))
        continue
    elif s.startswith('|'):
        cells = [c.strip() for c in s.strip('|').split('|')]
        if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
            table.append(cells)
    elif re.match(r'^\d+\.\s', s):
        if para or bullets: flush()
        nums.append(re.sub(r'^\d+\.\s*', '', s))
    elif s.startswith('- '):
        if para or nums: flush()
        bullets.append(s[2:])
    else:
        if bullets or nums or table: flush()
        para.append(s)
    i += 1

flush()

CSS = """
body{font-family:'Zoho Puvi',-apple-system,'Segoe UI',Roboto,sans-serif;color:#313949;
max-width:860px;margin:0 auto;padding:48px 32px 96px;line-height:1.65;font-size:15px;background:#fff}
h1{font-size:30px;color:#202123;font-weight:600;margin:0 0 4px;line-height:1.25}
h2{font-size:23px;color:#202123;font-weight:600;margin:52px 0 12px;padding-bottom:8px;border-bottom:1px solid #D6D6E3}
h3{font-size:18px;color:#202123;font-weight:600;margin:34px 0 8px}
h4{font-size:15px;color:#434D5E;font-weight:600;margin:24px 0 6px}
p{margin:0 0 14px}
a{color:#5464F2}
code{background:#F4F4F6;border-radius:4px;padding:1px 5px;font-size:13px;
font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
ul,ol{margin:0 0 16px;padding-left:26px}
li{margin:0 0 7px}
figure{margin:20px 0 26px}
figure img{width:100%;border:1px solid #D6D6E3;border-radius:6px;display:block}
figcaption{font-size:13px;color:#616E88;margin-top:8px;font-style:italic}
.tw{overflow-x:auto;margin:0 0 22px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{border:1px solid #D6D6E3;padding:8px 11px;text-align:left;vertical-align:top}
th{background:#F1F0F7;color:#202123;font-weight:600}
.call{border-radius:6px;padding:13px 16px;margin:0 0 20px}
.call p{margin:0}
.callt{font-weight:600;font-size:13px;margin-bottom:5px!important;
text-transform:uppercase;letter-spacing:.4px}
.usecase{background:#EEEFFF;border-left:3px solid #5464F2}
.usecase .callt{color:#3752CA}
.note{background:#FFF9ED;border-left:3px solid #E28C27}
.note .callt{color:#F57C00}
.open{background:#FFF2F3;border-left:3px solid #FF4D5B}
.open .callt{color:#F63648}
.lede{color:#616E88;font-size:16px;margin-bottom:28px}
nav{background:#F1F0F7;border-radius:8px;padding:20px 26px;margin:0 0 40px}
nav p{font-weight:600;color:#202123;margin:0 0 10px}
nav ol{margin:0;padding-left:22px}
nav li{margin:0 0 5px}
nav a{text-decoration:none}
nav a:hover{text-decoration:underline}
"""

open(OUT, 'w').write(
    '<!doctype html><html><head><meta charset="utf-8">'
    '<title>Zoho Webinar in Zoho CRM</title><style>' + CSS + '</style></head><body>'
    + '\n'.join(body) + '</body></html>')

print(f'wrote {OUT}: {os.path.getsize(OUT)/1024/1024:.2f} MB, {fig} figures')
