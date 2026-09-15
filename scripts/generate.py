#!/usr/bin/env python3
"""Solution Pack Document generator — sections 1-4 only.

House style locked to 'Solution Pack Pusdatin Counter Surveillance Mobile v1.3.docx'.
Input JSON schema: see references/input-schema.md. Section 5 (spec table) and
section 6 (approval) are intentionally NOT generated.

Usage: generate.py <input.json> <output.docx>
Exit codes: 0 ok, 2 invalid input, 1 runtime error.
"""
import json
import re
import sys

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---- palette (from source doc) ----
NAVY = RGBColor(0x12, 0x35, 0x55)     # headings
BODY = RGBColor(0x22, 0x22, 0x22)      # body text
TITLE = RGBColor(0x33, 0x33, 0x33)     # document subtitle line
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FILL_LABEL = 'E9ECEF'                  # DocControl / 4.1 label cells
FILL_HEADER = '4F81BD'                 # table header rows
FILL_ZEBRA = 'DBE5F1'                  # odd data rows
FILL_WHITE = 'FFFFFF'
BORDER = '9FBAD0'                      # all table borders, 0.5pt

DC_LABELS = [
    'Document Name', 'Document Code', 'Project Code', 'Reference Lead Code',
    'Lead Name', 'Customer Name', 'End User', 'Year & Semester Delivery',
    'Version', 'Document Owner', 'Document Status', 'Branding Rule',
]

TBLPR_SEQ = ['w:tblStyle', 'w:tblpPr', 'w:tblOverlap', 'w:bidiVisual',
             'w:tblStyleRowBandSize', 'w:tblStyleColBandSize', 'w:tblW', 'w:jc',
             'w:tblCellSpacing', 'w:tblInd', 'w:tblBorders', 'w:shd',
             'w:tblLayout', 'w:tblCellMar', 'w:tblLook', 'w:tblCaption',
             'w:tblDescription', 'w:tblPrChange']
TCPR_SEQ = ['w:cnfStyle', 'w:tcW', 'w:gridSpan', 'w:hMerge', 'w:vMerge',
            'w:tcBorders', 'w:shd', 'w:noWrap', 'w:tcMar', 'w:textDirection',
            'w:tcFitText', 'w:vAlign', 'w:hideMark', 'w:tcPrChange']
TRPR_SEQ = ['w:cnfStyle', 'w:divId', 'w:gridBefore', 'w:gridAfter', 'w:wBefore',
            'w:wAfter', 'w:cantSplit', 'w:trHeight', 'w:tblHeader',
            'w:tblCellSpacing', 'w:jc', 'w:hidden', 'w:ins', 'w:del',
            'w:trPrChange']


def _normalize(parent, seq):
    """Re-append children of parent in canonical OOXML schema order."""
    order = {t: i for i, t in enumerate(seq)}
    children = list(parent)
    children.sort(key=lambda el: order.get('w:' + el.tag.split('}')[1], len(seq)))
    for el in children:
        parent.remove(el)
    for el in children:
        parent.append(el)


def _set_fonts(style, name):
    rPr = style.element.get_or_add_rPr()
    rf = rPr.get_or_add_rFonts()
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rf.set(qn(a), name)


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'), fill)
    tcPr.append(s)
    _normalize(tcPr, TCPR_SEQ)


def _tbl_borders(table):
    bd = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + edge)
        e.set(qn('w:val'), 'single')
        e.set(qn('w:sz'), '4')
        e.set(qn('w:space'), '0')
        e.set(qn('w:color'), BORDER)
        bd.append(e)
    table._tbl.tblPr.append(bd)


def _tbl_cellmar(table, top=70, left=100, bottom=70, right=100):
    cm = OxmlElement('w:tblCellMar')
    for tag, v in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        e = OxmlElement('w:' + tag)
        e.set(qn('w:w'), str(v))
        e.set(qn('w:type'), 'dxa')
        cm.append(e)
    table._tbl.tblPr.append(cm)


def _fixed_widths(table, widths):
    tblPr = table._tbl.tblPr
    old = tblPr.find(qn('w:tblW'))
    if old is not None:
        tblPr.remove(old)
    tw = OxmlElement('w:tblW')
    tw.set(qn('w:w'), str(sum(widths)))
    tw.set(qn('w:type'), 'dxa')
    tblPr.append(tw)
    _normalize(tblPr, TBLPR_SEQ)
    table.autofit = False
    # rewrite tblGrid to exact widths
    grid = table._tbl.find(qn('w:tblGrid'))
    for gc in list(grid):
        grid.remove(gc)
    for w in widths:
        gc = OxmlElement('w:gridCol')
        gc.set(qn('w:w'), str(w))
        grid.append(gc)
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            cell.width = Emu(widths[i] * 635)  # 635 EMU per dxa


