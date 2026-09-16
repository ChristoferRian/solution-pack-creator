---
name: solution-pack-creator
description: "Generate dokumen Solution Pack .docx section 1-4 sesuai house-style b2b-id."
version: 1.1.0
author: Chris, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [docx, solution-pack, presales, documents]
    related_skills: []
---

# Solution Pack Creator

Menghasilkan dokumen **Solution Pack .docx** (section 1–4: Document Control, Project
Background, User Requirement Summary, Proposed Solution) dengan styling persis house-style
perusahaan Chris. Timeline & Approval Section tidak dibuat skill ini (manual oleh Chris).

Isi konten (customer, URS, solution name, dsb.) tetap disusun agent dari MoM/requirement
di vault Obsidian atau input user — skill ini men-standardisasi **struktur, layout, dan
styling**, bukan menulis konten otomatis.

Status: **v1.1.0 — house style v1.1** (style set diambil dari `Solution Pack Pussiberad 2027
V1.1.docx`). QC + verifikasi struktur lolos; sample output: `templates/sample-output.docx`.

## File pendukung (dipakai installer URL — jangan hapus referensinya)
- `references/style-spec.md` — spec house style v1.1 (acuan styling section 1-4).
- `references/style-spec-v0-pusdatin-legacy.md` — arsip spec lama (Pusdatin CSM v1.3); masih
  acuan layout Spec Table section 5 & Approval Table section 6 (manual oleh Chris).
- `references/input-schema.md` — skema JSON input. `references/qc-checklist.md` — checklist QC.
- `references/publish.md` + `INSTALL.md` + `requirements.txt` — distribusi & dependency.
- `scripts/bootstrap.py` — bikin `.venv` + install requirement; `scripts/export_bundle.py` —
  bikin bundle zip di `dist/`; `scripts/_negtest_dev.py` — test input invalid.
- `templates/house-style-template.docx`, `templates/sample-input.json`,
  `templates/sample-output.docx`, `scripts/generate.py`, `scripts/qc.py`,
  `scripts/_verify_dev.py`.

## When to Use
- User minta bikin / draft / revisi dokumen Solution Pack untuk leads b2b-id.
- Jangan untuk: dokumen selain Solution Pack, atau bagian Timeline & Approval / spec table.

## Prerequisites
- venv skill: `<skill_dir>/.venv` (python-docx). Kalau belum ada:
  `uv venv <skill_dir>/.venv && uv pip install --python <skill_dir>/.venv/bin/python python-docx`
- Template house style: `templates/house-style-template.docx` (**wajib ada**). Generator
  menolak jalan kalau file ini hilang. Cara regenerasi template dari file acuan: buka docx
  acuan, ambil `sectPr`, ganti isi `word/document.xml` jadi `<w:body>{sectPr}</w:body>`,
  pertahankan part lain apa adanya (styles/numbering/theme).
- Style acuan: `references/style-spec.md`.
- Konten: MoM/requirement PDF dari vault Obsidian (`/vaults/obsidian/<Vault>/RO/`) + input user.

## How to Run
1. Kumpulkan konten → susun JSON sesuai `references/input-schema.md`.
2. Generate:
   `<skill_dir>/.venv/bin/python <skill_dir>/scripts/generate.py <input.json> <output.docx>`
3. QC wajib sebelum dikirim ke user:
   `<skill_dir>/.venv/bin/python <skill_dir>/scripts/qc.py <output.docx>`  → harus "QC PASS".
4. Opsional (verifikasi dalam): `scripts/_verify_dev.py <output.docx>` → "ALL PASS".

## Quick Reference
```
S=/opt/data/skills/productivity/solution-pack-creator
$S/.venv/bin/python $S/scripts/generate.py input.json output.docx
$S/.venv/bin/python $S/scripts/qc.py output.docx
$S/.venv/bin/python $S/scripts/_verify_dev.py output.docx
```

