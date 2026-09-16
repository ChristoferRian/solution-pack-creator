#!/usr/bin/env python3
"""Deep structural verification: generated docx vs house style V1.1 (Pusiberad)."""
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

# peta styleId <-> nama style (house-style template pakai styleId numerik)
with zipfile.ZipFile(GEN) as _z:
    gst = ET.fromstring(_z.read('word/styles.xml'))
    gset = _z.read('word/settings.xml').decode('utf-8', 'ignore')
SID, NAME2ID = {}, {}
for _s in gst.iter(W('style')):
    _nm = _s.find(W('name'))
    if _nm is not None:
        SID[_s.get(W('styleId'))] = _nm.get(W('val'))
        NAME2ID[_nm.get(W('val'))] = _s.get(W('styleId'))
# nama built-in di styles.xml huruf kecil ("heading 1"), sedangkan Title kapital
NAME2ID_L = {(k or '').lower(): v for k, v in NAME2ID.items()}
_STYLE_NAME = lambda sid: (SID.get(sid, sid) or '')

# 1. outline comparison (headings + table order)
go = body_outline(gen)
gen_heads = [(SID.get(s, s), t) for s, t in go
             if _STYLE_NAME(s).lower().startswith('heading') or _STYLE_NAME(s).lower() == 'title']
gen_seq = [t for s, t in gen_heads]
print('--- generated headings:', gen_seq)
ok &= check('judul pakai style Title', any(s == 'Title' and t == 'SOLUTION PACK DOCUMENT' for s, t in gen_heads))
ok &= check('section order 1-4', gen_seq[1:6] == ['1. Document Control', '2. Project Background', '2.1 Customer Background', '2.2 Problem Statement', '2.3 Objective'])

# generated tables: 3 (DocControl 12, URS, 4.1 4 rows)
gen_tbls = [c for c in gen.find(W('body')) if c.tag == W('tbl')]
ok &= check('table count = 3', len(gen_tbls) == 3, str(len(gen_tbls)))
ok &= check('DocControl 12 rows', len(gen_tbls[0].findall(W('tr'))) == 12)
urs_rows_n = len(gen_tbls[1].findall(W('tr')))
ok &= check(f'URS header + baris data ({urs_rows_n} baris)', urs_rows_n >= 2)
ok &= check('4.1 has 4 rows', len(gen_tbls[2].findall(W('tr'))) == 4)

# 2. styles.xml of generated: fonts/colors/sizes
for s in gst.iter(W('style')):
    sid = s.get(W('styleId'))
    if sid == NAME2ID_L.get('heading 1'):
        rPr = s.find(W('rPr'))
        rf = rPr.find(W('rFonts')) if rPr is not None else None
        col = rPr.find(W('color')) if rPr is not None else None
        sz = rPr.find(W('sz')) if rPr is not None else None
        pPr = s.find(W('pPr'))
        jc = pPr.find(W('jc')) if pPr is not None else None
        ok &= check('H1 tema major (Calibri Heading)', rf is not None and rf.get(W('asciiTheme')) == 'majorAscii')
        ok &= check('H1 color 123555', col is not None and col.get(W('val')) == '123555')
        ok &= check('H1 sz 32 (16pt)', sz is not None and sz.get(W('val')) == '32')
        ok &= check('H1 rata kiri', jc is None or jc.get(W('val')) == 'left')
    if sid == NAME2ID_L.get('heading 2'):
        rPr = s.find(W('rPr'))
        sz = rPr.find(W('sz')) if rPr is not None else None
        pPr = s.find(W('pPr'))
        ind = pPr.find(W('ind')) if pPr is not None else None
        ok &= check('H2 sz 28 (14pt)', sz is not None and sz.get(W('val')) == '28')
        ok &= check('H2 ind left=400 leftChars=200', ind is not None and ind.get(W('left')) == '400' and ind.get(W('leftChars')) == '200',
                    str(ind.attrib) if ind is not None else 'no ind')
    if sid == NAME2ID_L.get('normal'):
        rPr = s.find(W('rPr'))
        col = rPr.find(W('color')) if rPr is not None else None
        sz = rPr.find(W('sz')) if rPr is not None else None
        ok &= check('Normal color 222222', col is not None and col.get(W('val')) == '222222')
        ok &= check('Normal sz 22 (11pt)', sz is not None and sz.get(W('val')) == '22')
    if sid == NAME2ID_L.get('normal - h2'):
        pPr = s.find(W('pPr'))
        ind = pPr.find(W('ind')) if pPr is not None else None
        jc = pPr.find(W('jc')) if pPr is not None else None
        ok &= check('Normal-H2 ind left=965 firstLine=274', ind is not None and ind.get(W('left')) == '965' and ind.get(W('firstLine')) == '274',
                    str(ind.attrib) if ind is not None else 'no ind')
        ok &= check('Normal-H2 justify', jc is not None and jc.get(W('val')) == 'both')

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
            styles_used.add(SID.get(s.get(W('val')), s.get(W('val'))))
ok &= check('objectives pakai Bullet List - H2', 'Bullet List - H2' in styles_used, str(styles_used))
ok &= check('body pakai Normal - H2', 'Normal - H2' in styles_used, str(styles_used))
ok &= check('sel tabel pakai style house', 'Table - Item' in styles_used and 'Table - Description' in styles_used, str(styles_used))

# 7. no numPr anywhere in body (manual numbering everywhere)
nnumpr = sum(1 for p in body.iter(W('p')) if p.find(W('pPr')) is not None and p.find(W('pPr')).find(W('numPr')) is not None)
# List Bullet uses numPr in the DEFAULT template — that's expected for bullets; headings must NOT
hdr_numpr = 0
for p in body.iter(W('p')):
    pPr = p.find(W('pPr'))
    if pPr is None: continue
    s = pPr.find(W('pStyle'))
    if s is not None and _STYLE_NAME(s.get(W('val'))).lower().startswith('heading') and pPr.find(W('numPr')) is not None:
        hdr_numpr += 1
ok &= check('no heading numPr', hdr_numpr == 0, str(hdr_numpr))

# 8. sectPr page setup
sect = body.find(W('sectPr'))
pgsz = sect.find(W('pgSz'))
pgmar = sect.find(W('pgMar'))
ok &= check('Letter size', pgsz.get(W('w')) == '12240' and pgsz.get(W('h')) == '15840', str(pgsz.attrib))
mar = {k.split('}')[1]: v for k, v in pgmar.attrib.items()}
ok &= check('margins 936 (0.65in) semua sisi', all(mar.get(k) == '936' for k in ('top', 'right', 'bottom', 'left')), str(mar))
ok &= check('header/footer distance 0', mar.get('header') == '0' and mar.get('footer') == '0', str(mar))

# 9. kolom No URS pakai auto-numbering (numId)
urs_no_cells = [r.findall(W('tc'))[0] for r in urs.findall(W('tr'))[1:]]
auto = 0
for tc in urs_no_cells:
    p = tc.find(W('p'))
    if p is None:
        continue
    pPr = p.find(W('pPr'))
    if pPr is not None and pPr.find(W('numPr')) is not None:
        auto += 1
ok &= check(f'kolom No URS auto-numbering ({auto}/{len(urs_no_cells)})', auto == len(urs_no_cells), f'{auto}/{len(urs_no_cells)}')

print('\nRESULT:', 'ALL PASS' if ok else 'HAS FAILURES')
sys.exit(0 if ok else 1)
