# AGENTS.md — Bagaskara Cell Web App

## Tentang Proyek

Konversi aplikasi Bagaskara Cell (toko retail HP & aksesoris — offline + online di Shopee, Tokopedia, TikTok Shop) dari app hybrid Capacitor/vanilla JS yang ada di direktori ini menjadi web app modern. Dipakai untuk operasional toko sehari-hari.

**Status saat ini: baru tahap scaffolding awal, belum ada kode Laravel yang jalan.** Lihat "Status Pengerjaan" di bawah sebelum melanjutkan.

---

## Tugas Utama

1. Analisis app existing sudah selesai (lihat "Inventori App Lama" di bawah) — jangan analisis ulang dari nol, sudah lengkap.
2. Konversi menjadi web app dengan stack di bawah.
3. Pertahankan semua fitur existing — jangan ada fitur yang hilang saat migrasi (kecuali yang memang disepakati diganti, lihat catatan per-fitur).

## Tech Stack (sudah difinalisasi)

- **Backend:** Laravel 11 (PHP 8.3+)
- **Frontend:** Blade + Tailwind CSS v4 (via Vite)
- **Interaktivitas:** **Livewire + Alpine.js** — Livewire untuk komponen server-driven (Produk, Riwayat, Setelan, Laporan), Alpine.js untuk interaksi client-only di dalamnya (item invoice dinamis, live total, signature canvas, autocomplete, OCR modal, toggle tema/zoom)
- **Database:** MySQL 8 (via Docker)
- **Container:** Docker + docker-compose (`app` PHP-FPM, `web` nginx :8080, `db` MySQL :3306, `phpmyadmin` :8081)
- **Platform:** web browser dulu (mobile-first responsive). **Tidak** membangun ulang wrapper Android/Capacitor di fase ini.
- **Cetak invoice:** PDF server-side via `barryvdh/laravel-dompdf` (thermal 58/80mm + A4), plus opsi browser print (`window.print()`)
- **Dev environment:** Windows, jalankan via Docker Desktop

## Konvensi Kode

- Bahasa komentar & commit message: **Bahasa Indonesia santai tapi jelas**
- Naming: English untuk kode (variabel, function, table), Indonesia untuk label UI
- Format Rupiah: `Rp 1.500.000` (titik sebagai pemisah ribuan) — buat helper `formatRupiah()`
- Validasi IMEI: 15 digit numerik + Luhn checksum — **ini fitur BARU, bukan port.** App lama tidak punya validasi Luhn sama sekali (cuma ekstraksi digit dari OCR). Buat `app/Rules/ValidImei.php` implements `ValidationRule`.
- Timezone: `Asia/Jakarta`
- Locale: `id`

## Role & Akses (sudah difinalisasi)

2 role: `kasir` dan `owner`.

- **Kasir**: Invoice (buat/edit), Riwayat (lihat + cicilan), Produk (CRUD stok)
- **Owner**: full akses, termasuk Laporan Laba/Rugi, Pengeluaran, dan Setelan Toko (yang tidak bisa diakses Kasir)

Login sederhana saja, tidak ada halaman registrasi publik (toko 2 orang).

## Fitur Khusus Bagaskara Cell

- **IMEI tracking** — setiap unit HP punya IMEI unik (nullable untuk produk aksesoris), wajib tervalidasi Luhn di server
- **Invoice/nota** — format print thermal & A4, ada logo Bagaskara Cell, tanda tangan pembeli+penjual
- **Harga multi-platform** — kolom `price_sell` (harga dasar/offline) + `price_shopee`/`price_tokopedia`/`price_tiktok` nullable (fallback ke `price_sell` kalau kosong). **Belum perlu integrasi API** marketplace di fase ini — cukup input manual.
- **Mobile-first UI** — sering diakses dari HP di toko, jadi UI harus responsif dan tombol besar
- **Tanda tangan penjual** — disimpan sebagai default per user (`users.signature_path`), dengan tombol "gambar ulang" kalau mau ganti. Beda dari app lama yang selalu gambar ulang tiap transaksi.
- **Data**: proyek ini **mulai fresh**, tidak ada migrasi data produksi dari app lama (dikonfirmasi user, belum ada data nyata yang harus dipindah).

