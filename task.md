# CLAUDE.md — Bagaskara Cell Web App

## Tentang Proyek

Konversi aplikasi Bagaskara Cell yang sudah ada di direktori ini menjadi aplikasi web modern.

**Konteks bisnis:** Bagaskara Cell adalah toko retail HP & aksesoris (offline + online di Shopee, Tokopedia, TikTok Shop). Aplikasi ini dipakai untuk operasional toko sehari-hari.

## Tugas Utama

1. **Analisis dulu** aplikasi existing di direktori ini — pahami fitur, alur data, dan logika bisnisnya sebelum menulis kode apapun.
2. Konversi menjadi web app dengan stack di bawah.
3. Pertahankan semua fitur existing — jangan ada fitur yang hilang saat migrasi.

## Tech Stack

- **Backend:** Laravel 11 (PHP 8.3+)
- **Frontend:** Blade + Tailwind CSS v4 (via Vite)
- **Interaktivitas:** Alpine.js atau Livewire (pilih yang paling cocok dengan kompleksitas UI existing)
- **Database:** MySQL 8 (via Docker)
- **Container:** Docker + docker-compose (app, nginx, mysql, phpmyadmin)
- **Dev environment:** Windows, jalankan via Docker Desktop

## Struktur Docker yang Diinginkan

```
docker-compose.yml
docker/
├── nginx/default.conf
└── php/Dockerfile
```

Services: `app` (PHP-FPM), `web` (nginx, port 8080), `db` (MySQL, port 3306), `phpmyadmin` (port 8081).

## Konvensi Kode

- Bahasa komentar & commit message: **Bahasa Indonesia santai tapi jelas**
- Naming: English untuk kode (variabel, function, table), Indonesia untuk label UI
- Format Rupiah: `Rp 1.500.000` (titik sebagai pemisah ribuan) — buat helper `formatRupiah()`
- Validasi IMEI: 15 digit numerik + Luhn checksum (sudah ada logikanya di app lama, port ke Laravel Rule)
- Timezone: `Asia/Jakarta`
- Locale: `id`

## Fitur Khusus Bagaskara Cell

- **IMEI tracking** — setiap unit HP punya IMEI unik, wajib tervalidasi
- **Invoice/nota** — format print thermal & A4, ada logo Bagaskara Cell
- **Harga multi-platform** — harga bisa beda antara offline, Shopee, Tokopedia, TikTok Shop
- **Mobile-first UI** — sering diakses dari HP di toko, jadi UI harus responsif dan tombol besar

## Aturan Kerja

- Sebelum refactor besar, jelaskan dulu rencananya, jangan langsung eksekusi
- Setiap selesai satu fitur, pastikan `php artisan test` lulus
- Jangan hapus file aplikasi lama — pindahkan ke folder `_legacy/` sebagai referensi
- Migration database harus reversible (ada `down()` method)
- Jangan commit file `.env`, hanya `.env.example`

## Perintah Umum

```bash
# Jalankan environment
docker compose up -d

# Masuk ke container app
docker compose exec app bash

# Laravel commands (dari dalam container)
php artisan migrate
php artisan test
npm run dev        # Vite dev server untuk Tailwind
```

## Catatan

- [x] Detail aplikasi existing: hybrid Capacitor app, vanilla HTML/CSS/JS (`www/index.html`, ~6300 baris SPA), localStorage sebagai "database". Fitur: Dashboard, Invoice Generator (dengan signature canvas, IMEI scan OCR via Tesseract.js, PDF via html2pdf.js), Inventori Produk, Riwayat & Piutang (cicilan), Setelan (template, katalog HP, backup/restore, i18n ID/EN, dark/light theme), Laporan Laba/Rugi + Pengeluaran.
- [x] Butuh autentikasi multi-user: **ya** — 2 role:
  - **Kasir**: akses Invoice & Riwayat (buat invoice, lihat riwayat, catat cicilan/piutang) + Inventori Produk (CRUD stok)
  - **Owner**: full akses semua menu, termasuk Laporan Laba/Rugi & Setelan Toko (yang tidak bisa diakses Kasir)
- [x] Integrasi API Shopee/Tokopedia/TikTok Shop: **belum perlu di fase pertama** — cukup field harga multi-platform manual dulu