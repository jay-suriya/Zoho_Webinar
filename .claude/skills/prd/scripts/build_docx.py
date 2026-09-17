#!/usr/bin/env python3
"""Build a .docx from prd-source.md — stdlib only.

Real Heading 1/2/3/4 styles so Word and Zoho Writer can build a TOC from them,
embedded JPEGs with captions, tables with a shaded header row, bullets, numbered
lists, and shaded callout blocks for notes / use cases / open questions.
"""
import os, re, subprocess, zipfile, html as H

SRC = os.environ.get('PRD_SRC', 'prd-source.md')
IMGDIR = os.environ.get('PRD_IMAGES', 'screens-web')
# Output name: PRD_DOCX, else the source's first '# ' heading, else a default.
def _default_out():
    try:
        for ln in open(SRC):
            if ln.startswith('# '):
                return re.sub(r'[\\/:*?"<>|]', '-', ln[2:].strip()) + '.docx'
    except OSError:
        pass
    return 'PRD.docx'
OUT = os.environ.get('PRD_DOCX') or _default_out()
EMU_IN = 914400
MAX_W_IN = 6.1                      # fits inside 1in margins on Letter

def esc(t):
    return H.escape(t, quote=False).replace('"', '&quot;')

def dims(path):
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', path],
                         capture_output=True, text=True).stdout
    w = int(re.search(r'pixelWidth:\s*(\d+)', out).group(1))
    h = int(re.search(r'pixelHeight:\s*(\d+)', out).group(1))
    return w, h

# ---------- inline runs ----------
def runs(text, base=''):
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)   # links -> plain label

    """Turn **bold**, *italic* and `code` into w:r elements."""
    parts = re.split(r'(\*\*[^*]+\*\*|(?<!\*)\*[^*]+\*(?!\*)|`[^`]+`)', text)
    out = []
    for p in parts:
        if not p:
            continue
        props, body = [base] if base else [], p
        if p.startswith('**') and p.endswith('**'):
            props.append('<w:b/>'); body = p[2:-2]
        elif p.startswith('*') and p.endswith('*'):
            props.append('<w:i/>'); body = p[1:-1]
        elif p.startswith('`') and p.endswith('`'):
            props.append('<w:rFonts w:ascii="Menlo" w:hAnsi="Menlo"/><w:sz w:val="18"/>')
            body = p[1:-1]
        rpr = f'<w:rPr>{"".join(props)}</w:rPr>' if props else ''
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{esc(body)}</w:t></w:r>')
    return ''.join(out) or '<w:r><w:t/></w:r>'

def para(text, style=None, extra=''):
    ppr = ''
    if style or extra:
        st = f'<w:pStyle w:val="{style}"/>' if style else ''
        ppr = f'<w:pPr>{st}{extra}</w:pPr>'
    return f'<w:p>{ppr}{runs(text)}</w:p>'

# ---------- document assembly ----------
body, rels, media, imgs = [], [], [], 0
fig = 0