## Aturan Kerja

- Sebelum refactor besar, jelaskan dulu rencananya, jangan langsung eksekusi
- Setiap selesai satu fitur, pastikan `php artisan test` lulus
- **Jangan hapus file aplikasi lama.** Idealnya dipindah ke `_legacy/`, tapi lihat catatan permission di bawah — kalau `git mv` gagal karena Access Denied, biarkan saja di lokasi asal, jangan dihapus.
- Migration database harus reversible (ada `down()` method)
- Jangan commit file `.env`, hanya `.env.example`

---

## ⚠️ Status Pengerjaan (per sesi terakhir)

**Sudah dibuat (siap dipakai):**
- `docker-compose.yml` (services: app, web, db, phpmyadmin)
- `docker/php/Dockerfile` (PHP 8.3-FPM + ext pdo_mysql, mbstring, exif, gd, zip, bcmath + composer)
- `docker/nginx/default.conf`

**Belum dikerjakan sama sekali:** `laravel new`, migration, model, seeder, semua komponen Livewire, PDF, auth — semuanya masih di tahap rencana (lihat "Urutan Pengerjaan" di bawah).

**Blocker yang belum selesai:**
1. **Environment kosong** — mesin dev ini (waktu sesi terakhir) belum punya Docker Desktop, WSL, PHP, maupun Composer terpasang (sudah dicek: tidak ada di Program Files, registry, Start Menu, maupun proses yang jalan). User bilang sudah install Docker Desktop tapi belum kedeteksi — kemungkinan instalasi belum selesai/perlu restart, atau salah lokasi. **Cek ulang ini duluan** sebelum lanjut ke scaffolding (`docker --version` harus jalan).
2. **Permission file lama** — `www/`, `android/`, kedua file `.apk`, `capacitor.config.json`, `package.json`/`package-lock.json` lama, `style.css`, logo, `README.md`, `test.js`, dll di root **tidak punya ACL delete/rename** untuk user Windows saat ini (`git mv` gagal "Access is denied", begitu juga `icacls /grant` gagal karena tidak ada WRITE_DAC). File-file ini bisa **dibaca** dan **kontennya bisa ditimpa** (write data masih diizinkan), tapi tidak bisa di-rename/dipindah/dihapus dari shell non-elevated. **Keputusan user: biarkan di tempat, jangan coba pindah paksa lagi.** Kalau nanti perlu file baru menggantikan `package.json`/`README.md` root (bentrok nama dengan hasil `laravel new`), timpa **isinya** saja (bukan rename), konten lama tetap aman di git history.
3. Karena masalah #2, pendekatan `laravel new .` langsung di root kemungkinan akan komplain root tidak kosong. Rencana: scaffold Laravel di folder sementara (mis. lewat container), lalu salin hasil generate ke root, dan untuk file yang bentrok (`package.json`, `README.md`, `.gitignore`) **timpa isinya** manual (merge `.gitignore`, jangan overwrite polos supaya entry lama seperti `android/.gradle/` dll tidak hilang).

**Langkah selanjutnya begitu Docker terkonfirmasi jalan:**
1. `docker compose build` lalu `docker compose up -d`
2. Jalankan `composer create-project laravel/laravel` di dalam container `app` (working dir kosongkan dulu / pakai temp dir lalu pindahkan)
3. Install `livewire/livewire`, `barryvdh/laravel-dompdf`, Tailwind v4 via `@tailwindcss/vite`, Chart.js (npm)
4. Lanjut ke migration (lihat skema di bawah)

---

