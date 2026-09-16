# Solution Pack Creator

> Skill ini berfungsi untuk menjadi guideline membuat Solution Pack document dari
> bab 1–4. Bab 5-nya biarkan user isi sendiri.

Hermes skill untuk generate dokumen **Solution Pack `.docx`** (section 1–4) sesuai
house-style b2b-id, dikunci ke **house style v1.1** (style set diambil dari dokumen
`Solution Pack Pussiberad 2027 V1.1.docx`).

- **Section yang dibuat:** 1. Document Control, 2. Project Background,
  3. User Requirement Summary, 4. Proposed Solution
- **Bukan scope skill ini:** spec table (section 5), Timeline & Approval (section 6) — manual
- **Status:** v1.1.1 — house style v1.1, tested & QC-passed (QC struktur + 9 negative input test)

Skill ini **harness-agnostic**: cuma butuh Python 3.9+ dan `python-docx`, dan tidak ada
absolute path yang di-hardcode (semua script me-resolve path relatif ke folder skill).
Command di seluruh dokumen memakai placeholder `<skill_dir>` = folder tempat `SKILL.md`
berada. Bagian yang Hermes-specific (`INSTALL.md`, `references/publish.md`) ditandai jelas.

Skill ini men-standardisasi **struktur, layout, dan styling**, bukan menulis konten
otomatis. Isi konten (customer, URS, solution name, dst) tetap disusun dari
MoM/requirement di vault Obsidian atau input user.

## Install

Repo ini adalah skill-nya langsung — `SKILL.md` ada di root, jadi bisa di-install
langsung dari raw URL:

```bash
hermes skills install \
  https://raw.githubusercontent.com/<owner>/<repo>/main/SKILL.md --yes
```

Lalu siapkan venv-nya (portable, butuh Python 3.9+):

```bash
python3 <skill_dir>/scripts/bootstrap.py
```

Verifikasi:

```bash
python3 <skill_dir>/scripts/qc.py \
        <skill_dir>/templates/sample-output.docx
```

Harus berakhir `QC PASS`.

## Pakai

```bash
# setup / repair venv
python3 <skill_dir>/scripts/bootstrap.py

# generate dari input JSON (skema: references/input-schema.md)
<skill_dir>/.venv/bin/python <skill_dir>/scripts/generate.py <input.json> <output.docx>

# QC struktur — wajib pass sebelum dikirim
<skill_dir>/.venv/bin/python <skill_dir>/scripts/qc.py <output.docx>

# export bundle zip buat dipindah ke Hermes lain
python3 <skill_dir>/scripts/export_bundle.py
```

Contoh input lengkap: [`templates/sample-input.json`](templates/sample-input.json).
Contoh output: [`templates/sample-output.docx`](templates/sample-output.docx).

## Isi Repo

| Path | Isi |
|---|---|
| `SKILL.md` | Definisi skill, procedure, pitfalls, verification |
| `INSTALL.md` | Instalasi ringkas untuk manusia |
| `references/style-spec.md` | Spec house style v1.1 (acuan styling section 1–4) |
| `references/style-spec-v0-pusdatin-legacy.md` | Arsip spec lama (Pusdatin CSM v1.3); acuan layout Spec Table & Approval |
| `references/input-schema.md` | Skema input JSON |
| `references/qc-checklist.md` | Checklist QC output |
| `references/publish.md` | Cara export & install ke Hermes lain |
| `scripts/generate.py` | Generator `.docx` section 1–4 (berbasis template house style) |
| `scripts/qc.py` | QC struktur + style output |
| `scripts/bootstrap.py` | Bikin/repair venv + install dependency |
| `scripts/export_bundle.py` | Packaging zip untuk dipindah |
| `scripts/_verify_dev.py`, `scripts/_negtest_dev.py` | Test dev (opsional) |
| `templates/house-style-template.docx` | Template house style (styles/numbering/theme) — **wajib ada** untuk generate |
| `templates/` | Sample input & output |

## Requirements

- Python 3.9+
- `python-docx` (lihat [`requirements.txt`](requirements.txt); `bootstrap.py` mengurusnya)
- `uv` opsional (lebih cepat); fallback `python -m venv` + `pip`

## Catatan

- `.venv` sengaja tidak di-commit — dibangun ulang oleh `scripts/bootstrap.py`.
  Copy manual tanpa bootstrap → `ModuleNotFoundError: docx`.
- Bundle zip di `dist/` juga tidak di-commit (build artifact).

## License

MIT — lihat [`LICENSE`](LICENSE).
