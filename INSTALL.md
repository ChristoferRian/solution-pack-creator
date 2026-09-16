# Install — Solution Pack Creator

Skill ini **harness-agnostic**: cuma butuh **Python 3.9+** dan **python-docx**.
`<skill_dir>` = folder tempat `SKILL.md` ini berada. Tidak ada path yang di-hardcode.

## Cara umum (semua harness / mesin)

```bash
# 1. taruh folder skill di mana saja (clone repo atau unzip bundle)
# 2. siapkan venv + dependency (sekali saja)
python3 <skill_dir>/scripts/bootstrap.py
# 3. verifikasi
python3 <skill_dir>/scripts/qc.py <skill_dir>/templates/sample-output.docx
```

Harus berakhir `QC PASS`. Setelah itu pakai seperti di `SKILL.md` (Quick Reference).

Dari bundle zip (mis. hasil `scripts/export_bundle.py` atau lampiran GitHub release):

```bash
unzip -o solution-pack-creator-<versi>.zip -d <folder-tujuan>
python3 <folder-tujuan>/solution-pack-creator/scripts/bootstrap.py
```

Harness lain (commandcode, Claude Code, Codex, dll.) cukup memakai folder skill ini apa
adanya — interpreter-nya `<skill_dir>/.venv/bin/python` (Windows: `.venv\Scripts\python.exe`).

## Hermes (opsional)

Kalau dipasang sebagai skill Hermes:

```bash
unzip -o solution-pack-creator-<versi>.zip -d "$HERMES_HOME/skills/productivity/"
python3 "$HERMES_HOME/skills/productivity/solution-pack-creator/scripts/bootstrap.py"
python3 "$HERMES_HOME/skills/productivity/solution-pack-creator/scripts/qc.py" \
        "$HERMES_HOME/skills/productivity/solution-pack-creator/templates/sample-output.docx"
```

Atau dari URL raw GitHub:

```bash
hermes skills install \
  https://github.com/ChristoferRian/solution-pack-creator/raw/main/SKILL.md --yes
python3 "$HERMES_HOME/skills/productivity/solution-pack-creator/scripts/bootstrap.py"
```

Skill ke-load di session Hermes berikutnya. Detail distribusi: `references/publish.md`.

## Ekspor ulang (maintainer)

```bash
python3 <skill_dir>/scripts/export_bundle.py               # -> <skill_dir>/dist/<name>-<version>.zip
python3 <skill_dir>/scripts/export_bundle.py /tmp/sp.zip   # atau path custom
```

## Requirements

- Python 3.9+
- `python-docx` (lihat `requirements.txt`; `bootstrap.py` mengurusnya)
- `uv` opsional (lebih cepat); fallback `python -m venv` + `pip`
