# Export & Install — Solution Pack Creator (khusus Hermes)

> **File ini Hermes-specific.** Untuk harness lain (commandcode, Claude Code, Codex, dll.),
> cukup copy/clone folder skill lalu `python3 <skill_dir>/scripts/bootstrap.py` — lihat
> `INSTALL.md` bagian "Cara umum". Tidak ada path yang di-hardcode di script.

Dua jalur distribusi. Jalur A offline (bundle zip), jalur B online (install dari
URL raw GitHub).

## Jalur A — Bundle zip (offline, paling portable)

Di mesin sumber:

```
python3 <skill_dir>/scripts/export_bundle.py            # -> <skill_dir>/dist/solution-pack-creator-<ver>.zip
python3 <skill_dir>/scripts/export_bundle.py /tmp/sp.zip  # atau path custom
```

Script mencetak ukuran + SHA256. Bundle **tidak** memuat `.venv` (di-rebuild di
sisi target), `dist/`, `__pycache__`, `.git`.

Di mesin target:

```
unzip -o solution-pack-creator-<versi>.zip -d "$HERMES_HOME/skills/productivity/"
python3 "$HERMES_HOME/skills/productivity/solution-pack-creator/scripts/bootstrap.py"
python3 "$HERMES_HOME/skills/productivity/solution-pack-creator/scripts/qc.py" \
        "$HERMES_HOME/skills/productivity/solution-pack-creator/templates/sample-output.docx"
```

`bootstrap.py` bikin `.venv` (prefer `uv`, fallback `python -m venv`) + install
`requirements.txt`. `qc.py` harus cetak `QC PASS`. Skill ke-load di session
berikutnya (loader Hermes cache di awal session — ini normal, bukan bug).

## Jalur B — Install dari URL (GitHub raw)

Push folder skill ke repo GitHub dengan layout `<repo>/<path>/solution-pack-creator/`,
lalu di mesin target:

```
hermes skills install \
  https://github.com/<owner>/<repo>/raw/<branch>/<path>/solution-pack-creator/SKILL.md --yes
```

Installer URL Hermes (lihat `tools/skills_hub_sources.py::UrlSource.fetch`) mengambil
`SKILL.md` **plus** file pendukung yang direferensi di body dengan pola
`references/…`, `templates/…`, `scripts/…`, `assets/…`, `examples/…` (dan link
se-dir `](./file.ext)`). Karena itu SKILL.md menyebut **setiap** file pendukung
secara eksplisit — jangan hapus referensinya, kalau tidak file itu tidak ikut
ter-install.

Batasan yang perlu diingat:
- Traversal (`../`) bikin install gagal — jangan pakai path keluar folder.
- File di luar direktori allowlist (mis. `requirements.txt` di root, `INSTALL.md`)
  hanya ikut kalau ditulis sebagai link se-dir `](./file`)`/`](file)`.
- `.venv` tidak pernah ikut; jalankan `scripts/bootstrap.py` setelah install.
- Install URL = trust `community`; verifikasi dengan `qc.py` sebelum dipakai.

## Alternatif yang TIDAK jalan

- `hermes skills snapshot export` hanya meng-export entri registry/lockfile
  (skill yang di-install dari hub/URL). Skill lokal murni (source `local`)
  tidak ikut. Pakai jalur A atau B di atas.
- Copy manual folder tanpa `bootstrap.py` → `ModuleNotFoundError: docx`.

## Verifikasi pasca-install

1. `python3 <skill_dir>/scripts/bootstrap.py` → cetak `venv OK: …`
2. `python3 <skill_dir>/scripts/qc.py <skill_dir>/templates/sample-output.docx` → `QC PASS`
3. Optional re-check struktural: `python3 <skill_dir>/scripts/_verify_dev.py <sample.docx>`
4. Session Hermes baru → `skill_view(name='solution-pack-creator')` mengembalikan isi SKILL.md.
