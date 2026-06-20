# Project Description: Bagaskara Cell — POS & Invoice Generator

File ini dibuat sebagai panduan cepat untuk AI Agent (seperti Claude) dalam memahami arsitektur, teknologi, fitur, dan roadmap aplikasi Bagaskara Cell.

---

## 1. Spesifikasi Teknologi (Tech Stack)

Aplikasi ini menggunakan pendekatan **hybrid mobile app** dengan basis web offline-first yang dibungkus oleh **Capacitor.js** menjadi aplikasi Android (.apk).

- **Bahasa Utama**: HTML5, CSS3 (Vanilla CSS), dan JavaScript (ES6+ Vanilla).
- **Arsitektur**: Single Page Application (SPA) mandiri — satu file `www/index.html` (~6300+ baris).
- **Penyimpanan (Database)**:
  - `localStorage` browser/webview sebagai media penyimpanan utama offline.
  - `bagaskara_invoices` — data invoice transaksi.
  - `bagaskara_products` — data produk inventori.
  - `bagaskara_expenses` — data pengeluaran operasional.
  - `bagaskara_store_info` — profil dan pengaturan toko.
  - `bagaskara_templates` — template teks catatan invoice (dynamic, supports custom templates).
  - `bagaskara_counter` + `bagaskara_last_date` — state penomoran invoice otomatis.
  - `bagaskara_lang` — preferensi bahasa (id/en).
  - `bagaskara_theme` — preferensi tema (dark/light).
- **Framework Mobile**: **Capacitor.js (Android Platform)**.
  - Plugins yang digunakan:
    - `@capacitor/filesystem`: Menyimpan file backup JSON dan PDF ke folder Documents.
    - `@capacitor/share`: Native share sheet untuk membagikan PDF dan file backup.
    - `@capacitor-community/contacts`: Integrasi kontak HP untuk pemilihan nama pelanggan.
- **Pustaka Pihak Ketiga (Third-Party Libs)**:
  - `Tesseract.js` (Offline OCR): Memindai nomor IMEI/Serial Number dari kamera HP.
  - `html2pdf.js`: Mengonversi invoice HTML menjadi dokumen PDF siap cetak.

---

## 2. Tujuan Aplikasi

Membantu operasional harian konter Handphone **Bagaskara Cell** untuk:
1. Membuat invoice dan tanda bukti garansi dengan tampilan profesional.
2. Mengelola stok HP (baru maupun bekas) berdasarkan nomor IMEI secara unik.
3. Mencatat riwayat penjualan, omset harian, piutang pelanggan, dan pengeluaran toko secara offline-first.
4. Menghasilkan laporan laba/rugi otomatis per bulan.

---

## 3. Fitur Utama & Alur Kerja yang Sudah Selesai

### A. Beranda (Dashboard)
- **Topbar Greeting Dinamis**: Menampilkan sapaan berdasarkan waktu (Selamat Pagi/Siang/Sore/Malam) dengan nama toko dan tanggal hari ini. Otomatis mengikuti bahasa aktif (ID/EN).
- Metrik finansial: Invoices hari ini, Omset hari ini, Total Stok Ready, Nilai Inventori (Modal Aktif).
- Metrik piutang: Total Piutang aktif (Rp) dan jumlah Pelanggan Berhutang.
- Card **Tagihan Aktif** — muncul otomatis jika ada piutang, menampilkan max 5 pelanggan dengan tombol `+ Cicilan` langsung.
- Pintasan cepat membuat invoice baru dan melihat riwayat.
- Feed 5 transaksi terbaru dengan badge status pembayaran berwarna.
- **View Switcher**: Toggle antara Ringkasan (Harian) dan Laporan Bulanan.