def add_image(spec):
    global fig, imgs
    fig += 1
    fn, cap = (spec.split('|', 1) + [''])[:2]
    fn, cap = fn.strip(), cap.strip()
    path = os.path.join(IMGDIR, fn)
    if not os.path.exists(path):
        raise SystemExit(f'missing image: {fn}')
    imgs += 1
    rid = f'rIdImg{imgs}'
    media.append((fn, path))
    rels.append(f'<Relationship Id="{rid}" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                f'Target="media/{fn}"/>')
    pw, ph = dims(path)
    w_in = min(MAX_W_IN, pw / 96)
    cx, cy = int(w_in * EMU_IN), int(w_in * ph / pw * EMU_IN)
    body.append(
      '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="200" w:after="60"/></w:pPr>'
      '<w:r><w:drawing>'
      f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
      f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
      f'<wp:docPr id="{imgs}" name="Figure {fig}"/>'
      '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
      '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
      '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
      f'<pic:nvPicPr><pic:cNvPr id="{imgs}" name="{esc(fn)}"/><pic:cNvPicPr/></pic:nvPicPr>'
      f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
      f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
      '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
      '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')
    label = f'Figure {fig}' + (f' — {cap}' if cap else '')
    body.append(para(label, 'Caption', '<w:jc w:val="center"/>'))

CALL = {'USECASE': ('EEEFFF', 'Sample use case'),
        'NOTE':    ('FFF9ED', 'Note'),
        'OPEN':    ('FFF2F3', 'Open question')}

def add_callout(kind, lines):
    shade, title = CALL.get(kind, CALL['NOTE'])
    inner = (f'<w:p><w:pPr><w:spacing w:after="40"/></w:pPr>'
             f'<w:r><w:rPr><w:b/><w:caps/><w:sz w:val="17"/></w:rPr>'
             f'<w:t>{esc(title)}</w:t></w:r></w:p>'
             + f'<w:p>{runs(" ".join(lines))}</w:p>')
    body.append(
      '<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/>'
      '<w:tblBorders>' + ''.join(
          f'<w:{e} w:val="single" w:sz="4" w:color="{shade}"/>'
          for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV')) +
      '</w:tblBorders>'
      '<w:tblCellMar><w:top w:w="120" w:type="dxa"/><w:left w:w="160" w:type="dxa"/>'
      '<w:bottom w:w="120" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tblCellMar>'
      '</w:tblPr><w:tblGrid><w:gridCol w:w="9360"/></w:tblGrid>'
      f'<w:tr><w:tc><w:tcPr><w:shd w:val="clear" w:fill="{shade}"/></w:tcPr>'
      f'{inner}</w:tc></w:tr></w:tbl>'
      '<w:p><w:pPr><w:spacing w:after="0" w:line="120" w:lineRule="exact"/></w:pPr></w:p>')

def add_table(rows):
    head, rest = rows[0], rows[1:]
    n = len(head)
    grid = ''.join(f'<w:gridCol w:w="{9360 // n}"/>' for _ in range(n))
    def cell(txt, hdr):
        shd = '<w:shd w:val="clear" w:fill="F1F0F7"/>' if hdr else ''
        return (f'<w:tc><w:tcPr>{shd}</w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>'
                f'{runs(txt, "<w:b/>" if hdr else "")}</w:p></w:tc>')
    trs = ('<w:tr><w:trPr><w:tblHeader/></w:trPr>'
           + ''.join(cell(c, True) for c in head) + '</w:tr>')
    for r in rest:
        r = (r + [''] * n)[:n]
        trs += '<w:tr>' + ''.join(cell(c, False) for c in r) + '</w:tr>'
    body.append(
      '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="5000" w:type="pct"/>'
      '<w:tblBorders>' + ''.join(
          f'<w:{e} w:val="single" w:sz="4" w:color="D6D6E3"/>'
          for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV')) +
      '</w:tblBorders></w:tblPr>'
      f'<w:tblGrid>{grid}</w:tblGrid>{trs}</w:tbl>'
      '<w:p><w:pPr><w:spacing w:after="0" w:line="120" w:lineRule="exact"/></w:pPr></w:p>')

# ---------- parse ----------
lines = open(SRC).read().split('\n')
i, table, buf = 0, [], []

def flush_para():
    global buf
    if buf:
        body.append(para(' '.join(buf))); buf = []

def flush_table():
    global table
    if table:
        add_table(table); table = []

while i < len(lines):
    s = lines[i].strip()
    if not s:
        flush_para(); flush_table()
    elif s.startswith('![['):
        flush_para(); flush_table(); add_image(s[3:s.index(']]')])
    elif s.startswith('#'):
        flush_para(); flush_table()
        lvl = len(s) - len(s.lstrip('#'))
        body.append(para(s[lvl:].strip(), f'Heading{min(lvl,4)}'))
    elif s.startswith('>'):
        flush_para(); flush_table()
        kind, cbuf = 'NOTE', []
        while i < len(lines) and lines[i].strip().startswith('>'):
            t = lines[i].strip()[1:].strip()
            m = re.match(r'^(USECASE|NOTE|OPEN):\s*(.*)$', t)
            if m:
                if cbuf: add_callout(kind, cbuf); cbuf = []
                kind, t = m.group(1), m.group(2)
            if t: cbuf.append(t)
            i += 1
        if cbuf: add_callout(kind, cbuf)
        continue
    elif s.startswith('|'):
        flush_para()
        cells = [c.strip() for c in s.strip('|').split('|')]
        if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
            table.append(cells)
    elif re.match(r'^\d+\.\s', s):
        flush_para(); flush_table()
        body.append(para(re.sub(r'^\d+\.\s*', '', s), 'ListParagraph',
                         '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>'))
    elif s.startswith('- '):
        flush_para(); flush_table()
        body.append(para(s[2:], 'ListParagraph',
                         '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'))
    else:
        flush_table(); buf.append(s)
    i += 1
flush_para(); flush_table()

# ---------- package ----------
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"')

document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document {NS}><w:body>' + ''.join(body) +
            '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
            '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
            'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
            '</w:body></w:document>')

def hstyle(sid, name, sz, color, before, after, outline):
    return (f'<w:style w:type="paragraph" w:styleId="{sid}">'
            f'<w:name w:val="{name}"/><w:basedOn w:val="Normal"/><w:qFormat/>'
            f'<w:pPr><w:keepNext/><w:outlineLvl w:val="{outline}"/>'
            f'<w:spacing w:before="{before}" w:after="{after}"/></w:pPr>'
            f'<w:rPr><w:b/><w:color w:val="{color}"/><w:sz w:val="{sz}"/></w:rPr></w:style>')

styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          f'<w:styles {NS}>'
          '<w:docDefaults><w:rPrDefault><w:rPr>'
          '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="21"/>'
          '</w:rPr></w:rPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
          '<w:name w:val="Normal"/><w:qFormat/>'
          '<w:pPr><w:spacing w:after="140" w:line="288" w:lineRule="auto"/></w:pPr>'
          '<w:rPr><w:color w:val="313949"/></w:rPr></w:style>'
          + hstyle('Heading1', 'heading 1', 46, '202123', 0,   160, 0)
          + hstyle('Heading2', 'heading 2', 32, '202123', 440, 140, 1)
          + hstyle('Heading3', 'heading 3', 25, '202123', 320, 100, 2)
          + hstyle('Heading4', 'heading 4', 22, '434D5E', 240,  80, 3)
          + '<w:style w:type="paragraph" w:styleId="Caption">'
            '<w:name w:val="Caption"/><w:basedOn w:val="Normal"/><w:qFormat/>'
            '<w:pPr><w:spacing w:before="0" w:after="240"/></w:pPr>'
            '<w:rPr><w:i/><w:color w:val="616E88"/><w:sz w:val="18"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="ListParagraph">'
            '<w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:qFormat/>'
            '<w:pPr><w:ind w:left="720"/><w:spacing w:after="80"/></w:pPr></w:style>'
            '<w:style w:type="table" w:styleId="TableGrid">'
            '<w:name w:val="Table Grid"/><w:tblPr/></w:style>'
          '</w:styles>')

def numdef(nid, aid, fmt, txt):
    return (f'<w:abstractNum w:abstractNumId="{aid}"><w:multiLevelType w:val="singleLevel"/>'
            f'<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="{fmt}"/>'
            f'<w:lvlText w:val="{txt}"/><w:lvlJc w:val="left"/>'
            '<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
            + ('<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr>'
               if fmt == 'bullet' else '')
            + '</w:lvl></w:abstractNum>')

numbering = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             f'<w:numbering {NS}>'
             + numdef(1, 0, 'bullet', '') + numdef(2, 1, 'decimal', '%1.')
             + '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
               '<w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>'
             '</w:numbering>')

content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
  '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
  '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
  '<Default Extension="xml" ContentType="application/xml"/>'
  '<Default Extension="jpg" ContentType="image/jpeg"/>'
  '<Default Extension="jpeg" ContentType="image/jpeg"/>'
  '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
  '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
  '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
  '</Types>')

root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
  '</Relationships>')

doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
  '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
  '<Relationship Id="rIdNum" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
  + ''.join(rels) + '</Relationships>')

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', content_types)
    z.writestr('_rels/.rels', root_rels)
    z.writestr('word/document.xml', document)
    z.writestr('word/styles.xml', styles)
    z.writestr('word/numbering.xml', numbering)
    z.writestr('word/_rels/document.xml.rels', doc_rels)
    for fn, path in media:
        z.write(path, f'word/media/{fn}')

print(f'wrote {OUT}: {os.path.getsize(OUT)/1024/1024:.2f} MB, '
      f'{fig} figures, {len(media)} images embedded')
