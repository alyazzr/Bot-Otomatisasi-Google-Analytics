# Manual Konfigurasi API Google Analytics

Panduan ini menjelaskan cara mendapatkan kredensial yang diperlukan untuk menghubungkan Bot Otomatisasi dengan Google Analytics 4. Proses ini melibatkan Google Cloud Console dan halaman Admin Google Analytics.

## Bagian 1: Mendapatkan Kredensial untuk Menarik Laporan (Data API)

Langkah ini bertujuan untuk membuat sebuah **Service Account** yang akan memberikan izin kepada bot untuk membaca data dari properti Google Analytics Anda secara aman.

### Langkah 1: Buat atau Pilih Proyek di Google Cloud Console

1.  Buka [Google Cloud Console](https://console.cloud.google.com/).
2.  Buat proyek baru atau pilih proyek yang sudah ada yang ingin Anda gunakan.

### Langkah 2: Aktifkan Google Analytics Data API

1.  Di menu navigasi, pergi ke **APIs & Services > Library**.
2.  Cari "**Google Analytics Data API**".
3.  Klik pada API tersebut, lalu klik tombol **Enable**. Ini memberikan izin pada proyek Anda untuk menggunakan API ini.

### Langkah 3: Buat Service Account

1.  Di menu navigasi, pergi ke **IAM & Admin > Service Accounts**.
2.  Klik **+ CREATE SERVICE ACCOUNT**.
3.  Beri nama service account (misal: `bot-ga-reporter`) dan deskripsi, lalu klik **CREATE AND CONTINUE**.
4.  Pada bagian **Grant this service account access to project**, pilih peran (role). Untuk membaca data, peran **Viewer** sudah cukup. Klik **CONTINUE**.
5.  Klik **DONE** untuk menyelesaikan pembuatan service account.

### Langkah 4: Buat dan Unduh Kunci JSON

1.  Di halaman Service Accounts, temukan service account yang baru Anda buat dan klik alamat emailnya.
2.  Pindah ke tab **KEYS**.
3.  Klik **ADD KEY > Create new key**.
4.  Pilih tipe kunci **JSON** dan klik **CREATE**.
5.  Sebuah file `.json` akan otomatis terunduh. **Ini adalah kredensial rahasia Anda.**

🚨 **PENTING:**
-   Ganti nama file ini menjadi `credentials.json` (atau nama lain yang mudah dikenali).
-   **JANGAN PERNAH** mengunggah atau melakukan `commit` file `.json` ini ke GitHub.
-   Pastikan nama file ini sudah ada di dalam file `.gitignore` Anda.

### Langkah 5: Beri Izin Service Account di Google Analytics

Langkah terakhir dan paling penting adalah memberi tahu Google Analytics bahwa service account Anda boleh mengakses datanya.

1.  Buka file `.json` yang Anda unduh dan salin alamat email service account (terlihat di field `"client_email"`).
2.  Buka **Google Analytics**, lalu pergi ke **Admin** di pojok kiri bawah.
3.  Pastikan Anda memilih Akun dan Properti yang benar.
4.  Di kolom **Property**, klik **Property Access Management**.
5.  Klik tombol `+` di pojok kanan atas, lalu pilih **Add users**.
6.  Tempelkan alamat email service account di kolom **Enter email addresses**.
7.  Di bagian **Permissions**, berikan peran **Viewer**. Jangan berikan akses "Administrator".
8.  Klik **Add** untuk menyimpan.

Sekarang, bot Anda sudah memiliki izin untuk menarik data laporan dari GA4.

## Bagian 2: Mendapatkan Kredensial untuk Mengirim Data (Measurement Protocol)

Langkah ini bertujuan untuk mendapatkan **Measurement ID** dan **API Secret** yang digunakan untuk mengirim *fake hit*.

### Langkah 1: Dapatkan Measurement ID

1.  Di **Google Analytics**, pergi ke **Admin**.
2.  Di kolom **Property**, klik **Data Streams**.
3.  Pilih *data stream* (website) yang relevan.
4.  **Measurement ID** (dengan format `G-XXXXXXXXXX`) akan terlihat di pojok kanan atas. Salin ID ini.

### Langkah 2: Buat API Secret

1.  Di halaman **Data Streams** yang sama, gulir ke bawah dan klik pada bagian **Measurement Protocol API secrets**.
2.  Jika Anda sudah pernah membuatnya, daftarnya akan muncul. Jika belum, klik tombol **Create**.
3.  Beri nama panggilan untuk secret Anda (misal: `bot-secret-key`).
4.  Klik **Create**. **Secret value** akan muncul. Salin nilai ini.

🚨 **PENTING:**
-   Simpan **API Secret** ini baik-baik. Anda tidak bisa melihatnya lagi setelah menutup jendela ini.
-   Masukkan **Measurement ID** dan **API Secret** ke dalam file konfigurasi lokal Anda (misal: `situs_a.txt`), jangan pernah menyimpannya di dalam kode atau mengunggahnya ke GitHub.

---

Setelah semua kredensial ini Anda dapatkan dan masukkan ke dalam file konfigurasi lokal, bot Anda siap untuk dijalankan sesuai fungsinya.