### B. Pembuat Invoice (Invoice Generator)
- Pengisian detail pelanggan (nama, nomor HP, alamat). Integrasi pencarian dari daftar kontak HP.
- **Status Pembayaran**: dropdown Lunas / DP / Belum Bayar. Field "Jumlah Dibayar" muncul kondisional saat memilih DP.
- Pengaturan tipe garansi (Tanpa Garansi, Garansi Personal Toko, Garansi Resmi Brand).
- Panel tanda tangan digital (Canvas-based Signature) untuk penjual dan pembeli pada modal pratinjau.
- Tombol `Pilih Stok` di setiap baris barang untuk auto-fill nama, IMEI, dan harga jual dari inventori.
- Mengurangi stok barang (`status → "Terjual"`) saat invoice disimpan.
- **Live Total Banner**: Bar fixed di bawah layar menunjukkan total belanja real-time + tombol "Preview & Create". Diletakkan di **luar** `#tab-form` agar `position: fixed` tidak rusak oleh `transform` pada animasi `fadeIn`.
- **Template Catatan Dinamis**: Dropdown template catatan invoice yang diisi secara dinamis dari localStorage (termasuk template custom user).

### C. Inventori Produk & Autocomplete Katalog
- Manajemen unit produk: Merek, Model, RAM, Storage, Warna, Kondisi (Baru/Second/Refurbish), Harga Beli, Harga Jual, Supplier, IMEI, Catatan.
- Pencarian produk dengan chip filter merek cepat.
- Autocomplete dari `www/phone-catalog.json` (540 tipe HP populer) — memilih tipe HP otomatis mengisi RAM & Storage default.
- **Log & Riwayat Aktivitas Perubahan**: Setiap produk memiliki log riwayat perubahan yang mencatat setiap aksi beserta tanggal & waktu (*timestamp*) ketika unit masuk stok, mengalami pembaruan detail, terjual (keluar stok), atau dikembalikan statusnya ke Tersedia (jika invoice dihapus/diperbarui). Riwayat ini bisa di-expand langsung pada kartu produk.

### D. Riwayat Transaksi & Piutang
- Filter pencarian berdasarkan no invoice, nama pembeli, atau IMEI produk.
- **Filter chip status pembayaran**: Semua / Lunas / DP / Belum Bayar / Semua Piutang.
- Badge warna pada setiap kartu invoice: Lunas (hijau), DP (oranye), Belum Bayar (merah).
- Kotak info **Sudah Dibayar** + **Sisa Tagihan** pada invoice yang masih punya hutang.
- Tombol **💰 Catat Cicilan** pada invoice belum lunas — membuka bottom sheet untuk merekam pembayaran baru, update `paymentHistory[]`, dan auto-update status ke Lunas jika sisa = 0.
- Share nota ke WhatsApp (teks) atau ekspor PDF via Capacitor native share. PDF dihasilkan dari elemen `#print-area` menggunakan `html2pdf.js` — isi PDF identik dengan tampilan pratinjau invoice.
- Hapus invoice — otomatis mengembalikan status produk ke `"Tersedia"`.

### E. Setelan (Settings)
- **Profil Toko**: Nama, alamat, telepon, Instagram, folder PDF output.
- **Template Catatan Dinamis (Add/Remove)**:
  - 4 template bawaan: Umum (Default), HP/Gadget, Aksesoris & Sparepart, Jasa Service.
  - **Tambah Template Baru**: User bisa menambahkan template custom dengan nama dan teks sendiri.
  - **Hapus Template**: Semua template kecuali "Umum (Default)" bisa dihapus (termasuk template bawaan HP, Aksesoris, Servis).
  - **Reset ke Default**: Template bawaan yang sudah diedit bisa di-reset ke teks default.
  - Template custom otomatis muncul di dropdown pemilih template di form Invoice.
- **Katalog Model HP**: Import/Export CSV, reset ke default.
- **Bahasa (Language Toggle)**: ID / EN toggle button. Seluruh UI diterjemahkan termasuk:
  - Bottom navigation labels
  - Dashboard stat labels & value spans
  - View switcher buttons
  - Filter chips
  - Step titles (Invoice form)
  - Card titles & profit/loss labels
  - Buttons, placeholders, toast messages
  - Laporan periode label & month names
  - Topbar greeting & date
- **Tema (Theme Toggle)**: Dark Mode 🌙 / Light Mode ☀️ toggle button.
- **Backup & Restore**:
  - Ekspor Backup (JSON): Invoice, produk, pengeluaran, profil toko, template, penomoran.
  - Impor & Restore dari file JSON.
  - Reset terpisah: Reset Transaksi (mengembalikan stok) dan Reset Produk.
  - Card ringkasan data real-time: jumlah Invoice, Produk, dan Piutang.

