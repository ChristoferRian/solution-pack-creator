# Input Schema — Solution Pack Generator (v1)

JSON input untuk `scripts/generate.py`. Tipe field konten: string bebas (agent
mengisi dari MoM/user input). Field yang TIDAK ada di JSON → generator error.
TBD diperbolehkan sebagai nilai string "TBD".

```json
{
  "meta": {
    "title": "PENGADAAN ... T.A 2027",          // line kedua judul (bold 10.5pt #333333, center)
    "document_code": "SPD-<CUSTOMER>-<SOLUTION>-<YEAR>",   // pola wajib
    "project_code": "PRJ-<CUSTOMER>-<SOLUTION>-<YEAR>",    // mirror document_code
    "reference_lead_code": "TBD" | "LD-<CUSTOMER>-<SOLUTION>-<YEAR>-<SEQ>",
    "lead_name": "",
    "customer_name": "Kementerian ... / Paspampres / ...",
    "end_user": "...",
    "year_semester_delivery": "2027 | TBD",
    "version": "V1.0 (init)",                    // format: V<x.y> (changelog) — [a-z] tidak dipakai
    "document_owner": "PreSales / PGO",          // default
    "document_status": "Draft for S03 Review",   // default
    "branding_rule": ""
  },
  "background": {
    "customer_background": "paragraf ...",       // 1-3 paragraf
    "problem_statement": ["paragraf 1", "paragraf 2"],  // array paragraf
    "objectives": ["Menyediakan ...", "Mendukung ..."]  // bullet list
  },
  "urs": [
    { "name": "IMSI Radar", "description": "Mendeteksi ..." },
    ...
  ],
  "solution": {
    "name": "Integrated ... System",
    "category": "...",
    "deployment_context": "...",
    "overview": ["paragraf 1", "paragraf 2"]     // Solution Overview, array paragraf
  }
}
```

## Aturan

1. **meta.title** — baris kedua dokumen (di bawah H1 "SOLUTION PACK DOCUMENT").
   Kapital, deskriptif, mengandung nama pengadaan + tahun anggaran.
2. **document_code / project_code** — pola `SPD-`/`PRJ-` + customer short + solution short + year. Project code = mirror document code (ganti prefix).
3. **version** — `V<major>.<minor>` + changelog dalam kurung. Contoh: `V1.0 (initial draft)`. Jangan "v0.4" (huruf kecil, tanpa changelog) — inkonsistensi dokumen lama.
4. **urs** — fleksibel jumlahnya (sample: 10). name = nama requirement (bold di tabel), description = deskripsi lengkap.
5. **solution.overview** — paragraf paragraf overview; paragraf terakhir biasanya catatan operasional (SOP/kewenangan) bila solusinya sensitif (jammer/counter-UAS) — ikuti pola ini.
6. Semua field di atas wajib. Nilai kosong string diperbolehkan (mis. lead_name, branding_rule), "TBD" diperbolehkan.
7. Konten bebas — agent menyusun dari MoM vault / input user. Generator hanya memvalidasi struktur, bukan kualitas konten.
8. **Jangan letakkan spec table / timeline / approval di JSON ini** — out of scope v1.
9. **meta.title dipakai untuk document properties saja** (title file), TIDAK tampil di body.
   Dokumen hanya punya satu baris judul: "SOLUTION PACK DOCUMENT" (style `Title`).
   Jangan menambahkan baris judul pengadaan — keputusan Chris untuk house style v1.1.
10. **meta.watermark_text** (default `"DRAFT"`) dan **meta.footer_text**
    (default `"Internal Draft - S03 Approval Use Only"`) mengatur watermark header & teks
    footer. Isi string kosong (`""`) kalau ingin tanpa watermark / tanpa footer — mis. untuk
    dokumen yang sudah berstatus produksi.

## Defaults

Kalau user tidak menentukan:
- `document_owner`: "PreSales / PGO"
- `document_status`: "Draft for S03 Review"
- `reference_lead_code`, `year_semester_delivery`: "TBD"
- `lead_name`, `branding_rule`: ""
