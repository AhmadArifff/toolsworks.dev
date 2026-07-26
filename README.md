# ⚡ toolsworks.dev

> **Developer Database & SQL Tools Suite** — Platform web terpadu untuk analisis skema database, pembuatan query `INSERT` SQL dari CSV, pembersihan file SQL, dan konversi Excel ke CSV. **100% diproses secara lokal di browser Anda.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?logo=tailwindcss)
![Privacy First](https://img.shields.io/badge/Privacy-100%25_Local-emerald)

---

## 📋 Daftar Isi

- [Tentang Toolsworks.dev](#-tentang-toolsworksdev)
- [✨ Fitur Utama](#-fitur-utama)
  - [1. ERD Visualizer](#1-erd-visualizer-erd)
  - [2. QueryForge — SQL Insert Generator](#2-queryforge--sql-insert-generator-query-forge)
  - [3. Data Bench — Pembersih SQL & Excel to CSV](#3-data-bench--pembersih-sql--excel-to-csv-data-bench)
- [🔒 Keamanan & Privasi](#-keamanan--privasi)
- [🛠️ Teknologi & Stack](#%EF%B8%8F-teknologi--stack)
- [📁 Struktur Folder Project](#-struktur-folder-project)
- [🚀 Cara Menjalankan Project (Getting Started)](#-cara-menjalankan-project-getting-started)
- [⚙️ Produksi & Deployment](#%EF%B8%8F-produksi--deployment)
- [📄 Lisensi](#-lisensi)

---

## 💡 Tentang Toolsworks.dev

**toolsworks.dev** dirancang untuk membantu Software Engineer, Database Administrator (DBA), dan Data Analyst dalam mengelola, menganalisis, serta memproses data SQL dan Excel secara efisien tanpa kekhawatiran privasi. 

Seluruh pengolahan file `.sql`, `.csv`, `.xlsx`, dan `.xls` dilakukan **sepenuhnya di memori browser pengguna**. Tidak ada data yang dikirimkan ke server luar maupun backend pihak ketiga.

---

## ✨ Fitur Utama

### 1. ERD Visualizer (`/erd`)
Tool visualisasi diagram Entity Relationship (ERD) interaktif dari file dump SQL (MySQL / PostgreSQL).

* **Auto Layout Engine**: Menyusun posisi kartu tabel secara otomatis menggunakan algoritma *Force-directed Graph Layout*.
* **Schema FK Mapper**: Mendeteksi `PRIMARY KEY`, `FOREIGN KEY`, `CONSTRAINT`, dan `ALTER TABLE` secara otomatis.
* **Value-Relation Engine (Detektor Relasi Tersembunyi)**: Memindai isi data `INSERT INTO` untuk menemukan kecocokan nilai antar kolom yang tidak memiliki FK eksplisit pada skema.
* **Materialized View Solver**: Merokonsruksi data dari `CREATE VIEW` sederhana dan menyertakannya dalam analisis relasi.
* **Interactive Canvas (Drag, Zoom, Pan)**:
  * Canvas utama & canvas **Grup Relasi** mendukung geser kartu tabel (Drag & Drop), Zoom In/Out (`+` / `-` / Scroll), dan Pan latar belakang.
  * Kartu tabel pada Grup Relasi tidak tumpang tindih secara default dan garis relasi SVG ter-update secara *real-time* saat kartu digeser.
* **Live Query Builder & Data Preview**:
  * Menghasilkan query `SELECT ... JOIN ... WHERE` multi-tabel secara *live*.
  * Pratinjau data hasil gabungan (*In-memory JOIN execution*) langsung di browser.
* **Ekspor Skema**: Ekspor definisi tabel dan relasi ke dalam format JSON.

---

### 2. QueryForge — SQL Insert Generator (`/query-forge`)
Generator query `INSERT` SQL otomatis dari file data CSV.

* **DDL Parser**: Membaca struktur tabel dari perintah `CREATE TABLE`.
* **Flexible CSV Reader**: Mendukung unggah file `.csv` maupun tempel teks CSV (menggunakan PapaParse).
* **Smart Column Auto-Matching**: Secara cerdas mencocokkan header CSV dengan kolom database berdasarkan alias nama (seperti `nama` → `name`, `no_hp` → `phone`).
* **Auto Column Injection**:
  * Auto-generate `UUID()` untuk kolom Kunci Primer (`id`).
  * Auto-set `NOW()` untuk timestamp (`created_at` / `updated_at`).
* **Duplicate Value Checker**: Memeriksa potensi duplikasi nilai pada kolom tertentu sebelum query di-generate.
* **Batching & Boundary Controls**: Membatasi rentang baris data yang diproses dan memecah query menjadi beberapa *batch* (misal 100 baris per perintah `INSERT`).
* **Multi-Format Export**: Salin semua batch, salin per batch tertentu, atau unduh file `.sql`.

---

### 3. Data Bench — Pembersih SQL & Excel to CSV (`/data-bench`)
Dua panel utility praktis untuk manipulasi file SQL dan Excel.

* **Panel Pembersih File SQL**:
  * Menghapus seluruh komentar SQL (`--`, `#`, `/* */`) dan baris kosong berlebih.
  * Memproses file besar secara asinkron (*chunked processing*) tanpa membuat layar browser membeku (*freeze*).
  * Menampilkan statistik penghematan ukuran file (sebelum vs sesudah dalam KB/MB dan persentase).
* **Panel Konversi Excel ke CSV**:
  * Mendukung format Excel `.xlsx` dan `.xls` (menggunakan SheetJS).
  * Pilih sheet spesifik atau konversi seluruh sheet sekaligus.
  * Opsi unduh file tunggal `.csv` atau arsip `.zip` untuk multi-sheet (menggunakan JSZip).

---

## 🔒 Keamanan & Privasi

```
 ┌─────────────────────────────────────────────────────────────┐
 │                      BROWSER PENGGUNA                       │
 │  ┌──────────────┐    ┌─────────────────┐   ┌─────────────┐  │
 │  │ File .SQL    │ ──▶│ In-Memory Engine│──▶│ Output Hasil│  │
 │  │ .CSV / .XLSX │    │ (JS Processing) │   │ (Download)  │  │
 │  └──────────────┘    └─────────────────┘   └─────────────┘  │
 └─────────────────────────────────────────────────────────────┘
                                X
                        [ TANPA SERVER ]
```

* **100% Local Browser Execution**: Pemrosesan file menggunakan JavaScript Client-Side murni.
* **Zero Network Upload**: Tidak ada panggilan API upload file. Data bisnis atau skema sensitif Anda tetap aman di perangkat lokal.

---

## 🛠️ Teknologi & Stack

* **Framework**: [Next.js 16](https://nextjs.org/) (App Router)
* **Library Utama**: [React 19](https://react.dev/)
* **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
* **Animasi UI**: [Framer Motion](https://www.framer.com/motion/)
* **Font**: Google Fonts (`Inter`, `JetBrains Mono`, `Bricolage Grotesque`) via `next/font`
* **Parser Data**:
  * [PapaParse](https://www.papaparse.com/) — Fast CSV parsing
  * [SheetJS (xlsx)](https://sheetjs.com/) — Excel spreadsheet parsing
  * [JSZip](https://stuk.github.io/jszip/) — ZIP archive generator

---

## 📁 Struktur Folder Project

```text
toolsworks/
├── public/
│   └── tools/
│       ├── erd-visualizer.html         # Asset HTML ERD Visualizer Engine
│       ├── sql-insert-generator.html   # Asset HTML QueryForge Engine
│       └── data-bench.html             # Asset HTML Data Bench Engine
├── src/
│   ├── app/
│   │   ├── layout.js                   # Root Layout + Fonts + Navbar
│   │   ├── page.js                     # Landing Page Dashboard
│   │   ├── globals.css                 # Global CSS + Tailwind Imports
│   │   ├── erd/
│   │   │   └── page.js                 # ERD Visualizer Route (/erd)
│   │   ├── query-forge/
│   │   │   └── page.js                 # QueryForge Route (/query-forge)
│   │   └── data-bench/
│   │       └── page.js                 # Data Bench Route (/data-bench)
│   ├── components/
│   │   └── Navbar.jsx                  # Header Navigasi Terpadu
│   └── lib/
│       └── utils.js                    # Utility Helper Functions
├── package.json
└── README.md
```

---

## 🚀 Cara Menjalankan Project (Getting Started)

### Prasyarat
* **Node.js** v18.0.0 atau yang lebih baru
* **npm** / **yarn** / **pnpm** / **bun**

### Langkah-langkah Instalasi

1. **Clone repository atau buka folder project**:
   ```bash
   cd toolsworks
   ```

2. **Install dependensi npm**:
   ```bash
   npm install
   ```

3. **Jalankan server pengembangan (Development Server)**:
   ```bash
   npm run dev
   ```

4. **Buka di browser**:
   Buka `http://localhost:3000` pada browser Anda untuk melihat aplikasi.

---

## ⚙️ Produksi & Deployment

### Build untuk Produksi
Untuk membuat bundle produksi yang teroptimasi:

```bash
npm run build
```

### Menjalankan Server Produksi
Setelah build berhasil, jalankan server produksi secara lokal:

```bash
npm run start
```

---

## 📄 Lisensi

Project ini dilisensikan di bawah lisensi [MIT License](LICENSE). Bebas digunakan dan dikembangkan kembali.
