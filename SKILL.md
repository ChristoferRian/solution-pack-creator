---
name: solution-pack-creator
description: "Generate dokumen Solution Pack .docx section 1-4 sesuai template house-style b2b-id."
version: 1.0.0
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
Background, User Requirement Summary, Proposed Solution) dengan styling persis
house-style perusahaan Chris — styling dikunci ke template Pusdatin CSM v1.3
(lihat `references/style-spec.md`). Timeline & Approval Section tidak dibuat skill
ini (dikerjakan manual oleh Chris).

Isi konten (customer, URS, solution name, dan seterusnya) tetap disusun oleh agent
dari MoM/requirement di vault Obsidian atau input user — skill ini men-standardisasi
**struktur, layout, dan styling**, bukan menulis konten secara otomatis.

Status: **v1.0.0 — locked, tested & QC-passed** (31 struktur cek + 9 negative input
tests all pass) dan portable (bisa di-export + di-install ke Hermes lain, lihat
`references/publish.md`). Sample output verifiable: `templates/sample-output.docx`.

## When to Use
- User minta bikin / draft / revisi dokumen Solution Pack untuk leads b2b-id
- Jangan untuk: dokumen selain Solution Pack, atau bagian Timeline & Approval

## Prerequisites
- venv skill: `<skill_dir>/.venv` (python-docx). Bikin/verifikasi dengan
  `scripts/bootstrap.py` — ia prefer `uv`, fallback `python -m venv` + `pip`, dan
  install dari `requirements.txt`.
- Spec styling ada di dalam skill: `references/style-spec.md`
- Skema input: `references/input-schema.md`
- Untuk konten: MoM/requirement PDF dari vault Obsidian (path vault spesifik mesin user)

## How to Run
1. Kumpulkan konten (dari vault/user) → susun draft section 1–4 dalam bentuk JSON
   (skema di `references/input-schema.md`).
2. Validasi JSON manual (kuncinya ada & wajib semua, lihat skema) sebelum generate.
3. Generate:
   `terminal(command="<skill_dir>/.venv/bin/python <skill_dir>/scripts/generate.py <input.json> <output.docx>")`
4. QC output pakai `references/qc-checklist.md`.

## Files
Installer URL Hermes hanya mengambil SKILL.md + path yang direferensi eksplisit di
body (`references/`, `templates/`, `scripts/`). Daftar ini wajib dipertahankan:
- `scripts/generate.py` — generator .docx (section 1–4)
- `scripts/qc.py` — QC struktur output
- `scripts/bootstrap.py` — bikin/repair venv + install dependency
- `scripts/export_bundle.py` — packaging zip untuk dipindah ke Hermes lain
- `scripts/_verify_dev.py`, `scripts/_negtest_dev.py` — test dev (opsional)
- `references/input-schema.md`, `references/qc-checklist.md`, `references/style-spec.md`, `references/publish.md`
- `templates/sample-input.json`, `templates/sample-output.docx`
- `[requirements.txt](./requirements.txt)` dan `[INSTALL.md](./INSTALL.md)`

## Quick Reference
```
# setup / repair venv (portable)
python3 <skill_dir>/scripts/bootstrap.py
# generate
<skill_dir>/.venv/bin/python <skill_dir>/scripts/generate.py <input.json> <output.docx>
# QC struktur (wajib pass sebelum dikirim ke user)
<skill_dir>/.venv/bin/python <skill_dir>/scripts/qc.py <output.docx>
# export bundle buat dipindah ke Hermes lain
python3 <skill_dir>/scripts/export_bundle.py
# contoh input lengkap lihat templates/sample-input.json
```
`<skill_dir>` = folder skill ini di mesin manapun (mis. `~/.hermes/skills/productivity/solution-pack-creator`).

## Procedure
1. **Kumpulkan konten** — MoM dari vault, kebutuhan user. Selesaikan ambiguitas
   (customer, end user, solusi, URS) sebelum lanjut; jangan mengarang konten.
   Selesai: semua field wajib skema terisi atau di-mark TBD.
2. **Susun input JSON** sesuai `references/input-schema.md`. Field konten bebas
   diisi agent, field struktur (12 label Document Control, urutan section, 4 baris
   tabel 4.1) dipaksa oleh generator. Selesai: JSON parse & wajib semua terisi.
3. **Generate .docx** dengan perintah di Quick Reference. Selesai: file output
   ada dan dibuka tanpa error (verifikasi dengan open ulang pakai python-docx).
4. **QC** — jalankan `scripts/qc.py` (validasi struktur + typos terlarang) lalu
   `references/qc-checklist.md` untuk review visual. Selesai: QC pass, laporkan
   path output ke user.
5. **Serahkan** — kirim file docx ke user. Chris menambahkan Timeline & Approval
   secara manual setelahnya.

## Export & Install
- Bundle zip: `python3 <skill_dir>/scripts/export_bundle.py` → `<skill_dir>/dist/<name>-<version>.zip`
  (tanpa `.venv`; cetak SHA256). Unzip di target, lalu jalankan `scripts/bootstrap.py`.
- Dari GitHub: `hermes skills install <raw-url>/SKILL.md --yes` — installer mengambil
  SKILL.md + file yang direferensi di body (`references/`, `templates/`, `scripts/`).
  **Jangan hapus referensi file pendukung dari body**; kalau dihapus, file itu tidak
  ikut ter-install.
- Jalur lengkap + alternatif yang tidak jalan: `references/publish.md`.
- Ringkas untuk manusia: `[INSTALL.md](./INSTALL.md)`.

## Pitfalls
- Jangan tulis nomor section otomatis Word (numPr) — house-style pakai numbering
  manual diketik ("1. Document Control").
- Zebra tabel: DBE5F1/FFFFFF harus strict alternation per item row — dokumen
  sumber punya beberapa row tanpa fill; itu bug template, jangan ditiru.
- Spec table & Timeline & Approval bukan scope v1 skill ini.
- Item software di spec table pakai GAMBAR="N/A" — hanya relevan di section 5 (out of scope), dicatat untuk v2 catalog.
- URS fleksibel jumlahnya (bukan wajib 10) — keputusan user.
- `.venv` sengaja tidak ikut bundle/zip — dibangun ulang oleh `scripts/bootstrap.py`
  di mesin target. Copy manual tanpa bootstrap → `ModuleNotFoundError: docx`.
- Skill lokal (source `local`) tidak ikut `hermes skills snapshot export`; pakai
  `scripts/export_bundle.py` atau install-URL, lihat `references/publish.md`.

## Verification
- `scripts/qc.py output.docx` → "QC PASS" + 0 error
- Buka ulang output dengan python-docx → struktur section 1-4 lengkap & urut
- Struktural (dev, opsional): `scripts/_verify_dev.py <output.docx>` (set `SP_REF_DOCX`
  untuk membandingkan dengan dokumen referensi Pusdatin CSM v1.3 bila tersedia)
- Negative test (dev): `scripts/_negtest_dev.py` → 9 kasus input invalid ditolak
- Pasca-install di mesin baru: `scripts/bootstrap.py` → `venv OK`, lalu `scripts/qc.py`
  pada `templates/sample-output.docx` → `QC PASS`