### F. Laporan & Pengeluaran
- **Selector Periode**: dropdown bulan + tahun, auto-generate 4 tahun ke belakang, refresh otomatis.
- **Laporan Laba / Rugi per bulan**:
  - Pendapatan = `amountPaid` invoice di periode (invoice lama fallback ke `grandTotal`).
  - HPP = `priceBuy` produk yang terjual via invoice di periode (cross-ref `productId`).
  - Laba Kotor = Pendapatan − HPP.
  - Laba Bersih = Laba Kotor − Total Pengeluaran (merah jika rugi).
  - Ringkasan: jumlah Invoice, Unit Terjual, Piutang Baru di bulan itu.
- **Pencatatan Pengeluaran**: 7 kategori (Sewa Toko, Listrik & Air, Gaji Karyawan, Belanja Stok, Transportasi, Iklan & Promosi, Operasional Lain). Fitur tambah, edit, dan hapus pengeluaran.
- **Bilingual Period Label**: "Periode: Juni 2026" (ID) / "Period: June 2026" (EN).

---

## 4. Struktur Data Utama

### Invoice Object
```json
{
  "invNo": "BC/0001/VI/2026",
  "dateVal": "2026-06-18",
  "dateFormatted": "18 Juni 2026",
  "custName": "Budi Santoso",
  "custPhone": "08123456789",
  "custAddress": "-",
  "warrantyType": "personal | resmi | none",
  "warrantyDur": "1 Bulan",
  "payment": "Cash",
  "paymentStatus": "lunas | dp | belum_bayar",
  "amountPaid": 2500000,
  "amountRemaining": 0,
  "paymentHistory": [
    { "date": "18 Jun 2026", "amount": 500000, "note": "DP awal" }
  ],
  "discount": 0,
  "subtotal": 2500000,
  "grandTotal": 2500000,
  "notes": "Garansi berlaku sejak...",
  "items": [
    { "name": "Samsung A55", "imei": "123456789", "qty": 1, "price": 2500000, "sub": 2500000, "productId": 1718700000000 }
  ],
  "custSignature": ""
}
```

### Product Object
```json
{
  "id": 1718700000000,
  "brand": "Samsung",
  "model": "Galaxy A55",
  "ram": "8GB",
  "storage": "256GB",
  "color": "Navy",
  "condition": "Baru",
  "priceBuy": 2100000,
  "priceSell": 2500000,
  "source": "Distributor ABC",
  "warrantyType": "resmi",
  "imei": "352000001234567",
  "notes": "",
  "status": "Tersedia | Terjual",
  "log": [
    {
      "timestamp": "18/06/2026 12:35:10",
      "action": "Stok Masuk",
      "notes": "Harga Beli: Rp 2.100.000 | Supplier: Distributor ABC"
    },
    {
      "timestamp": "18/06/2026 12:40:22",
      "action": "Terjual (Stok Keluar)",
      "notes": "No Invoice: BC/0001/VI/2026 | Pelanggan: Budi Santoso"
    }
  ]
}
```

### Expense Object
```json
{
  "id": 1718700000001,
  "date": "2026-06-18",
  "dateFormatted": "18 Jun 2026",
  "category": "Listrik & Air",
  "amount": 350000,
  "note": "Bayar listrik PLN bulan Juni"
}
```

### Templates Object (localStorage: `bagaskara_templates`)
```json
{
  "umum": "Barang yang sudah dibeli tidak dapat ditukar...",
  "hp": "Garansi berlaku sejak tanggal invoice diterbitkan...",
  "aksesoris": "Aksesoris tidak bergaransi kecuali...",
  "servis": "Garansi perbaikan/servis hanya berlaku...",
  "laptop": "Custom template text by user...",
  "custom": ""
}
```

---

## 5. Keinginan Pengguna & Pola Desain (Aesthetics)

