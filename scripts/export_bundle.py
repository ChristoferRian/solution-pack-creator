#!/usr/bin/env python3
"""Package this skill into a distributable zip (stdlib only).

Usage: python3 scripts/export_bundle.py [output.zip]

Default output: <skill_dir>/dist/<name>-<version>.zip, where <version> comes from
the SKILL.md frontmatter. Excludes .venv, dist, __pycache__, *.pyc, .git, .DS_Store.
Prints size, sha256, and the install snippet.
"""
import hashlib
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'.venv', 'dist', '__pycache__', '.git', '.pytest_cache', '.mypy_cache'}
SKIP_FILES = {'.DS_Store', 'Thumbs.db'}
SKIP_SUFFIX = {'.pyc', '.pyo'}


def read_meta():
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    name = re.search(r'^name:\s*(\S+)', text, re.M)
    version = re.search(r'^version:\s*(\S+)', text, re.M)
    if not name or not version:
        sys.exit('ERROR: SKILL.md frontmatter is missing name/version')
    return name.group(1), version.group(1)


def iter_files():
    for path in sorted(SKILL.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(SKILL)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.name in SKIP_FILES or path.suffix in SKIP_SUFFIX:
            continue
        yield path, rel


def main():
    name, version = read_meta()
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else SKILL / 'dist' / f'{name}-{version}.zip'
    out.parent.mkdir(parents=True, exist_ok=True)

    files = list(iter_files())
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for path, rel in files:
            z.write(path, arcname=f'{name}/{rel.as_posix()}')

    blob = out.read_bytes()
    digest = hashlib.sha256(blob).hexdigest()
    print(f'Bundle : {out}')
    print(f'Version: {version}')
    print(f'Files  : {len(files)}')
    print(f'Size   : {len(blob)} bytes')
    print(f'SHA256 : {digest}')
    print(f'Built  : {datetime.now(timezone.utc).isoformat(timespec="seconds")}')
    print()
    print('Install on another Hermes agent:')
    print(f'  1. copy {out.name} to the target machine')
    print(f'  2. unzip -o {out.name} -d "$HERMES_HOME/skills/productivity/"')
    print(f'  3. python3 "$HERMES_HOME/skills/productivity/{name}/scripts/bootstrap.py"')
    print(f'  4. python3 "$HERMES_HOME/skills/productivity/{name}/scripts/qc.py" \\')
    print(f'         "$HERMES_HOME/skills/productivity/{name}/templates/sample-output.docx"')
    return 0


if __name__ == '__main__':
    sys.exit(main())
