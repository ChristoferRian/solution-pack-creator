#!/usr/bin/env python3
"""QC checker for generated Solution Pack .docx (sections 1-4).

Usage: qc.py <output.docx>  ->  prints QC PASS or FAIL list; exit 1 on FAIL.
"""
import re
import sys

from docx import Document
from docx.oxml.ns import qn

DC_LABELS = [
    'Document Name', 'Document Code', 'Project Code', 'Reference Lead Code',
    'Lead Name', 'Customer Name', 'End User', 'Year & Semester Delivery',
    'Version', 'Document Owner', 'Document Status', 'Branding Rule',
]
EXPECTED_H1 = ['SOLUTION PACK DOCUMENT']
EXPECTED_H2 = ['1. Document Control', '2. Project Background',
               '3. User Requirement Summary', '4. Proposed Solution']
EXPECTED_H3 = ['2.1 Customer Background', '2.2 Problem Statement', '2.3 Objective',
               '4.1 Solution Name', '4.2 Solution Overview']
FORBIDDEN = ['stationery', 'algorhytm', 'one tme', 'spesfikasi', 'anlyzer', 'chipper']


def cell_fill(cell):
    tcPr = cell._tc.find(qn('w:tcPr'))
    if tcPr is None:
        return None
    shd = tcPr.find(qn('w:shd'))
    return shd.get(qn('w:fill')) if shd is not None else None


def all_text(doc):
    parts = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                parts.append(c.text)
    return '\n'.join(parts)


def headings(doc, level):
    name = f'Heading {level}'
    return [p for p in doc.paragraphs if p.style is not None and p.style.name == name]


def check(doc, errors):
    # --- headings: exact order, manual numbering (no numPr) ---
    for i, p in enumerate(headings(doc, 1)):
        if p.text != EXPECTED_H1[i]:
            errors.append(f'H1 wrong: {p.text!r}')
    h2 = [p.text for p in headings(doc, 2)]
    if h2 != EXPECTED_H2:
        errors.append(f'H2 sequence wrong: {h2}')
    h3 = [p.text for p in headings(doc, 3)]
    if h3 != EXPECTED_H3:
        errors.append(f'H3 sequence wrong: {h3}')
    for p in doc.paragraphs:
        if p.style is not None and p.style.name.startswith('Heading'):
            pPr = p._p.find(qn('w:pPr'))
            if pPr is not None and pPr.find(qn('w:numPr')) is not None:
                errors.append(f'heading uses auto-numbering (must be manual): {p.text!r}')

    tables = doc.tables
    if len(tables) != 3:
        errors.append(f'expected 3 tables, got {len(tables)}')
        return
    t0, t1, t2 = tables

    # --- table 1: Document Control ---
    if len(t0.rows) != 12:
        errors.append(f'DocControl rows: {len(t0.rows)} (expected 12)')
    for i, row in enumerate(t0.rows):
        if i < len(DC_LABELS) and row.cells[0].text != DC_LABELS[i]:
            errors.append(f'DocControl label r{i}: {row.cells[0].text!r} != {DC_LABELS[i]!r}')
        if cell_fill(row.cells[0]) != 'E9ECEF':
            errors.append(f'DocControl label fill r{i}: {cell_fill(row.cells[0])}')
    dc_code = t0.rows[1].cells[1].text
    pr_code = t0.rows[2].cells[1].text
    version = t0.rows[8].cells[1].text
    if not dc_code.startswith('SPD-'):
        errors.append(f'document_code not SPD-: {dc_code!r}')
    if not pr_code.startswith('PRJ-'):
        errors.append(f'project_code not PRJ-: {pr_code!r}')
    if dc_code.startswith('SPD-') and pr_code.startswith('PRJ-') and dc_code[4:] != pr_code[4:]:
        errors.append(f'code mirror mismatch: {dc_code} vs {pr_code}')
    if not re.match(r'^V\d+\.\d+', version):
        errors.append(f'version format wrong: {version!r}')

    # --- table 2: URS ---
    hdr = [c.text for c in t1.rows[0].cells]
    if hdr != ['No', 'User Requirement', 'Deskripsi']:
        errors.append(f'URS header wrong: {hdr}')
    for i, c in enumerate(t1.rows[0].cells):
        if cell_fill(c) != '4F81BD':
            errors.append(f'URS header fill c{i}: {cell_fill(c)}')
    for i, row in enumerate(t1.rows[1:]):
        cells = row.cells
        if len(cells) < 3:
            errors.append(f'URS r{i+1}: <3 cells')
            continue
        if cells[0].text != str(i + 1):
            errors.append(f'URS No not sequential at r{i+1}: {cells[0].text!r}')
        expected = 'DBE5F1' if i % 2 == 0 else 'FFFFFF'
        for k in range(3):
            if cell_fill(cells[k]) != expected:
                errors.append(f'URS zebra broken r{i+1} c{k}: {cell_fill(cells[k])} (want {expected})')
        if not cells[1].text.strip() or not cells[2].text.strip():
            errors.append(f'URS r{i+1}: empty name/description')

    # --- table 3: Solution Name (4.1) ---
    if len(t2.rows) != 4:
        errors.append(f'4.1 table rows: {len(t2.rows)} (expected 4)')
    else:
        hdr2 = [c.text for c in t2.rows[0].cells]
        if hdr2 != ['Item', 'Description']:
            errors.append(f'4.1 header wrong: {hdr2}')
        for i, c in enumerate(t2.rows[0].cells):
            if cell_fill(c) != '4F81BD':
                errors.append(f'4.1 header fill c{i}: {cell_fill(c)}')
        labels = ['Solution Name', 'Solution Category', 'Deployment Context']
        for j, want in enumerate(labels, start=1):
            if t2.rows[j].cells[0].text != want:
                errors.append(f'4.1 label r{j}: {t2.rows[j].cells[0].text!r} != {want!r}')
            if cell_fill(t2.rows[j].cells[0]) != 'E9ECEF':
                errors.append(f'4.1 label fill r{j}: {cell_fill(t2.rows[j].cells[0])}')

    # --- no trailing empty rows in any table ---
    for ti, t in enumerate(tables):
        last = t.rows[-1]
        if not any(c.text.strip() for c in last.cells):
            errors.append(f'table {ti+1}: trailing empty row')

    # --- forbidden typo strings ---
    text = all_text(doc).lower()
    for bad in FORBIDDEN:
        if bad in text:
            errors.append(f'forbidden string found: {bad!r}')


def main():
    if len(sys.argv) != 2:
        print('usage: qc.py <output.docx>', file=sys.stderr)
        return 2
    doc = Document(sys.argv[1])
    errors = []
    check(doc, errors)
    if errors:
        for e in errors:
            print('FAIL:', e)
        print(f'QC FAIL: {len(errors)} issue(s)')
        return 1
    print('QC PASS: no issues')
    return 0


if __name__ == '__main__':
    sys.exit(main())