- **Desain Premium**: Tema gelap modern (*dark mode*) dan tema terang (*light mode*) dengan aksen oranye (*dark-orange theme*), font Google Fonts (Outfit), efek glassmorphism, dan transisi mikro halus agar terasa premium di mobile.
- **Bilingual UI**: Seluruh antarmuka mendukung Bahasa Indonesia dan English, disimpan di `localStorage` dan diterapkan melalui sistem `translations` map + helper `_translateEl()`.
- **Offline & Portabel**: Aplikasi tidak bergantung pada server internet. Semua data di lokal perangkat.
- **Kompatibilitas APK**: Setiap modifikasi pada `www/index.html` harus disinkronkan via:
  ```powershell
  cmd /c "npm run sync"
  cmd /c "cd android && gradlew.bat assembleDebug"
  ```

---

## 6. Rekomendasi & Saran Teknis untuk AI Agent

### A. Sinkronisasi & Kompilasi APK

```powershell
# Sync web assets ke Android
cmd /c "npm run sync"

# Build APK debug
cmd /c "cd android && gradlew.bat assembleDebug"

# Copy APK ke lokasi user
Copy-Item "android\app\build\outputs\apk\debug\app-debug.apk" "C:\Users\rifen\Downloads\BagaskaraCell.apk" -Force
```

Output APK ada di: `android/app/build/outputs/apk/debug/app-debug.apk`

> **Note**: Pada PowerShell user ini, `npm` harus dijalankan via `cmd /c "npm ..."` karena execution policy membatasi script .ps1.

### B. Konsistensi UI/UX & Desain
- Variabel CSS: `--or` (`#F7931A`) aksen oranye, `--bk2` (`#1e1e1e`) latar kartu, `--bk3` (`#2d2d2d`) input.
- Dropdown kustom: gunakan `.cs-wrap` + `csToggle()`. Untuk trigger callback setelah pilih, tambahkan `data-onchange="namaFungsi"` pada `.cs-trigger`.
- Modal bottom sheet: gunakan pola `.cicilan-overlay` + `.cicilan-sheet` yang sudah ada.
- Badge status: gunakan kelas `.pay-badge .pay-badge-lunas/.pay-badge-dp/.pay-badge-hutang` untuk konsistensi warna.
- **Light Theme**: Semua elemen kartu, input, dan nav memiliki override di `body.light-theme` block CSS.

### C. Penanganan Data & Tipe Data di LocalStorage
- ID dibuat dengan `Date.now()` — selalu gunakan `parseInt()` atau `==` (bukan `===`) saat mencocokkan ID dari dataset DOM.
- Selalu gunakan `try-catch` saat `JSON.parse()` dari localStorage.
- Invoice lama (sebelum Tahap 3) tidak punya `paymentStatus` — selalu fallback: `inv.paymentStatus || 'lunas'`.
- Backward compatibility backup: cek `importObj._version` untuk tahu field apa yang tersedia.

### D. Generasi PDF & Share WhatsApp

- **Library**: `html2pdf.js` (via CDN) + `html2canvas` bawaan bundle.
- **Elemen sumber**: `#print-area` (sama dengan `div.preview-box`) — clone element ini yang dirender ke PDF.
- **Penting — Clone Positioning**: Clone harus diposisikan off-screen dengan `position: fixed; left: -99999px`, **BUKAN** `z-index: -9999`. Elemen dengan z-index sangat negatif tidak dirender html2canvas dan menghasilkan PDF kosong/blank.
- **html2canvas options wajib**: `useCORS: true`, `allowTaint: true`, `backgroundColor: '#ffffff'`, `windowWidth: <lebar clone>`.
- **Native path (Capacitor)**: PDF blob → base64 → `CapFilesystem.writeFile()` ke `Documents/<pdfFolder>/` → `CapShare.share()` dengan URI file.
- **Browser fallback**: `navigator.share({ files: [pdfFile] })` → jika tidak support, trigger download otomatis.

