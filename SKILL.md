---
name: solution-pack-creator
description: "Generate dokumen Solution Pack .docx section 1-4 sesuai house-style b2b-id."
version: 1.3.0
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
atau input user — skill ini men-standardisasi **struktur, layout, dan styling**, bukan
menulis konten otomatis.

Status: **v1.3.0 — house style v1.2 + writing-quality gate**. Style set dari
`Solution Pack Pussiberad 2027 V1.1` + watermark draft & footer dari V1.2. Sejak v1.3.0
setiap draft wajib lewat writing-quality pass (skill `avoid-ai-writing`) sebelum generate.
QC + verifikasi struktur lolos; sample output: `templates/sample-output.docx`.

## File pendukung (sebut eksplisit di sini supaya ikut ter-install di harness yang hanya
menarik file yang direferensikan)
- `references/style-spec.md` — spec house style v1.1 (acuan styling section 1-4).
- `references/style-spec-v0-pusdatin-legacy.md` — arsip spec lama (Pusdatin CSM v1.3); masih
  acuan layout Spec Table section 5 & Approval Table section 6 (manual oleh Chris).
- `references/input-schema.md` — skema JSON input. `references/qc-checklist.md` — checklist QC.
- `references/publish.md` + `INSTALL.md` + `requirements.txt` — distribusi & dependency.
- `scripts/bootstrap.py` — bikin `.venv` + install requirement; `scripts/export_bundle.py` —
  bikin bundle zip di `dist/`; `scripts/_negtest_dev.py` — test input invalid.
- `scripts/prose_blocks.py` — ekstrak / tulis-balik blok prosa JSON untuk writing-quality pass.
- `templates/house-style-template.docx`, `templates/sample-input.json`,
  `templates/sample-output.docx`, `scripts/generate.py`, `scripts/qc.py`,
  `scripts/_verify_dev.py`.

## Lokasi file & status dokumen (aturan kerja)
- **Default setiap dokumen Solution Pack = DRAFT.** Kerjakan dan simpan di
  `/opt/data/<project>/temp/`.
- Dokumen **PRODUKSI** ada di `/opt/data/<project>/main/`. Naik dari draft ke produksi
  **hanya kalau user bilang eksplisit** (mis. "naikin jadi versi produksi"). Jangan pernah
  menaikkan status sendiri, jangan menaruh draft baru langsung di `main/`.
- `<project>` = nama project yang dikerjakan (mis. `Pussiberad`), sejalan dengan nama folder
  project di vault (`/vaults/obsidian/<Project>/`).
- Arsip/deliverable juga di-mirror ke vault project. Vault ada di luar write-safe root:
  tulis lewat staging di `/opt/data` lalu `cp` ke vault.
- Saat menyerahkan dokumen ke user: sebutkan **status (draft/produksi) + path**-nya.

## When to Use
- User minta bikin / draft / revisi dokumen Solution Pack untuk leads b2b-id.
- Jangan untuk: dokumen selain Solution Pack, atau bagian Timeline & Approval / spec table.

## Prerequisites
- **`<skill_dir>` = folder tempat `SKILL.md` ini berada** (hasil clone/unzip/install). Semua
  perintah di bawah relatif ke folder itu — skill ini tidak menyimpan absolute path.
- venv skill: `<skill_dir>/.venv` (python-docx). Cara termudah:
  `python3 <skill_dir>/scripts/bootstrap.py` (otomatis pakai `uv` kalau tersedia, fallback ke
  `python -m venv` + pip). Manual: `uv venv <skill_dir>/.venv && uv pip install --python
  <skill_dir>/.venv/bin/python python-docx`
- Template house style: `templates/house-style-template.docx` (**wajib ada**). Generator
  menolak jalan kalau file ini hilang. Cara regenerasi template dari file acuan: buka docx
  acuan, ambil `sectPr`, ganti isi `word/document.xml` jadi `<w:body>{sectPr}</w:body>`,
  pertahankan part lain apa adanya (styles/numbering/theme).
- Style acuan: `references/style-spec.md`.
- **Skill `avoid-ai-writing`** (skill terpisah, wajib untuk writing-quality pass). Resolve
  folder skill-nya dari daftar skill profil yang aktif — jangan hardcode path. Kalau belum
  ter-install, install dulu; jangan melewati pass ini diam-diam.
- Konten: dokumen MoM/requirement (PDF) + input user. Di setup Hermes Chris, sumbernya ada
  di vault Obsidian (`<vault>/<project>/RO/`); di harness atau mesin lain, pakai file yang
  diberikan user. Path vault itu contoh konteks, bukan syarat.

## How to Run
1. Kumpulkan konten → susun JSON sesuai `references/input-schema.md`.
2. Writing quality pass (wajib) di JSON — lihat section di bawah — **sebelum** generate.
3. Generate:
   `<skill_dir>/.venv/bin/python <skill_dir>/scripts/generate.py <input.json> <output.docx>`
