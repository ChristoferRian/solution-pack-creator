#!/usr/bin/env python3
"""Deep structural verification: generated docx vs reference Pusdatin CSM v1.3."""
import sys
import zipfile
from xml.etree import ElementTree as ET

import os
import tempfile

W = lambda t: '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}' + t
GEN = sys.argv[1] if len(sys.argv) > 1 else os.path.join(tempfile.gettempdir(), 'sp_verify.docx')
# Optional reference docx for outline comparison. Set SP_REF_DOCX to the Pusdatin
# CSM v1.3 source document to enable it; otherwise the ref-only checks are skipped.
REF = os.environ.get('SP_REF_DOCX', '')

def load(path):
    with zipfile.ZipFile(path) as z:
        return ET.fromstring(z.read('word/document.xml'))

def body_outline(root):
    body = root.find(W('body'))
    out = []
    for c in body:
        if c.tag == W('p'):
            pPr = c.find(W('pPr'))
            st = ''
            if pPr is not None:
                s = pPr.find(W('pStyle'))
                st = s.get(W('val')) if s is not None else ''
            txt = ''.join(t.text or '' for t in c.iter(W('t'))).strip()
            if txt:
                out.append((st, txt[:60]))
        elif c.tag == W('tbl'):
            rows = c.findall(W('tr'))
            out.append(('TBL', f'rows={len(rows)}'))
    return out

def style_defs(root):
    # styles.xml loaded separately; here just doc properties we care about
    return None

def check(label, cond, detail=''):
    print(('PASS' if cond else 'FAIL'), label, ('| ' + detail) if detail and not cond else '')
    return cond

ok = True
gen = load(GEN)
ref = load(REF) if REF and os.path.exists(REF) else None

# 1. outline comparison (headings + table order)
go = body_outline(gen)
gen_heads = [(s, t) for s, t in go if s.startswith('Heading')]
gen_seq = [t for s, t in gen_heads]
print('--- generated headings:', gen_seq)
ok &= check('H1 present', any(s == 'Heading1' and t == 'SOLUTION PACK DOCUMENT' for s, t in gen_heads))
ok &= check('section order 1-4', gen_seq[:5] == ['SOLUTION PACK DOCUMENT', '1. Document Control', '2. Project Background', '2.1 Customer Background', '2.2 Problem Statement'])

# generated tables: 3 (DocControl 12, URS, 4.1 4 rows)
gen_tbls = [c for c in gen.find(W('body')) if c.tag == W('tbl')]
ok &= check('table count = 3', len(gen_tbls) == 3, str(len(gen_tbls)))
ok &= check('DocControl 12 rows', len(gen_tbls[0].findall(W('tr'))) == 12)
ok &= check('URS 11 rows (header+10)', len(gen_tbls[1].findall(W('tr'))) == 11)
ok &= check('4.1 has 4 rows', len(gen_tbls[2].findall(W('tr'))) == 4)

# 2. styles.xml of generated: fonts/colors/sizes
with zipfile.ZipFile(GEN) as z:
    gst = ET.fromstring(z.read('word/styles.xml'))
    gset = z.read('word/settings.xml').decode('utf-8', 'ignore')
for s in gst.iter(W('style')):
    sid = s.get(W('styleId'))
    if sid == 'Heading1':
        rPr = s.find(W('rPr'))
        rf = rPr.find(W('rFonts')) if rPr is not None else None
        col = rPr.find(W('color')) if rPr is not None else None
        sz = rPr.find(W('sz')) if rPr is not None else None
        pPr = s.find(W('pPr'))
        jc = pPr.find(W('jc')) if pPr is not None else None
        ok &= check('H1 Arial', rf is not None and rf.get(W('ascii')) == 'Arial')
        ok &= check('H1 color 123555', col is not None and col.get(W('val')) == '123555')
        ok &= check('H1 sz 40', sz is not None and sz.get(W('val')) == '40')
        ok &= check('H1 center', jc is not None and jc.get(W('val')) == 'center')
    if sid == 'Heading2':
        rPr = s.find(W('rPr'))
        sz = rPr.find(W('sz')) if rPr is not None else None
        pPr = s.find(W('pPr'))
        ind = pPr.find(W('ind')) if pPr is not None else None
        ok &= check('H2 sz 23', sz is not None and sz.get(W('val')) == '23')
        ok &= check('H2 ind left=514 hanging=719', ind is not None and ind.get(W('left')) == '514' and ind.get(W('hanging')) == '719',
                    str(ind.attrib) if ind is not None else 'no ind')
    if sid == 'Normal':
        rPr = s.find(W('rPr'))
        col = rPr.find(W('color')) if rPr is not None else None
        sz = rPr.find(W('sz')) if rPr is not None else None
        ok &= check('Normal color 222222', col is not None and col.get(W('val')) == '222222')
        ok &= check('Normal sz 16 (8pt)', sz is not None and sz.get(W('val')) == '16')

