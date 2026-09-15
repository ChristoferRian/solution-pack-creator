# Install — Solution Pack Creator

Skill lokal Hermes (category `productivity`). Detail lengkap: `references/publish.md`.

## Dari bundle zip

```bash
unzip -o solution-pack-creator-1.0.0.zip -d "$HERMES_HOME/skills/productivity/"
python3 "$HERMES_HOME/skills/productivity/solution-pack-creator/scripts/bootstrap.py"
python3 "$HERMES_HOME/skills/productivity/solution-pack-creator/scripts/qc.py" \
        "$HERMES_HOME/skills/productivity/solution-pack-creator/templates/sample-output.docx"
```

Harus berakhir `QC PASS`. Skill ke-load di session Hermes berikutnya.

## Dari GitHub (raw URL)

```bash
hermes skills install \
  https://github.com/<owner>/<repo>/raw/<branch>/<path>/solution-pack-creator/SKILL.md --yes
python3 "$HERMES_HOME/skills/productivity/solution-pack-creator/scripts/bootstrap.py"
```

## Ekspor ulang

```bash
python3 <skill_dir>/scripts/export_bundle.py            # -> <skill_dir>/dist/<name>-<version>.zip
```

## Requirements

- Python 3.9+
- `python-docx` (lihat `requirements.txt`; `bootstrap.py` mengurusnya)
- `uv` opsional (lebih cepat); fallback `python -m venv` + `pip`