4. QC wajib sebelum dikirim ke user:
   `<skill_dir>/.venv/bin/python <skill_dir>/scripts/qc.py <output.docx>`  → harus "QC PASS".
5. Opsional (verifikasi dalam): `scripts/_verify_dev.py <output.docx>` → "ALL PASS".

## Quick Reference
```
# <skill_dir> = folder tempat SKILL.md ini berada
cd "<skill_dir>"
python3 scripts/bootstrap.py                          # sekali saja: bikin .venv + python-docx
python3 scripts/prose_blocks.py input.json --extract prose.txt    # writing-quality pass
# audit + tulis ulang prose.txt (skill avoid-ai-writing), lalu:
python3 scripts/prose_blocks.py input.json --apply prose.txt
.venv/bin/python scripts/generate.py input.json out.docx
.venv/bin/python scripts/qc.py out.docx
.venv/bin/python scripts/_verify_dev.py out.docx
```
Di Windows interpreter-nya `.venv\Scripts\python.exe`.

## Kompatibilitas harness
Skill ini harness-agnostic — cuma butuh **Python 3.9+** dan **python-docx**
(lihat `requirements.txt`). Semua `scripts/*.py` me-resolve path relatif ke folder skill
(`Path(__file__)`), jadi tidak ada absolute path di kode. Cara pakai di harness selain Hermes
(mis. commandcode, Claude Code, Codex): copy/clone folder skill → `python3 scripts/bootstrap.py`
→ jalankan script seperti di Quick Reference. Yang Hermes-specific hanya `INSTALL.md` dan
`references/publish.md` (cara install ke Hermes); sisanya berlaku umum.

## Style House v1.1 (ringkas — detail di `references/style-spec.md`)
- Judul dokumen → style `Title`; section 1–4 → `Heading 1`; sub-section → `Heading 2`.
- Body → `Normal - H2`; bullet → `Bullet List - H2`; sel tabel → `Table - Item` /
  `Table - Description`. **Jangan** pakai `Normal`, `List Bullet`, atau `Heading 3`.
- Font dari theme (Calibri heading / Cambria body) — jangan set font/size langsung di body.
- Tabel: style `Normal Table` + border manual #9FBAD0, fill label #E9ECEF, header #4F81BD,
  zebra #DBE5F1/#FFFFFF.
- Kolom **No URS auto-numbering** (numId 7), bukan angka manual.
- **Setiap `Heading 1` mulai di halaman baru**: section 2–4 didahului paragraf kosong berisi
  manual page break (section 1 tetap di halaman judul).
- **Watermark & footer wajib**: setiap halaman punya watermark `DRAFT` (diagonal, abu-abu)
  dan footer `Internal Draft - S03 Approval Use Only` (rata tengah). Override lewat
  `meta.watermark_text` / `meta.footer_text` (kosong = tanpa).

## Writing quality pass (wajib) — skill `avoid-ai-writing`
Menghapus pola tulisan khas AI dari **prosa** dokumen. Bukan urusan struktur/styling — itu
urusan generator. Pass ini dikerjakan di **JSON**, bukan di file .docx: prosa yang diperbaiki
lalu di-generate ulang, supaya hasilnya tetap reproducible dari input.

Prosedur:
1. **Ekstrak prosa**: `python3 <skill_dir>/scripts/prose_blocks.py <input.json> --extract prose.txt`.
   Blok diambil dalam urutan dokumen (customer background, problem statement, objectives,
   deskripsi URS, deployment context, solution overview). Identifier/nama tidak ikut.
2. **Audit + tulis ulang** `prose.txt` mengikuti skill `avoid-ai-writing`, mode `rewrite`.
   Profil yang cocok: konteks `docs`, voice `professional`.
3. **Tulis balik**: `python3 <skill_dir>/scripts/prose_blocks.py <input.json> --apply prose.txt`.
   Exit 2 = jumlah blok berubah — script sengaja menolak, karena itu pengaman urutan blok.
4. **Verifikasi mekanis**, original vs hasil, dari folder skill `avoid-ai-writing`:
   - `node detector/validate.js <original-prose.txt> <rewritten-prose.txt>` → harus `PASS`.
   - `node scripts/normalize-quotes.js <rewritten> --reference <original> --write` (marks pass).
   - Detector: `detector/patterns.js` diekspor sebagai module tanpa CLI — panggil
     `AIDetector.analyzeText(text, { contextMode })` dari helper Node kecil.
5. Baru generate .docx, lalu `qc.py` seperti biasa.
6. **Laporkan ke user**: finding utama, hasil verifikasi, dan residual yang tersisa
   (termasuk yang sengaja dipertahankan). Sediakan review copy prosa kalau diminta.

Yang **tidak** boleh diubah pass ini:
- Bab 1 Document Control — isinya kode/identifier/status, bukan prosa. Field yang wajar
  berubah hanya `meta.version` (naikkan tiap revisi: `V<x.y> (changelog)`).