## Style House v1.1 (ringkas — detail di `references/style-spec.md`)
- Judul dokumen → style `Title`; section 1–4 → `Heading 1`; sub-section → `Heading 2`.
- Body → `Normal - H2`; bullet → `Bullet List - H2`; sel tabel → `Table - Item` /
  `Table - Description`. **Jangan** pakai `Normal`, `List Bullet`, atau `Heading 3`.
- Font dari theme (Calibri heading / Cambria body) — jangan set font/size langsung di body.
- Tabel: style `Normal Table` + border manual #9FBAD0, fill label #E9ECEF, header #4F81BD,
  zebra #DBE5F1/#FFFFFF.
- Kolom **No URS auto-numbering** (numId 7), bukan angka manual.

## Procedure
1. **Kumpulkan konten** — MoM/requirement. Selesaikan ambiguitas (customer, end user,
   solusi, URS) sebelum lanjut; jangan mengarang konten. Selesai: semua field wajib terisi
   atau ditandai TBD.
2. **Susun input JSON** sesuai `references/input-schema.md`. Field struktur (12 label
   Document Control, urutan section, tabel 4.1 4 baris) dipaksa generator. Selesai: JSON
   parse & valid (generator exit 2 kalau tidak).
3. **Generate .docx**. Selesai: file ada, terbuka dengan python-docx, exit 0.
4. **QC** — `scripts/qc.py` harus "QC PASS: no issues", lalu review visual
   `references/qc-checklist.md`. Selesai: QC pass, path output dilaporkan ke user.
5. **Serahkan** — kirim docx ke user; Chris menambahkan spec table + Timeline & Approval.

## Pitfalls
- **Style salah = tampilan salah.** Body wajib `Normal - H2`; memakai `Normal` masih terlihat
  mirip tapi kehilangan indent/justify house style. Bullet wajib `Bullet List - H2`.
- Section pakai `Heading 1` (bukan `Heading 2`), judul dokumen pakai `Title` (bukan `Heading 1`).
  House style v1.1 tidak memakai `Heading 3` sama sekali.
- Tabel jangan diberi table style bawaan Word (`Table Grid`) — house style pakai
  `Normal Table` + border manual 0.5pt #9FBAD0.
- Kolom No URS pakai numPr (numId 7). Jangan menulis angka literal — kalau nanti URS
  ditambah/dikurangi, nomor manual bikin dokumen tidak konsisten dan `qc.py` tetap menuntut
  auto-numbering.
- Jangan tulis nomor section otomatis Word (numPr) di heading — house-style pakai numbering
  manual diketik ("1. Document Control").
- Zebra tabel: #DBE5F1/#FFFFFF harus strict alternation per baris data, mulai #DBE5F1.
- **Kalau template/style diganti**, wajib: generate sample dari `templates/sample-input.json`,
  jalankan `qc.py` + `_verify_dev.py`, dan bandingkan style XML hasil generate dengan file
  acuan (harus identik untuk style yang sama). Jangan mengubah template tanpa re-verifikasi.
- Style XML di template ini memakai `styleId` numerik — script yang membaca XML mentah harus
  memetakan `styleId` → `w:name` (lihat `scripts/_verify_dev.py`), bukan menganggap
  `styleId == "Heading1"`.
- Spec table (section 5) & Approval table (section 6) di luar scope generator — jangan
  ditambahkan ke output. Layout-nya (bila perlu diedit manual) ada di
  `references/style-spec-v0-pusdatin-legacy.md`.
- URS fleksibel jumlahnya (bukan wajib 10) — keputusan user.

## Verification
- `scripts/qc.py output.docx` → "QC PASS" (0 issue).
- `scripts/_verify_dev.py output.docx` → "ALL PASS" (struktur XML, style, lebar kolom,
  border, margin, auto-numbering URS).
- `templates/sample-output.docx` = output acuan dari `templates/sample-input.json`.
