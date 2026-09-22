#!/usr/bin/env python3
"""Ambil / tulis kembali blok prosa dari input JSON Solution Pack.

Dipakai untuk writing-quality pass (skill `avoid-ai-writing`): prosa diekstrak ke
satu file teks datar, diaudit + ditulis ulang, lalu ditulis kembali ke JSON yang
sama. Field non-prosa (kode dokumen, nama URS, nama/kategori solusi, semua label
Document Control) tidak pernah ikut — itu identifier, bukan prosa.

Urutan blok = urutan tampil di dokumen (bab 2 -> 4):
  background.customer_background[*]
  background.problem_statement[*]
  background.objectives[*]
  urs[*].description
  solution.deployment_context
  solution.overview[*]

Usage:
  prose_blocks.py <input.json> --extract <out.txt>
  prose_blocks.py <input.json> --apply <in.txt>

Exit codes: 0 ok, 2 input tidak konsisten (jumlah blok beda). `--apply` menolak jalan
kalau jumlah blok tidak sama persis, supaya tidak ada prosa yang tertukar posisinya.

Catatan `--apply`: kalau tidak ada field yang berubah, file JSON tidak ditulis sama sekali.
Kalau ada yang berubah, JSON ditulis ulang dengan formatting standar (`ensure_ascii=False`,
indent 2) — jadi file dengan formatting lain akan ikut ter-rapikan. Isi field di luar blok
prosa tetap apa adanya.
"""
import json
import sys


def collect(data):
    """Return list of (setter, original_value) plus the flat text blocks.

    setter(is_list) menerima list blok untuk field itu (atau string untuk field
    yang aslinya string) dan menulisnya kembali ke `data`.
    """
    bg = data['background']
    sol = data['solution']
    fields = []

    cb = bg['customer_background']
    fields.append(('background.customer_background', cb if isinstance(cb, list) else [cb]))

    for key in ('problem_statement', 'objectives'):
        fields.append((f'background.{key}', list(bg[key])))

    for i, u in enumerate(data['urs']):
        fields.append((f'urs[{i}].description', [u['description']]))

    fields.append(('solution.deployment_context', [sol['deployment_context']]))

    fields.append(('solution.overview', list(sol['overview'])))
    return fields


def blocks_of(fields):
    out = []
    for _, values in fields:
        out.extend(values)
    return out


def write_back(data, fields, new_blocks):
    pos = 0
    changed = []
    bg = data['background']
    sol = data['solution']
    for path, values in fields:
        n = len(values)
        chunk = new_blocks[pos:pos + n]
        pos += n
        for old, new in zip(values, chunk):
            if old != new:
                changed.append(path)
        if path == 'background.customer_background':
            bg['customer_background'] = chunk[0] if isinstance(bg['customer_background'], str) else chunk
        elif path == 'background.problem_statement':
            bg['problem_statement'] = chunk
        elif path == 'background.objectives':
            bg['objectives'] = chunk
        elif path.startswith('urs['):
            data['urs'][int(path[4:path.index(']')])]['description'] = chunk[0]
        elif path == 'solution.deployment_context':
            sol['deployment_context'] = chunk[0]
        elif path == 'solution.overview':
            sol['overview'] = chunk
    return changed


def main():
    if len(sys.argv) != 4 or sys.argv[2] not in ('--extract', '--apply'):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    json_path, mode, text_path = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    fields = collect(data)

    if mode == '--extract':
        text = '\n\n'.join(b.strip() for b in blocks_of(fields))
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text + '\n')
        words = len(text.split())
        print(f'extracted {len(blocks_of(fields))} blocks ({words} words) -> {text_path}')
        return 0

    with open(text_path, encoding='utf-8') as f:
        raw = f.read()
    new_blocks = [p.strip() for p in raw.split('\n\n') if p.strip()]
    expected = len(blocks_of(fields))
    if len(new_blocks) != expected:
        print(f'INPUT ERROR: jumlah blok beda — file teks punya {len(new_blocks)}, '
              f'JSON butuh {expected}. Blok dipisah baris kosong; jangan keluar '
              f'atau menambah baris kosong di dalam satu blok.', file=sys.stderr)
        return 2

    changed = write_back(data, fields, new_blocks)
    if not changed:
        print(f'{len(new_blocks)} blocks diperiksa: tidak ada yang berubah — file JSON tidak ditulis.')
        return 0
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'applied {len(new_blocks)} blocks to {json_path}; {len(changed)} field berubah')
    for c in changed:
        print('  -', c)
    return 0


if __name__ == '__main__':
    sys.exit(main())