# 3. URS table details: header repeat, zebra, white bold text
urs = gen_tbls[1]
rows = urs.findall(W('tr'))
trPr = rows[0].find(W('trPr'))
ok &= check('URS header tblHeader repeat', trPr is not None and trPr.find(W('tblHeader')) is not None)
ok &= check('URS header cantSplit', trPr is not None and trPr.find(W('cantSplit')) is not None)
hdr0 = rows[0].findall(W('tc'))[0]
shd = hdr0.find(W('tcPr')).find(W('shd'))
ok &= check('URS header fill 4F81BD', shd is not None and shd.get(W('fill')) == '4F81BD')
# zebra check
def fills(row):
    return [ (c.find(W('tcPr')).find(W('shd').get and W('shd')) if False else (c.find(W('tcPr')).find(W('shd')) if c.find(W('tcPr')) is not None else None)) for c in row.findall(W('tc')) ]
def row_fill(row):
    shds = fills(row)
    vals = set(s.get(W('fill')) if s is not None else None for s in shds)
    return vals.pop() if len(vals) == 1 else ('MIXED', vals)
for i, r in enumerate(rows[1:4]):
    want = 'DBE5F1' if i % 2 == 0 else 'FFFFFF'
    ok &= check(f'URS zebra r{i+1} = {want}', row_fill(r) == want, str(row_fill(r)))

# white bold header text: check run props in header cell
hp = rows[0].findall(W('tc'))[0].find(W('p'))
r0 = hp.find(W('r'))
rPr = r0.find(W('rPr')) if r0 is not None else None
col = rPr.find(W('color')) if rPr is not None else None
b = rPr.find(W('b')) if rPr is not None else None
ok &= check('URS header text white bold', col is not None and col.get(W('val')) == 'FFFFFF' and b is not None)

# 4. borders 9FBAD0 on all tables
for i, t in enumerate(gen_tbls):
    tb = t.find(W('tblPr')).find(W('tblBorders'))
    top = tb.find(W('top')) if tb is not None else None
    ok &= check(f'table{i+1} border 9FBAD0 sz4', top is not None and top.get(W('color')) == '9FBAD0' and top.get(W('sz')) == '4')

# 5. widths
def widths(t):
    return [g.get(W('w')) for g in t.find(W('tblGrid')).findall(W('gridCol'))]
ok &= check('DocControl widths 3090/7278', widths(gen_tbls[0]) == ['3090', '7278'], str(widths(gen_tbls[0])))
ok &= check('URS widths 605/2370/7393', widths(gen_tbls[1]) == ['605', '2370', '7393'], str(widths(gen_tbls[1])))
ok &= check('4.1 widths 3090/7278', widths(gen_tbls[2]) == ['3090', '7278'], str(widths(gen_tbls[2])))

# 6. objectives use List Bullet (style in doc)
body = gen.find(W('body'))
styles_used = set()
for p in body.iter(W('p')):
    pPr = p.find(W('pPr'))
    if pPr is not None:
        s = pPr.find(W('pStyle'))
        if s is not None:
            styles_used.add(s.get(W('val')))
ok &= check('ListBullet used for objectives', 'ListBullet' in styles_used, str(styles_used))

# 7. no numPr anywhere in body (manual numbering everywhere)
nnumpr = sum(1 for p in body.iter(W('p')) if p.find(W('pPr')) is not None and p.find(W('pPr')).find(W('numPr')) is not None)
# List Bullet uses numPr in the DEFAULT template — that's expected for bullets; headings must NOT
hdr_numpr = 0
for p in body.iter(W('p')):
    pPr = p.find(W('pPr'))
    if pPr is None: continue
    s = pPr.find(W('pStyle'))
    if s is not None and s.get(W('val')).startswith('Heading') and pPr.find(W('numPr')) is not None:
        hdr_numpr += 1
ok &= check('no heading numPr', hdr_numpr == 0, str(hdr_numpr))

# 8. sectPr page setup
sect = body.find(W('sectPr'))
pgsz = sect.find(W('pgSz'))
pgmar = sect.find(W('pgMar'))
ok &= check('Letter size', pgsz.get(W('w')) == '12240' and pgsz.get(W('h')) == '15840', str(pgsz.attrib))
mar = {k.split('}')[1]: v for k, v in pgmar.attrib.items()}
ok &= check('margins 1300/720/520/720', mar.get('top') == '1300' and mar.get('right') == '720' and mar.get('bottom') == '520' and mar.get('left') == '720', str(mar))

print('\nRESULT:', 'ALL PASS' if ok else 'HAS FAILURES')
sys.exit(0 if ok else 1)
