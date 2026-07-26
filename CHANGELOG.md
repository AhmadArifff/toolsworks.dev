# 📜 CHANGELOG — toolsworks.dev

Seluruh riwayat perubahan, pembaruan versi, dan rilis fitur aplikasi **toolsworks.dev**.

---

## [V.1.1.1] — 2026-07-27

### 🎨 Visual & Favicon Updates
- **Favicon Baru**: Mengganti favicon bawaan Next.js dengan ikon kustom `icon.svg` bernuansa gradient Teal (`#2DD4BF`) & Sky Blue (`#38BDF8`) berlogo kilat ⚡.
- **Pembersihan File Asset**: Menghapus `favicon.ico` bawaan agar Next.js memprioritaskan `icon.svg` modern.

---

## [V.1.1.0] — 2026-07-26

### 🚀 Fitur & Enhancement Modal Ringkasan ERD
- **Canvas Interaktif pada Grup Relasi**:
  - Mengubah visualisasi diagram pada setiap kartu "Grup Relasi" di Modal Ringkasan ERD menjadi **Canvas Interaktif Utuh**.
  - **Drag & Drop Kartu Tabel**: Kartu tabel dalam grup relasi dapat digeser dan ditata posisinya secara bebas.
  - **Zoom In (+), Zoom Out (-), Fit, & Pan**: Mendukung tombol zoom, mouse scroll wheel, dan pan latar belakang.
  - **Tata Letak Default Tanpa Tumpang Tindih**: Kartu tabel ditempatkan dengan jarak aman secara otomatis sehingga tidak saling menimpa.
  - **Real-Time SVG Line Redraw**: Garis relasi SVG (garis putus-putus teal) terhubung antar tabel dan ter-update secara *real-time* saat kartu digeser.
- **Hydration Warning Fix**:
  - Menambahkan `suppressHydrationWarning` pada tag `<html>` dan `<body>` di `src/app/layout.js` untuk mengatasi konflik atribut dinamis yang disuntikkan oleh ekstensi browser (seperti Scribe / Grammarly).

---

## [V.1.0.0] — 2026-07-26

### 🎉 Rilis Perdana Project toolsworks.dev
- Konsolidasi 3 tool HTML standalone (`erd-visualizer-Fixed.html`, `sql-insert-generator.html`, `data-bench.html`) ke dalam 1 project Next.js.
- Penambahan Halaman Dashboard Beranda (`/`) & Shared Navbar (`src/components/Navbar.jsx`).
- Implementasi embedding HTML direct di rute `/erd`, `/query-forge`, dan `/data-bench` untuk menjamin 100% konsistensi tampilan dan *flow logic*.
- Dokumentasi resmi `README.md`.