### E. Sistem Lokalisasi (i18n)
- **Translations map**: Objek `translations` di JS berisi dua key: `en` dan `id`. Setiap key berisi mapping `"Teks Indonesia": "English Text"`.
- **Helper function**: `_translateEl(el, tMap, lang)` — menerjemahkan `textContent` sebuah elemen. Skip elemen yang punya children (kecuali step-title yang dihandle khusus via text node).
- **Step titles** (Invoice form): Elemen `.step-title` memiliki child `<span class="step-badge">`, sehingga ditranslate via **text node matching** (bukan `textContent`).
- **Topbar greeting**: Diupdate oleh `updateTopbarGreeting()` — dipanggil saat load dan saat bahasa berubah.
- **Laporan tab**: `renderLaporanTab()` menggunakan month names sesuai bahasa aktif.
- Saat menambahkan teks baru ke UI, **selalu tambahkan key** ke kedua map (en & id) di objek `translations`.

### F. Template Catatan (Dynamic System)
- **Built-in templates**: `umum`, `hp`, `aksesoris`, `servis` — didefinisikan di `defaultTemplates` dan `builtInTemplateLabels`.
- **Custom templates**: Disimpan sebagai key tambahan di objek `bagaskara_templates` di localStorage.
- **Functions**:
  - `renderTemplateSettingsList()` — render daftar template di halaman Settings.
  - `populateTemplateSelector()` — populate dropdown `#note-template-options` di form Invoice.
  - `addNewCustomTemplate()` — tambah template baru via prompt.
  - `removeTemplate(key)` — hapus template (semua kecuali 'umum').
  - `resetBuiltInTemplate(key)` — reset template bawaan ke default.
  - `saveTemplateSettings()` — simpan semua template ke localStorage.

### G. Live Total Banner (Penting!)
- Banner `position: fixed` **HARUS** berada di **luar** elemen `.tab-content` (`#tab-form`).
- **Alasan**: Animasi `fadeIn` pada `.tab-content` menggunakan `transform: translateY()` yang membuat **containing block baru**, sehingga `position: fixed` pada child menjadi relatif terhadap parent (bukan viewport).
- Banner dikontrol visibilitasnya via `switchTab()`: ditampilkan hanya saat tab `form` aktif.

### H. Navigasi Tab
Aplikasi memiliki **5 tab** di bottom nav:
| ID Tab | Label (ID/EN) | Trigger saat buka |
|---|---|---|
| `dashboard` | Beranda / Home | `updateDashboardStats()` |
| `form` | Invoice | show `#live-banner` |
| `history` | Riwayat / History | `renderHistoryList()` |
| `products` | Produk / Products | `renderProductList()` |
| `settings` | Setelan / Settings | `updateBackupSummary()` |

Dashboard memiliki **view switcher** (Ringkasan / Laporan Bulanan) yang menampilkan `renderLaporanTab()` saat beralih.

---

## 7. Roadmap Selanjutnya

Semua tahap awal sudah selesai. Ide pengembangan berikutnya yang bisa dipertimbangkan:

- **Notifikasi Jatuh Tempo Piutang**: Alert otomatis untuk piutang yang sudah melewati X hari.
- **Laporan Stok**: Ringkasan produk yang paling cepat terjual, nilai stok saat ini, dan riwayat harga beli.
- **Multi-Toko / Multi-User**: Profil toko terpisah untuk lebih dari satu counter.
- **Export Laporan PDF**: Cetak laporan laba/rugi bulanan sebagai file PDF.
- **Grafik Visual**: Chart omset harian/bulanan menggunakan library ringan (misal Chart.js).
- **QRIS Payment Integration**: Integrasi pembayaran QRIS untuk kemudahan transaksi digital.

---

## 8. Log Pembaruan Terakhir (Update Database Erafone & Fix PDF)

Bagian ini mencatat pembaruan besar, kendala yang dihadapi, dan solusi teknis yang diterapkan pada sesi pengerjaan terakhir.