## Inventori App Lama (hasil analisis — jadi acuan fitur, JANGAN dianalisis ulang)

File utama lama: `www/index.html` (~7600 baris, vanilla JS SPA), `www/phone-catalog.js` (~400KB, `window.ERAFONE_CATALOG`, ~540 model HP). Semua data lama di `localStorage`, tanpa server, tanpa auth.

### Navigasi (6 tab)
Dashboard/Beranda, Riwayat/History, Invoice/form, Produk/Products, Katalog (browse read-only katalog HP), Setelan/Settings. Plus floating action button langsung ke tab Invoice.

### Dashboard
Stat cards (invoice hari ini, omset hari ini, stok ready, nilai inventori, total transaksi), grafik batang 7 hari, card piutang kondisional, Laporan Bulanan (picker bulan/tahun + export CSV), card Laba/Rugi (Pendapatan/HPP/Laba Kotor/Total Pengeluaran/Laba Bersih), list pengeluaran (7 kategori: Sewa Toko, Listrik & Air, Gaji Karyawan, Belanja Stok, Transportasi, Iklan & Promosi, Operasional), feed 5 invoice terbaru di paling bawah.

### Invoice (form 3-step)
1. No invoice otomatis (editable), tanggal, data pembeli (+pick kontak HP), metode bayar, diskon, status bayar (Lunas/DP/Belum Bayar + field jumlah dibayar kondisional)
2. Item dinamis: nama, IMEI (+scan OCR kamera), qty, harga, diskon per-item, tombol "Pilih Stok" (modal cari produk `status != Terjual`)
3. Garansi (none/personal/resmi/both + durasi kondisional), template catatan (auto-isi), catatan textarea

Live total banner (sticky), preview modal dengan 2 signature canvas (pembeli tersimpan ke invoice, penjual dulu cuma dibakar saat print — **di versi baru, signature penjual jadi default per-user**). Bisa edit invoice existing (restore stok lama dulu sebelum re-apply item baru).

### Riwayat/History
Search (nama/no invoice/IMEI/nama item) + filter status bayar, grouping accordion bulan-tahun. Per invoice: modal cicilan (partial payment → `amount_paid += min(entered, remaining)`, auto-lunas di 0), share WhatsApp (**app lama ini BROKEN**, panggil fungsi yang tidak ada — di versi baru bikin baru pakai link `wa.me`), lihat nota, hapus (restore stok).

### Produk/Products
Search + filter (status, brand), export/import CSV (kolom: `ID, Merek, Tipe, RAM, Storage, Warna, Kondisi, Harga Beli, Harga Jual, Sumber/Supplier, Tipe Garansi, IMEI, Catatan, Status` — **pertahankan urutan ini** di versi baru supaya CSV lama bisa diimport). Autocomplete brand+model dari katalog (auto-isi RAM/storage/harga). Activity log per produk (Stok Masuk/Terjual/Stok Dipulihkan/Detail Diupdate).

### Katalog
Browse read-only ~540 model HP (brand, model, kategori, image, variants: warna/kapasitas/harga/stok), filter harga/brand/kategori.

### Setelan
Profil toko, Template Catatan (4 bawaan: umum/hp/aksesoris/servis — `umum` tidak bisa dihapus — + custom), Katalog Model HP (import/export/reset), Backup & Restore (JSON versioned), toggle bahasa ID/EN, toggle tema (7 varian warna), zoom tampilan.

