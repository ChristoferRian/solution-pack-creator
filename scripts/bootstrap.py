#!/usr/bin/env python3
"""Bootstrap the skill venv (portable; stdlib only).

Usage: python3 scripts/bootstrap.py

Creates <skill_dir>/.venv, installs requirements.txt (python-docx), then verifies
the interpreter can import docx. Prefers `uv`; falls back to the venv module.
Exit codes: 0 ok, 1 failure.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
VENV = SKILL / '.venv'
REQ = SKILL / 'requirements.txt'
PYTHON = VENV / ('Scripts' if os.name == 'nt' else 'bin') / (
    'python.exe' if os.name == 'nt' else 'python')


def run(cmd):
    print('+', ' '.join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd], check=False)


def interpreter_ok(py):
    if not Path(py).exists():
        return False
    return subprocess.run([str(py), '-c', 'import docx'], capture_output=True).returncode == 0


def main():
    if interpreter_ok(PYTHON):
        print(f'venv OK: {PYTHON}')
        return 0

    uv = shutil.which('uv')
    if uv:
        if not PYTHON.exists():
            if run([uv, 'venv', VENV]).returncode != 0:
                return 1
        if run([uv, 'pip', 'install', '--python', PYTHON, '-r', REQ]).returncode != 0:
            return 1
    else:
        if not PYTHON.exists():
            if run([sys.executable, '-m', 'venv', VENV]).returncode != 0:
                return 1
        if run([PYTHON, '-m', 'pip', 'install', '-r', REQ]).returncode != 0:
            return 1

    if not interpreter_ok(PYTHON):
        print('ERROR: python-docx not importable from the new venv', file=sys.stderr)
        return 1
    print(f'venv OK: {PYTHON}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
