# House Style — Solution Pack Document (v1.1, Sep 2026)

Acuan resmi: file `Solution Pack Pussiberad 2027 V1.1.docx` (dari Chris).
Template generator: `templates/house-style-template.docx` — styles.xml, numbering.xml,
theme1.xml, dan sectPr disalin dari file itu, isinya dikosongkan.

Kalau ada selisih antara file acuan dan `style-formatting-guidance.md`, **file menang**.

## Halaman
- Letter 8.5 x 11 in; margin 936 dxa (0.65 in) di keempat sisi; header/footer distance 0.
- **Page break antar section**: setiap `Heading 1` — kecuali section pertama (1. Document
  Control) yang tetap di halaman judul — didahului **paragraf kosong berisi manual page break**
  (`<w:br w:type="page"/>`). Jadi H1 selalu berada di bagian paling atas halaman baru.
  Pakai mekanisme manual break ini (bukan `pageBreakBefore` di style), meniru file acuan.
  Paragraf pembawa break harus kosong (tanpa teks) dan tidak boleh kena zebra/spacing aneh.

## Font & warna
- Theme: **majorFont = Calibri** (heading), **minorFont = Cambria** (body).
- Body text #222222. Jangan pernah set font/size langsung di paragraf — ikut style/theme.

## Paragraph style
| Style | Dipakai untuk | Font | Size | Warna | Indent | Spacing |
|---|---|---|---|---|---|---|
| `Title` | baris "SOLUTION PACK DOCUMENT" | Calibri bold | 24 | 17375E | center (left 0.5" warisan Normal) | after 15pt, line 1.0 |
| `Heading 1` | section 1–4 | Calibri bold | 16 | 123555 | left 0 | after 3pt, line 1.05, outlineLvl 0 |
| `Heading 2` | sub-section 2.1/2.2/2.3/4.1/4.2 | Calibri bold | 14 | 1F497D | left 400 dxa + leftChars 200 | after 3pt, line 1.05, outlineLvl 1 |
| `Normal - H2` | paragraf body | Cambria | 11 | inherit (#000) | justify, left 965 dxa (0.67"), first line 274 dxa (0.19") | after 3pt, line 1.05 |
| `Bullet List - H2` | bullet (2.3 Objective) | Cambria | 11 | inherit | justify, left 4 ch, hanging 1 ch | after 3pt, line 1.05 |
| `Normal` | base style saja | Cambria | 11 | 222222 | left 720 dxa, first line 91 dxa | after 3pt, line 1.05 |
| `Table - Item` | sel nama/label tabel (bold) | Cambria bold | 11 | inherit | left 0 | after 3pt |
| `Table - Description` | sel deskripsi tabel | Cambria | 11 | inherit | justify, ind 0 | after 3pt |

`Heading 3` masih ada di template (warisan) tapi **tidak dipakai** — house style hanya
Title / Heading 1 / Heading 2.
Dua style terakhir (`Bullet List - H2`, `Table - Description`) tidak ada di file acuan;
generator membuatnya otomatis (`ensure_house_styles()`) sesuai nilai di tabel ini.

## Tabel
- Table style: **`Normal Table`** (tanpa style bawaan); border digambar manual:
  single, sz 4 (0.5 pt), warna **#9FBAD0**, semua sisi termasuk insideH/insideV.
- `tblLayout=fixed`, `tblCellMar` 70/100/70/100 dxa.
- Lebar kolom: DocControl & 4.1 = `3090/7278`; URS = `605/2370/7393` dxa.
- Fill: label **#E9ECEF**, header **#4F81BD** (teks putih bold 10pt, center, vAlign center),
  zebra data **#DBE5F1/#FFFFFF** (baris data pertama DBE5F1).
- Teks sel: DocControl 10pt (label bold); header URS 10pt bold putih;
  isi URS pakai `Table - Item` / `Table - Description` (11pt Cambria); header 4.1 pakai
  `Table - Item` + warna putih.
- Header tabel URS: `tblHeader` + `cantSplit` (repeat saat pindah halaman).
- **Kolom No URS: auto-numbering Word** (`numId 7` → abstractNum decimal `"%1."`),
  bukan angka manual. Nomor otomatis ikut kalau jumlah URS berubah.

## Selisih dengan `style-formatting-guidance.md`
- Guidance menulis warna heading "DarkSlateBlue"; file aktual: Title #17375E (theme text2
  shade BF), Heading 1 #123555, Heading 2 #1F497D (theme text2). Warna 4F81BD = accent1
  dipakai untuk fill header tabel, bukan teks heading.
- Guidance menulis Heading 2 indent 1.7 in; file aktual 400 dxa + leftChars 200 (≈2 ch,
  ≈0.28 in).
- Guidance menyebut style `Bullet List - H2` dan `Table - Description`; di file V1.1 bullet
  masih `List Bullet` dan sel deskripsi `Table - Normal`. Generator memakai nama versi
  guidance.
- Font "Calibri (Heading)" / "Cambria (Body)" di guidance = theme major/minor ✓ (cocok).