### Logika Bisnis Penting
- **Nomor invoice**: format `INV/YYYYMMDD/NNN`. App lama scan in-memory (race-prone). **Versi baru harus atomic** — `InvoiceCounter` table + `lockForUpdate()` dalam DB transaction, alokasi nomor final HANYA saat save sukses (bukan saat form dibuka).
- **Cicilan**: `amount_paid += min(entered, remaining)`, `amount_remaining = max(0, grand_total - amount_paid)`, auto-flip ke lunas di 0.
- **Stok**: `Tersedia → Terjual` saat invoice disimpan, balik ke `Tersedia` saat invoice diedit (restore dulu) atau dihapus. Semua transisi di-log.
- **Laba/Rugi**: Pendapatan (amount_paid non-lunas / grand_total lunas, per invoice_date) − HPP (sum `price_buy * qty` HANYA item yang linked ke `product_id` — item manual/lepas kontribusi HPP nol, ini limitasi yang disadari, bukan bug) − Total Pengeluaran = Laba Bersih.
- **i18n**: app lama scan string DOM (rapuh). **Versi baru pakai Laravel native** `__()` + `lang/id|en/*.php`, bukan di-port.
- **OCR IMEI**: Tesseract.js murni client-side (ekstraksi digit dari foto, tanpa validasi) — tetap dipakai sebagai Alpine island, hasil OCR masuk ke field yang divalidasi `ValidImei` Rule di server.

---

## Skema Database (rencana lengkap)

Urutan migration, semua dengan `down()`:

| # | Migration | Kolom kunci |
|---|---|---|
| 1 | `add_role_and_signature_to_users_table` | `role` enum(kasir,owner), `signature_path` nullable |
| 2 | `create_store_settings_table` | singleton: name, address, phone_primary, phone_secondary, instagram, pdf_folder_name |
| 3 | `create_note_templates_table` | slug unique, label, body text, is_built_in, is_deletable. Seed: umum(tak bisa hapus), hp, aksesoris, servis |
| 4 | `create_phone_catalog_models_table` | brand, model, category, image_url, price_min, price_max; unique(brand,model) |
| 5 | `create_phone_catalog_variants_table` | FK phone_catalog_model_id, color, capacity, variant_name, price, stock, status, image_url |
| 6 | `create_products_table` | brand, model, ram/storage/color nullable, condition enum, price_buy, price_sell, **price_shopee/price_tokopedia/price_tiktok nullable**, source, warranty_type, imei nullable unique, notes, status enum(tersedia,terjual), FK nullable phone_catalog_variant_id |
| 7 | `create_product_logs_table` | FK product_id cascade, FK nullable invoice_id, action, notes, created_at saja |
| 8 | `create_invoice_counters_table` | counter_date unique, last_sequence unsigned int |
| 9 | `create_invoices_table` | invoice_no unique, invoice_date, customer_name/phone/address, payment_method, discount, subtotal, grand_total, payment_status enum, amount_paid, amount_remaining, warranty_type enum, warranty_duration, notes, buyer_signature_path, seller_signature_path, FK created_by |
| 10 | `create_invoice_items_table` | FK invoice_id cascade, FK nullable product_id, name, imei nullable, qty, price, discount, subtotal |
| 11 | `create_invoice_payments_table` | FK invoice_id cascade, paid_at, amount, note, FK created_by |
| 12 | `create_expenses_table` | expense_date, category enum (7 kategori tetap), amount, note, FK created_by |

Models: `User`, `StoreSetting`, `NoteTemplate`, `PhoneCatalogModel` (hasMany `PhoneCatalogVariant`), `Product` (hasMany `ProductLog`, belongsTo `PhoneCatalogVariant`), `ProductLog`, `Invoice` (hasMany `InvoiceItem`/`InvoicePayment`, belongsTo `User`), `InvoiceItem`, `InvoicePayment`, `Expense`, `InvoiceCounter`.

**Seeder katalog**: konversi `www/phone-catalog.js` → `storage/app/seed-data/phone-catalog.json` sekali (strip prefix `window.ERAFONE_CATALOG = `, json_decode sisanya), lalu `PhoneCatalogSeeder` bulk-insert chunked dalam transaction.

---

## Breakdown Komponen Livewire (rencana)