- `meta.*`, `urs[*].name` (label requirement), `solution.name`, `solution.category`.
- Enumerasi spesifikasi (daftar perangkat deteksi, daftar PPE) — list-shaped content,
  memang begitu bentuknya.
- Label house style `Catatan operasional:` — konvensi dokumen acuan, pertahankan.
- Nomor/volume boleh dipindah ke spec table (bab 5) kalau memang di sana tempatnya, tapi
  keputusan itu harus dilaporkan eksplisit ke user, bukan dilakukan diam-diam.

## Procedure
1. **Kumpulkan konten** — MoM/requirement. Selesaikan ambiguitas (customer, end user,
   solusi, URS) sebelum lanjut; jangan mengarang konten. Selesai: semua field wajib terisi
   atau ditandai TBD.
2. **Susun input JSON** sesuai `references/input-schema.md`. Field struktur (12 label
   Document Control, urutan section, tabel 4.1 4 baris) dipaksa generator. Selesai: JSON
   parse & valid (generator exit 2 kalau tidak).
3. **Writing quality pass** — `scripts/prose_blocks.py` extract → audit + tulis ulang pakai
   skill `avoid-ai-writing` → apply. Selesai: jumlah blok sama, JSON valid, validator
   preservation `PASS`.
4. **Generate .docx** → simpan sebagai **draft** di `/opt/data/<project>/temp/`.
   Selesai: file ada, terbuka dengan python-docx, exit 0.
5. **QC** — `scripts/qc.py` harus "QC PASS: no issues", lalu review visual
   `references/qc-checklist.md`. Selesai: QC pass, path output dilaporkan ke user.
6. **Serahkan** — kirim docx ke user; Chris menambahkan spec table + Timeline & Approval.

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
- Section 2–4 wajib didahului **paragraf kosong + manual page break** (`_new_page(doc)` di
  generator) supaya H1 selalu di awal halaman. Jangan pakai `pageBreakBefore` di style
  Heading 1 — file acuan pakai manual break, dan itu yang dicek `qc.py`.
- Spec table (section 5) & Approval table (section 6) di luar scope generator — jangan
  ditambahkan ke output. Layout-nya (bila perlu diedit manual) ada di
  `references/style-spec-v0-pusdatin-legacy.md`.
- **Jangan mengangkat status dokumen sendiri.** Output baru selalu draft di
  `/opt/data/<project>/temp/`; `main/` hanya diisi setelah user memerintahkan naik ke produksi.
- URS fleksibel jumlahnya (bukan wajib 10) — keputusan user.
- **Writing pass dikerjakan di JSON, bukan di .docx.** Mengedit prosa langsung di file Word
  bikin hasil lepas dari generator dan tidak reproducible; perbaiki di JSON lalu generate ulang.
- **Katalog `avoid-ai-writing` itu English-centric.** Untuk konten Indonesia, terapkan **per
  pola** — opener seragam, klaim kepentingan tanpa dasar, pivot "bukan X tapi Y", restatement,
  em dash, synonym cycling, rule-of-three — jangan mencocokkan word-list Inggris. Detector-nya
  hanya andal untuk cek struktural/stilometrik (TTR, burstiness, em dash).
- **Writing pass tidak mengubah status dokumen.** Output tetap draft di
  `/opt/data/<project>/temp/`; kenaikan versi cuma di `meta.version`.
- `scripts/prose_blocks.py --apply` exit 2 = jumlah blok beda. Perbaiki file teksnya (blok
  dipisah baris kosong), jangan menggabung/memecah blok supaya jumlahnya cocok. Kalau 0 field
  berubah, script tidak menulis file JSON sama sekali; kalau ada perubahan, formatting JSON
  dinormalisasi (indent 2) — diff formatting itu wajar, bukan prosa yang berubah.
- **Jangan menaruh absolute path** (`/opt/data/...`, `/Users/...`, `/vaults/...`) di SKILL.md,
  `references/`, atau `scripts/`. Pakai `<skill_dir>` atau path relatif supaya skill tetap
  jalan di harness lain (commandcode, Claude Code, Codex, dll).

## Verification
- `scripts/qc.py output.docx` → "QC PASS" (0 issue). Tambah `--final` kalau dokumen sudah
  digabung dengan Spec Table/Approval manual.
- `scripts/_verify_dev.py output.docx` → "ALL PASS" (struktur XML, style, lebar kolom,
  border, margin, auto-numbering URS).
- `templates/sample-output.docx` = output acuan dari `templates/sample-input.json`.
- `scripts/prose_blocks.py <input.json> --extract <out.txt>` lalu `--apply` file yang sama →
  harus "0 field berubah" (round-trip bersih; bukti blok tidak tertukar posisi).
- Writing pass: `detector/validate.js` (skill `avoid-ai-writing`) → `PASS` antara prosa
  original dan hasil. Warning yang tersisa (mis. `number-missing`) dilaporkan beserta
  alasannya, bukan diabaikan.