def _repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    for tag in ('w:cantSplit', 'w:tblHeader'):
        trPr.append(OxmlElement(tag))
    _normalize(trPr, TRPR_SEQ)


def _run(p, text, size=8.0, bold=False, color=BODY, center=False):
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return r


# ---- document setup (styles + page) ----

def setup(doc):
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    sec.top_margin = Inches(1300 / 1440)
    sec.bottom_margin = Inches(520 / 1440)
    sec.left_margin = Inches(720 / 1440)
    sec.right_margin = Inches(720 / 1440)
    sec.header_distance = Inches(0)
    sec.footer_distance = Inches(0)

    n = doc.styles['Normal']
    _set_fonts(n, 'Calibri')
    n.font.size = Pt(8)
    n.font.color.rgb = BODY
    pf = n.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(3)   # after=60 dxa
    pf.line_spacing = 1.05    # line=252, lineRule auto

    specs = (('Heading 1', 'Arial', 20, None, None),
             ('Heading 2', 'Calibri', 11.5, 514, 719),
             ('Heading 3', 'Calibri', 9.5, 635, 419))
    for name, font, size, ind, hang in specs:
        st = doc.styles[name]
        _set_fonts(st, font)
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = NAVY
        p = st.paragraph_format
        p.space_before = Pt(0)
        p.space_after = Pt(3)
        p.line_spacing = 1.05
        if ind:
            p.left_indent = Inches(ind / 1440)
            p.first_line_indent = Inches(-hang / 1440)  # hanging indent
    h1 = doc.styles['Heading 1'].paragraph_format
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.left_indent = Inches(0)
    h1.first_line_indent = Inches(0)

    lb = doc.styles['List Bullet']
    _set_fonts(lb, 'Calibri')
    lb.font.size = Pt(8)
    lb.font.color.rgb = BODY


# ---- validation ----

def _as_list(v):
    if isinstance(v, str):
        return [v]
    return v


def validate(data):
    errs = []
    meta = data.get('meta') or {}
    for k in ('title', 'document_code', 'project_code', 'reference_lead_code',
              'lead_name', 'customer_name', 'end_user', 'year_semester_delivery',
              'version', 'document_owner', 'document_status', 'branding_rule'):
        if k not in meta:
            errs.append(f'meta.{k} missing')
    bg = data.get('background') or {}
    for k in ('customer_background', 'problem_statement', 'objectives'):
        if k not in bg:
            errs.append(f'background.{k} missing')
    if 'problem_statement' in bg and not _as_list(bg['problem_statement']):
        errs.append('background.problem_statement empty')
    if 'objectives' in bg and not _as_list(bg['objectives']):
        errs.append('background.objectives empty')
    urs = data.get('urs')
    if not isinstance(urs, list) or not urs:
        errs.append('urs must be a non-empty list')
    else:
        for i, item in enumerate(urs):
            if not isinstance(item, dict) or not item.get('name') or not item.get('description'):
                errs.append(f'urs[{i}] needs name & description')
    sol = data.get('solution') or {}
    for k in ('name', 'category', 'deployment_context', 'overview'):
        if k not in sol:
            errs.append(f'solution.{k} missing')
    if 'overview' in sol and not _as_list(sol['overview']):
        errs.append('solution.overview empty')

    dc, pc = meta.get('document_code', ''), meta.get('project_code', '')
    if dc and not dc.startswith('SPD-'):
        errs.append(f'document_code must start with SPD- (got: {dc})')
    if pc and not pc.startswith('PRJ-'):
        errs.append(f'project_code must start with PRJ- (got: {pc})')
    if dc.startswith('SPD-') and pc.startswith('PRJ-') and dc[4:] != pc[4:]:
        errs.append(f'project_code must mirror document_code (SPD-/PRJ- suffix mismatch: {dc} vs {pc})')
    if meta.get('version') and not re.match(r'^V\d+\.\d+', meta['version']):
        errs.append(f'version must match V<x.y> + optional changelog (got: {meta["version"]})')
    return errs


# ---- builders ----

def build_title(doc, meta):
    doc.add_paragraph('SOLUTION PACK DOCUMENT', style='Heading 1')
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(p, meta['title'], size=10.5, bold=True, color=TITLE)


