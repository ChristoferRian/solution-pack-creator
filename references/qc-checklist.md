# QC Checklist — Solution Pack Output (house style v1.1)

Jalankan `scripts/qc.py` dulu (otomatis: struktur, style, fill, theme).
Lalu review visual ini:

1. **Judul**: baris "SOLUTION PACK DOCUMENT" pakai style `Title` — Calibri bold 24pt,
   warna #17375E, rata tengah (bukan Heading 1).
2. **Section 1–4** pakai `Heading 1` (16pt, #123555); sub-section (2.1/2.2/2.3/4.1/4.2)
   pakai `Heading 2` (14pt, #1F497D, indent 2 ch). Tidak boleh ada `Heading 3`.
3. **Body** pakai `Normal - H2` (Cambria 11pt, justify, first-line indent 0.19"),
   **bullet 2.3** pakai `Bullet List - H2`. Tidak ada paragraf ber-style `Normal`.
4. **Document Control**: 12 baris; label #E9ECEF bold; teks 10pt; TBD boleh di
   Reference Lead Code & Year/Semester; Lead Name & Branding Rule boleh kosong.
5. **Version**: `V<x.y> (changelog)` — bukan `v0.4`.
6. **Kode**: `SPD-...` dan `PRJ-...` mirror; lead code `LD-...` atau TBD.
7. **URS**: header biru #4F81BD teks putih bold 10pt; kolom No auto-numbering
   (tampil "1.", "2.", …); zebra #DBE5F1/#FFFFFF mulai DBE5F1; nama sel pakai
   `Table - Item` (bold), deskripsi `Table - Description`; header ulang saat pindah halaman.
8. **4.1**: 4 baris (header Item|Deskripsi + Solution Name / Solution Category /
   Deployment Context), kolom label #E9ECEF bold.
9. **4.2**: overview paragraf; kalau solusi sensitif (jammer, counter-UAS, IMSI) wajib ada
   paragraf catatan operasional (SOP/kewenangan) di akhir.
10. **Scope**: TIDAK ada section 5 (spec table) / 6 (approval) — dikerjakan manual oleh Chris.
11. **Typo terlarang**: stationery (→stationary), Algorhytm (→Algorithm), One Tme Pad,
    Spesfikasi, Anlyzer, Chipper (→cipher).
12. **Buka di Word**: theme Calibri/Cambria aktif, tabel tidak melewati margin, tidak ada
    baris kosong nyangkut, dan navigation pane rapi (Title → Heading 1 → Heading 2).
13. **Page break antar section**: section 2, 3, dan 4 masing-masing mulai di halaman baru —
    di kode XML terlihat sebagai paragraf kosong dengan `<w:br w:type="page"/>` tepat sebelum
    tiap `Heading 1` (section 1 tetap di halaman judul).
14. **Watermark & footer**: setiap halaman punya watermark teks `DRAFT` (diagonal, abu-abu,
    Arial Unicode MS 36pt) dan footer `Internal Draft - S03 Approval Use Only` (8pt, #5A5A5A,
    rata tengah). Cek di Word: watermark harus muncul di **semua** halaman (bukan cuma ganjil).

Catatan: `qc.py` punya mode `--final` untuk dokumen yang sudah ditambah bagian manual
(Spec Table / Approval Section) — tabel >3 diizinkan dan bagian setelah section 4 tidak
dicek gaya paragrafnya.
