# Solution Pack — Style Spec (Reference: Pusdatin CSM v1.3.docx)

Locked decision: semua dokumen Solution Pack hasil generate ikut styling dokumen
"Solution Pack Pusdatin Counter Surveillance Mobile v1.3.docx".

## Page Setup
- Ukuran: Letter (12240 x 15840 dxa / 8.5" x 11")
- Margin: top 1300, right 720, bottom 520, left 720 dxa (≈ top 2.29cm, samping 1.27cm, bottom 0.92cm)
- Header/footer: kosong, no page number

## Teks
| Elemen | Font | Size (half-pt -> pt) | Warna | Lain |
|---|---|---|---|---|
| Heading1 (judul dok) | Arial | 40 -> 20pt | #123555 | Bold, CENTER |
| Heading2 (section 1-6) | Calibri | 23 -> 11.5pt | #123555 | Bold, numbering manual diketik ("1. Document Control") |
| Heading3 (2.1 dst) | Calibri | 19 -> 9.5pt | #123555 | Bold, numbering manual |
| Body/Normal | Calibri | 16 -> 8pt | #222222 | spacing after=60, line=252 auto |
- Indent legacy H2: left 514 hanging 719; H3: left 635 hanging 419
- Heading style family table: TableContents / TableHeading (bold, center) / TableParagraph

## Warna Palet
- Navy heading: #123555
- Body text: #222222
- Border tabel: single sz=4 (0.5pt) #9FBAD0 — semua tabel
- Header row tabel: fill #4F81BD, teks bold 7pt (7pt = sz 14)
- Group Roman (I./II.): fill #1F4E79, gridSpan penuh, bold 7pt
- Sub-group letter (A./B.): fill #4F81BD, 1 sel full-width, bold 7pt
- Label col DocControl & 4.1: fill #E9ECEF
- Zebra data row spec: #DBE5F1 / #FFFFFF bergantian per item
- Header text URS & Approval: white #FFFFFF bold (spec header di dok sumber tanpa warna eksplisit — standardize ke white)

## Tabel 1 — Document Control
- 12 baris x 2 kolom, lebar 3090 / 7278 dxa
- Label: bold, fill #E9ECEF | Value: regular
- Field tetap: Document Name, Document Code, Project Code, Reference Lead Code,
  Lead Name, Customer Name, End User, Year & Semester Delivery, Version,
  Document Owner (PreSales / PGO), Document Status (Draft for S03 Review), Branding Rule

## Tabel 2 — URS
- 3 kolom: 605 / 2370 / 7393 dxa (No | User Requirement | Deskripsi)
- Header: #4F81BD + white bold 7pt
- Data 7.5pt (sz 15): No center, nama UR bold, deskripsi regular
- Selalu 10 requirement

## Tabel 3 — Solution Name (4.1)
- Target: 4 baris x 2 kolom = header row (Item|Description) + 3 baris:
  Solution Name / Solution Category / Deployment Context
- Lebar 3090 / 7278, label fill #E9ECEF bold
- (Di dok sumber header row kehapus — itu deviation, bukan pola)

## Tabel 4 — Spec Table (Detailed Technical Specification)
- 5 kolom: NO 512 | URAIAN BARANG 4957 | VOL 645 | SAT 634 | GAMBAR 3174 (total 9922 dxa, fixed layout)
- Cell margin: 90 top/bottom, 100 left/right
- Header row: #4F81BD, bold 7pt, cantSplit + tblHeader (repeat tiap halaman)
- Struktur baris: Roman group (full-width, #1F4E79) -> Letter sub-group (full-width, #4F81BD) -> item rows
- Nomor item reset per sub-grup; NO col: center bold 7pt
- URAIAN cell: baris pertama = nama item BOLD 7pt; spec berikut "Parameter: " bold + "value" regular, 7pt
- VOL/SAT: center regular 7pt; SAT pakai Unit/Set/Lot/License/Server
- GAMBAR: gambar produk per item; item software ditulis "N/A"
- Zebra: #DBE5F1 / #FFFFFF bergantian per item row (di dok sumber manual & ada yang miss — generator harus strict alternation, jangan ada row tanpa fill)

## Tabel 5 — Approval
- 4 kolom: 3240 / 2520 / 2304 / 2304 (Role | Name | Signature | Date)
- Header: #4F81BD + white bold 7pt
- 5 role fixed: PGO/Presales (kosong), Product (Rizki Mardita),
  Project Planner (Badrul Huda), Head of Product (Edward Helly), CTO (Sindu Irawan)

## QA Checklist (anomali dok sumber — JANGAN ditiru)
- Double number NO=3 dua kali di grup B (Pusdatin doc) -> nomor harus sequential
- Typo: "stationery" (harusnya stationary), "Algorhytm", "One Tme Pad", "Spesfikasi", "Anlyzer", "Chipper"
- Trailing empty row di akhir spec table -> hapus
- SAT kapitalisasi konsisten (Unit bukan campur unit/Unit)
- Version format konsisten: V<x.y> + changelog dalam kurung