def build_doc_control(doc, meta):
    doc.add_paragraph('1. Document Control', style='Heading 2')
    values = [
        ('Document Name', 'Solution Pack Document'),
        ('Document Code', meta['document_code']),
        ('Project Code', meta['project_code']),
        ('Reference Lead Code', meta['reference_lead_code']),
        ('Lead Name', meta['lead_name']),
        ('Customer Name', meta['customer_name']),
        ('End User', meta['end_user']),
        ('Year & Semester Delivery', meta['year_semester_delivery']),
        ('Version', meta['version']),
        ('Document Owner', meta['document_owner']),
        ('Document Status', meta['document_status']),
        ('Branding Rule', meta['branding_rule']),
    ]
    t = doc.add_table(rows=len(values), cols=2)
    for i, (label, val) in enumerate(values):
        c0, c1 = t.rows[i].cells
        shade(c0, FILL_LABEL)
        _run(c0.paragraphs[0], label, bold=True)
        _run(c1.paragraphs[0], val)
    _tbl_borders(t)
    _tbl_cellmar(t)
    _fixed_widths(t, [3090, 7278])


def build_background(doc, bg):
    doc.add_paragraph('2. Project Background', style='Heading 2')
    doc.add_paragraph('2.1 Customer Background', style='Heading 3')
    for para in _as_list(bg['customer_background']):
        doc.add_paragraph(para)
    doc.add_paragraph('2.2 Problem Statement', style='Heading 3')
    for para in _as_list(bg['problem_statement']):
        doc.add_paragraph(para)
    doc.add_paragraph('2.3 Objective', style='Heading 3')
    for o in _as_list(bg['objectives']):
        doc.add_paragraph(o, style='List Bullet')


def build_urs(doc, urs):
    doc.add_paragraph('3. User Requirement Summary', style='Heading 2')
    t = doc.add_table(rows=1, cols=3)
    hdr = t.rows[0]
    _repeat_header(hdr)
    for i, label in enumerate(('No', 'User Requirement', 'Deskripsi')):
        c = hdr.cells[i]
        shade(c, FILL_HEADER)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        _run(c.paragraphs[0], label, size=7, bold=True, color=WHITE, center=True)
    for i, item in enumerate(urs):
        row = t.add_row()
        fill = FILL_ZEBRA if i % 2 == 0 else FILL_WHITE
        for c in row.cells:
            shade(c, fill)
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        _run(row.cells[0].paragraphs[0], str(i + 1), size=7.5, center=True)
        _run(row.cells[1].paragraphs[0], item['name'], size=7.5, bold=True)
        _run(row.cells[2].paragraphs[0], item['description'], size=7.5)
    _tbl_borders(t)
    _tbl_cellmar(t)
    _fixed_widths(t, [605, 2370, 7393])


def build_solution(doc, sol):
    doc.add_paragraph('4. Proposed Solution', style='Heading 2')
    doc.add_paragraph('4.1 Solution Name', style='Heading 3')
    rows = [
        ('Item', 'Description'),
        ('Solution Name', sol['name']),
        ('Solution Category', sol['category']),
        ('Deployment Context', sol['deployment_context']),
    ]
    t = doc.add_table(rows=4, cols=2)
    # header row
    for i, label in enumerate(rows[0]):
        c = t.rows[0].cells[i]
        shade(c, FILL_HEADER)
        _run(c.paragraphs[0], label, size=7, bold=True, color=WHITE, center=True)
    # label rows
    for j, (label, val) in enumerate(rows[1:], start=1):
        c0, c1 = t.rows[j].cells
        shade(c0, FILL_LABEL)
        _run(c0.paragraphs[0], label, bold=True)
        _run(c1.paragraphs[0], val)
    _tbl_borders(t)
    _tbl_cellmar(t)
    _fixed_widths(t, [3090, 7278])

    doc.add_paragraph('4.2 Solution Overview', style='Heading 3')
    for para in _as_list(sol['overview']):
        doc.add_paragraph(para)


def main():
    if len(sys.argv) != 3:
        print('usage: generate.py <input.json> <output.docx>', file=sys.stderr)
        return 2
    with open(sys.argv[1], encoding='utf-8') as f:
        data = json.load(f)
    errs = validate(data)
    if errs:
        for e in errs:
            print('INPUT ERROR:', e, file=sys.stderr)
        return 2
    doc = Document()
    setup(doc)
    build_title(doc, data['meta'])
    build_doc_control(doc, data['meta'])
    build_background(doc, data['background'])
    build_urs(doc, data['urs'])
    build_solution(doc, data['solution'])
    doc.save(sys.argv[2])
    print('OK:', sys.argv[2])
    return 0


if __name__ == '__main__':
    sys.exit(main())
