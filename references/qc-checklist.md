# QC Checklist — Solution Pack Output

Jalankan `scripts/qc.py` dulu (otomatis). Lalu review visual berikut:

1. **Halaman judul**: H1 "SOLUTION PACK DOCUMENT" center navy; baris judul
   pengadaan bold center abu-abu gelap (#333333), kapital, ada tahun anggaran.
2. **Document Control**: 12 baris, kolom label shaded #E9ECEF bold; TBD
   diperbolehkan (Reference Lead Code, Year & Semester); Lead Name &
   Branding Rule boleh kosong.
3. **Version**: format `V<x.y> (changelog)` — bukan `v0.4`.
4. **Kode**: `SPD-...` dan `PRJ-...` mirror; lead code `LD-...` atau TBD.
5. **Background**: 2.1 & 2.2 paragraf naratif mengalir (bukan bullet);
   2.3 berbentuk bullet list.
6. **URS**: header biru #4F81BD teks putih bold, zebra #DBE5F1/#FFFFFF mulai
   DBE5F1 di baris data pertama, nomor sequential, kolom No center.
7. **4.1**: 4 baris (header Item|Description + Solution Name / Solution
   Category / Deployment Context), kolom label #E9ECEF bold.
8. **4.2**: overview paragraf; kalau solusi sensitif (jammer, counter-UAS,
   IMSI) harus ada paragraf catatan operasional (SOP/kewenangan) di akhir.
9. **Scope**: TIDAK ada section 5 (spec table) / 6 (approval) — itu dikerjakan
   manual oleh Chris. Jangan menambahkannya.
10. **Typo terlarang** (dari dokumen lama — jangan sampai kebawa): stationery
    (→stationary), Algorhytm (→Algorithm), One Tme Pad, Spesfikasi, Anlyzer,
    Chipper (→cipher).
11. **Konsistensi font**: heading navy #123555 bold, body #222222, tabel 7-8pt.
12. **Buka di Word/LibreOffice**: header row URS terulang saat tabel pindah
    halaman, tabel tidak melewati margin kanan, tidak ada baris kosong nyangkut.