### A. Update Sistem Katalog Produk (Database Erafone)
- **Kendala**: Import database dari `update database.csv` (815+ entri) melalui sistem `fetch()` sebelumnya sering mengalami masalah *caching* di mobile, dan sistem lama memerlukan manajemen stok yang tidak relevan untuk database Erafone. Pengguna juga kesulitan melakukan *filter* karena UI filter sebelumnya tersembunyi dan tidak mendukung pemilihan ganda.
- **Solusi**: 
  - Mengubah arsitektur *parser* menggunakan skrip Python eksternal (`parse_erafone.py`) untuk mem- *build* file JavaScript statis (`phone-catalog.js`). Objek `window.ERAFONE_CATALOG` langsung diinjeksi ke aplikasi, 100% menghilangkan masalah *cache*.
  - Mengimplementasikan `localStorage` versi `v2` (`bagaskara_products_v2`) untuk memisahkan produk kustom milik pengguna dari database statis Erafone.
- **Update UI**: 
  - Merombak *Filter Modal*: Kategori diletakkan di atas Merek.
  - Menerapkan **Multi-Select Filter** menggunakan objek `Set()` di JavaScript. Pengguna sekarang dapat menekan banyak tombol merek/kategori sekaligus (ditandai dengan *class* `active` / warna oranye), dan memiliki tombol "Semua" yang secara otomatis mereset pilihan.

### B. Perbaikan Bug PDF Invoice (Blank & Gagal Share)
- **Kendala 1 (PDF Blank)**: Saat menekan tombol "Bagikan WA" dari Riwayat, `html2canvas` menghasilkan PDF putih kosong di Android.
- **Solusi 1**: Mengganti teknik *cloning* dari yang sebelumnya dilempar ke luar layar (`left: -99999px`) menjadi `position: fixed` dengan `width: 800px` dan `z-index: -9999`. Teknik lama dianggap elemen tidak valid oleh *engine WebView* Android sehingga tidak di- *render*, sedangkan teknik baru memanipulasi *stacking context* secara aman.
- **Kendala 2 (File Not Found saat Share)**: Fitur bagikan menampilkan *toast* "Invoice disimpan" tapi file gagal terkirim ke WhatsApp. Ini terjadi karena Android 11+ memblokir akses file `DOCUMENTS` tanpa *permission* eksplisit, dan `FileProvider` Capacitor kesulitan membaca *path* tersebut.
- **Solusi 2**: Mengubah jalur penyimpanan file. PDF sekarang dipaksa disimpan ke direktori `CACHE` internal (yang 100% kebal dari *permission blocking* Android) khusus untuk dikirim via WA, lalu aplikasi "mengetuk pintu" meminta izin `CapFilesystem.requestPermissions()` sebelum menyimpannya ke `DOCUMENTS` sebagai cadangan.

### C. Perbaikan Tipografi & Tata Letak PDF (Layout Tergencet & Tumpang Tindih)
- **Kendala 3 (Teks Tumpang Tindih)**: Di versi mobile, spasi antar kata hilang (contoh: `Nama:IstrikuTercinta`) karena `html2canvas` gagal menghitung metrik *font custom* (`Outfit`) dan terpengaruh *subpixel rounding* dari layar HP resolusi tinggi.
- **Solusi 3**: 
  - Mengunci *font* khusus elemen `.preview-box` (area cetak) menjadi `Arial, Helvetica, sans-serif !important`.
  - Mereset jarak huruf `letter-spacing: 0 !important` dan menambahkan `text-rendering: geometricPrecision !important` untuk presisi gambar metrik.
  - Menyelipkan entitas HTML spasi mati (`&nbsp;`) setelah tag `<strong>` pada nama/invoice agar Android tidak menelan (*collapse*) spasi kosong tersebut.
- **Kendala 4 (Layout Sempit/Tergencet)**: Desain PDF terlihat "tidak aturan" karena `html2canvas` menangkap lebar kanvas berdasarkan lebar layar HP (`original.offsetWidth` ~360px), lalu memelarkannya ke ukuran A4.
- **Solusi 4**: Menanamkan *hardcode* lebar mutlak `width: 800px` pada elemen *clone* dan kontainer *wrapper*, serta menset parameter `windowWidth: 800` pada konfigurasi `html2canvas`. Ini menipu *engine* HP agar berpikir bahwa ia adalah layar komputer lebar saat memproses gambar, menghasilkan tabel dan tata letak berproporsi desktop A4 yang lega dan presisi.
