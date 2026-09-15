#!/usr/bin/env python3
"""Negative tests: invalid inputs must be rejected with exit 2 and clear messages."""
import copy
import json
import subprocess
import sys
import tempfile
import os

HERE = os.path.dirname(__file__)
SKILL = os.path.dirname(HERE)
GEN = os.path.join(SKILL, 'scripts', 'generate.py')
PY = sys.executable  # run generate.py with the same interpreter running this test
SAMPLE = os.path.join(SKILL, 'templates', 'sample-input.json')

with open(SAMPLE, encoding='utf-8') as f:
    base = json.load(f)

fails = 0

def run_case(name, mutate, expect_substr):
    global fails
    data = copy.deepcopy(base)
    mutate(data)
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(data, f)
        tmp = f.name
    out = subprocess.run([PY, GEN, tmp, '/tmp/never.docx'], capture_output=True, text=True)
    os.unlink(tmp)
    passed = out.returncode == 2 and expect_substr in out.stderr
    print(('PASS' if passed else 'FAIL'), name, f'(rc={out.returncode})', '' if passed else out.stderr.strip()[:200])
    if not passed:
        fails += 1

run_case('missing meta field', lambda d: d['meta'].pop('end_user'), 'meta.end_user missing')
run_case('missing solution field', lambda d: d['solution'].pop('category'), 'solution.category missing')
run_case('bad doc code prefix', lambda d: d['meta'].__setitem__('document_code', 'XX-foo'), 'must start with SPD-')
run_case('bad proj code prefix', lambda d: d['meta'].__setitem__('project_code', 'XX-foo'), 'must start with PRJ-')
run_case('code mirror mismatch', lambda d: d['meta'].__setitem__('project_code', 'PRJ-OTHER-2027'), 'mirror')
run_case('lowercase version', lambda d: d['meta'].__setitem__('version', 'v0.4'), 'version must match')
run_case('empty objectives', lambda d: d['background'].__setitem__('objectives', []), 'objectives empty')
run_case('urs missing description', lambda d: d['urs'][0].pop('description'), 'urs[0]')
run_case('urs empty list', lambda d: d.__setitem__('urs', []), 'urs must be a non-empty')

print('\nNEGATIVE TESTS:', 'ALL PASS' if fails == 0 else f'{fails} FAILURES')
sys.exit(1 if fails else 0)