- **Dashboard**: `App\Livewire\Dashboard\Overview`, `SalesChart` (Chart.js via Alpine x-init), `MonthlyReport`
- **Invoice**: `App\Livewire\Invoice\Builder` (parent 3-step, item rows = Alpine island, save = 1 DB transaction: alokasi nomor + flip stok + product_logs), `StockPickerModal`, `PreviewModal` (dual signature canvas)
- **Riwayat**: `App\Livewire\History\Index`, `CicilanModal`. Share WA pakai helper `App\Support\WhatsAppLink` → `<a href="https://wa.me/...">`
- **Produk**: `App\Livewire\Products\Index`, `FormModal` (autocomplete katalog + harga multi-platform), activity log partial
- **Katalog**: `App\Livewire\Katalog\Index` (read-only)
- **Setelan** (owner-only kecuali Tampilan): `StoreProfile`, `NoteTemplates`, `CatalogManager`, `BackupRestore`. Tampilan (tema/zoom/bahasa) = pure Alpine + cookie/localStorage, tidak perlu tabel DB.
- **Laporan** (owner-only): `App\Livewire\Reports\ProfitLoss`, `Expenses`

Auth: `app/Http/Middleware/EnsureUserHasRole.php` (alias `role` di `bootstrap/app.php`), Gate `view-owner-menu` untuk sembunyikan menu di Blade (UX saja, middleware route = security boundary sesungguhnya).

## PDF & Print

`barryvdh/laravel-dompdf`. Partial konten dipakai bareng oleh PDF & browser-print (`resources/views/invoices/partials/_content-thermal.blade.php`, `_content-a4.blade.php`) supaya tidak ada dua sumber kebenaran tampilan. Route: `GET /invoices/{invoice}/pdf/thermal/{width?}`, `/pdf/a4`, `/print` (browser print fallback). Signature disimpan sebagai file PNG di `storage/app/public/signatures/`, path di kolom DB (bukan base64).

---

## Urutan Pengerjaan (Milestone)

1. Scaffolding (Docker up, `laravel new`, Tailwind v4, Livewire)
2. Skema + seeder (migration, model, seeder user/store/template/katalog)
3. Auth + layout shell (login, role middleware, nav sesuai role, placeholder semua tab)
4. Produk/Products (CRUD, autocomplete, harga multi-platform, log, CSV)
5. Invoice Builder (form 3-step, stock picker, nomor atomic, save transaction, edit mode)
6. PDF + print + signature + WhatsApp
7. Riwayat/History (search/filter/accordion, cicilan, hapus+restore)
8. Katalog (browse read-only)
9. Dashboard nyata (stat, grafik, feed, laporan bulanan)
10. Laporan Laba/Rugi + Pengeluaran (owner-only)
11. Setelan (profil, template, katalog manager, backup/restore, tampilan)
12. Polish OCR IMEI (Tesseract.js npm, Alpine island)
13. Hardening (full test suite hijau, update README)

Tiap milestone di-review dulu sebelum lanjut ke berikutnya.

## Strategi Testing

- `InvoiceNumberServiceTest` — alokasi berurutan per hari, unique constraint tolak duplikat
- `ValidImeiRuleTest` — tabel IMEI valid/invalid Luhn + non-numerik/panjang salah
- `InvoiceBuilderTest` — save→flip stok+log, edit→restore stok lama dulu, hapus→restore+log
- `InvoicePaymentTest` — partial payment, overpayment ter-cap, auto-lunas di 0
- `RoleAccessTest` — Kasir 403 di `/laporan`,`/pengeluaran`,`/setelan`; Owner lolos semua
- `ProductsTest` — CRUD + round-trip CSV
- `ProfitLossReportTest` — verifikasi rumus termasuk edge case item tanpa product_id
- Smoke test PDF — route dompdf return 200 + content-type application/pdf

## Perintah Umum (setelah Docker jalan)

```bash
docker compose up -d
docker compose exec app bash
php artisan migrate
php artisan test
npm run dev
```
