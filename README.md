# Pembuatan Bot Otomatisasi Pelaporan Data Menggunakan Google Analytics API

Proyek ini adalah hasil dari Praktik Kerja Lapangan di **Dinas Komunikasi dan Informatika (Diskominfo) Provinsi Yogyakarta**. Bot ini dirancang untuk mengatasi tantangan pelaporan data Google Analytics 4 (GA4) yang seringkali dilakukan secara manual, memakan waktu, dan rentan terhadap kesalahan manusia (*human error*).

## 📜 Deskripsi

Tujuan utama bot ini adalah mengotomatisasi dua proses kunci: pengiriman data simulasi (*fake hit*) untuk pengujian dan penarikan laporan analitik dari GA4. Dengan menggunakan Google Analytics Data API v1beta, bot ini mengambil metrik dan dimensi yang telah ditentukan, kemudian mengekspornya ke dalam format `.CSV`. File CSV ini dirancang agar dapat langsung terhubung dengan Looker Studio untuk visualisasi data interaktif, sehingga mempercepat alur kerja dan mendukung pengambilan keputusan berbasis data.

## 👥 Tim Pengembang

Proyek ini disusun dan dikembangkan oleh:
-   **Alya Azzahra** (22106050008) 
-   **Yusrina Mastura** (22106050046) 

[cite_start]Sebagai bagian dari program Praktik Kerja Lapangan Program Studi Informatika, Fakultas Sains dan Teknologi, UIN Sunan Kalijaga Yogyakarta[cite: 1, 6, 10, 11, 12].

## ✨ Fitur Utama

Bot ini dioperasikan melalui Command Line Interface (CLI) dan memiliki tiga fungsionalitas utama:

#### 1. Modul Pengirim *Fake Hit*
Fitur untuk melakukan simulasi pengiriman data `page_view` ke GA4, berguna untuk pengujian pelacakan event.
-   Memilih file konfigurasi untuk situs yang berbeda.
-   Menentukan jumlah total *hit* (pengunjung simulasi) yang akan dikirim.
-   Tiga metode penentuan *path* target:
    1.  **Otomatis**: *Scraping* dari sitemap website.
    2.  **Spesifik**: Input manual untuk semua website yang diuji.
    3.  **Dari File**: Menggunakan daftar `TARGET_PATHS` yang ada di file konfigurasi.

#### 2. Modul Generator Laporan
Menarik data analitik secara terprogram dan mengekspornya ke format `.CSV`.
-   Menggunakan **Google Analytics Data API v1beta**.
-   Menarik metrik spesifik: **Users, Sessions, Engaged sessions, Engagement Rate, dan Conversions**.
-   Menarik dimensi spesifik: **date, pagePath, dan sourceMedium**.
-   Menghasilkan laporan per-website atau laporan gabungan.

#### 3. Integrasi Visualisasi
File `.CSV` yang dihasilkan dirancang agar kompatibel dan mudah dihubungkan sebagai sumber data di **Looker Studio**.
-   Memungkinkan pembuatan dasbor interaktif.
-   Menyajikan data secara *real-time* tanpa perlu proses manual tambahan.

## 🛠️ Teknologi yang Digunakan

-   **Bahasa Pemrograman**: Python 3.9 
-   **API**:
    -   Google Analytics Data API v1beta 
    -   Measurement Protocol (GA4) 
-   **Library**: Pandas (untuk mengolah data dan membuat CSV) 
-   **Platform & Tools**: Visual Studio Code, Git, Google Cloud Console, Looker Studio.


### Konfigurasi Kredensial API

Untuk menghubungkan bot dengan Google Analytics, Anda memerlukan beberapa kredensial API. Silakan ikuti panduan lengkapnya di file berikut:

➡️ **[Buka Panduan Konfigurasi API (MANUAL.md)](MANUAL.md)**


## 🚀 Instalasi dan Pengaturan

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/alyazzr/Bot-Otomatisasi-Google-Analytics.git](https://github.com/alyazzr/Bot-Otomatisasi-Google-Analytics.git)
    cd Bot-Otomatisasi-Google-Analytics
    ```

2.  **Buat dan Aktifkan Virtual Environment**
    ```bash
    # Buat environment
    python -m venv venv

    # Aktifkan di Windows
    venv\Scripts\activate
    ```

3.  **Install Dependensi**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi Properti**
    -   Di dalam folder `data_situs`, salin file `config.example.txt` menjadi file `.txt` baru (misal: `diskominfo.txt`).
    -   Buka file `.txt` yang baru dan isi parameter berikut sesuai dengan properti GA4 Anda:
        -   `NAMA_SITUS`
        -   `MEASUREMENT_ID`
        -   `API_SECRET`
        -   `PROPERTY_ID`
        -   `WEBSITE_URL`
        -   `TARGET_PATHS` (pisahkan dengan koma, contoh: `/,/profil,/berita`)
    -   File `.txt` yang berisi data asli ini akan diabaikan oleh Git sesuai aturan di `.gitignore`.

## 🏃 Cara Menjalankan Bot

Jalankan script utama dari terminal. Anda akan disambut dengan menu interaktif.

```bash
python App.py
```
Anda akan melihat menu utama untuk memilih fitur yang ingin dijalankan:
-   **[1] Kirim Fake Hit**
-   **[2] Laporan**
-   **[3] Visualisasi** (pastikan Anda sudah mengatur koneksi ke Looker Studio)
-   **[4] Keluar**

Pilih nomor sesuai dengan fitur yang ingin Anda gunakan dan ikuti instruksi yang muncul di terminal.
