import requests
import uuid
import os
import time
import random
import webbrowser
import http.server
import socketserver
import threading
import tempfile
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from playwright.sync_api import sync_playwright, Error

def dapatkan_lokasi_pengguna():
    try:
        res = requests.get("http://ip-api.com/json/", timeout=5)
        data = res.json()
        lokasi = f"{data.get('city', '-')}, {data.get('regionName', '-')}, {data.get('country', '-')}"
        return lokasi
    except:
        return "Lokasi tidak diketahui"

def baca_konfigurasi_file(nama_file: str):
    """Membaca detail properti dari file .txt yang diberikan."""
    path_file = os.path.join('data_situs', nama_file)
    if not os.path.exists(path_file):
        print(f"❌ Error: File '{nama_file}' tidak ditemukan.")
        return None
    config = {}
    with open(path_file, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                config[key.strip()] = value.strip() 
            if key == 'TARGET_PATHS':
                paths_raw = [p.strip() for p in value.split(',') if p.strip()]
                config[key] = [p if p.startswith('/') else '/' + p for p in paths_raw]
            else:
                config[key] = value
    required_keys = ['MEASUREMENT_ID', 'API_SECRET', 'WEBSITE_URL']
    if not all(key in config for key in required_keys):
        print(f"❌ Error: File '{nama_file}' tidak lengkap. Butuh 'MEASUREMENT_ID', 'API_SECRET', dan 'WEBSITE_URL'.")
        return None
    config['nama_file_sumber'] = nama_file
    return config

def kirim_pageview(measurement_id, api_secret, path, client_id):
    """Mengirim event page_view. Mengembalikan True jika berhasil."""
    url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"
    judul = path.strip("/").replace("-", " ").capitalize() if path != "/" else "Homepage"
    page_location = f"https://contoh.com{path}"
    payload = {
        "client_id": client_id,
        "events": [
            {
                "name": "page_view",
                "params": {
                    "page_title": judul,
                    "page_location": page_location,
                    "page_path": path,
                    "engagement_time_msec": str(random.randint(100, 500))
                }
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, timeout=5)
        return res.status_code == 204
    except requests.exceptions.RequestException:
        return False

def scrape_situs_untuk_path(base_url: str):
    """Mengambil semua link internal dari sebuah URL menggunakan browser automation."""
    print(f"  -> 🤖 Membuka browser virtual untuk {base_url}...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(base_url, wait_until='networkidle', timeout=30000)
            html_content = page.content()
            browser.close()

            soup = BeautifulSoup(html_content, 'html.parser')
            links = set()
            domain_name = urlparse(base_url).netloc

            for a_tag in soup.find_all("a", href=True):
                href = a_tag['href']
                full_url = urljoin(base_url, href)
                parsed_href = urlparse(full_url)

                if domain_name == parsed_href.netloc:
                    path = parsed_href.path
                    if path:
                        if not path.startswith('/'):
                            path = '/' + path
                        links.add(path)

            
            if not links:
                print(f"  ⚠ Tidak ada path internal yang ditemukan, hanya menggunakan homepage ('/').")
                return ['/']
                
            print(f"  -> ✅ Ditemukan {len(links)} path unik setelah render JavaScript.")
            return sorted(list(links))

    except Error as e:
        print(f"  ❌ Error Playwright: {e}")
        return []
    except Exception as e:
        print(f"  ❌ Terjadi error tak terduga saat scraping: {e}")
        return []

def kirim_hit_via_browser(measurement_id, path, website_url):
    """Membuat file HTML sementara, menjalankan server lokal, dan membukanya di browser."""
    judul = path.strip("/").replace("-", " ").capitalize() or "Homepage"
    client_id = str(uuid.uuid4())
    page_location = f"{website_url.rstrip('/')}{path}"
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{judul}</title>
    <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      // --- PERBAIKAN DI SINI ---
      // Memberitahu config untuk TIDAK mengirim page_view otomatis
      gtag('config', '{measurement_id}', {{
        'send_page_view': false 
      }});
      // --------------------------

      // Hanya event ini yang akan mengirim satu page_view yang valid
      gtag('event', 'page_view', {{
        'page_title': '{judul}',
        'page_location': '{page_location}',
        'page_path': '{path}',
        'client_id': '{client_id}'
      }});
    </script>
</head>
<body>
    <h2>✅ Hit untuk '{judul}' sedang dikirim...</h2>
</body>
</html>
"""
    try:
        # Menjalankan server lokal dan membuka browser
        # (Sisa logika server dan webbrowser Anda tetap sama)
        temp_dir = tempfile.gettempdir()
        original_dir = os.getcwd()
        file_name = f"temp_ga_{uuid.uuid4().hex[:8]}.html"
        full_path = os.path.join(temp_dir, file_name)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        PORT = 9000 + random.randint(0, 99)

        class SilentHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args): pass

        def start_server():
            os.chdir(temp_dir)
            with socketserver.TCPServer(("", PORT), SilentHandler) as httpd:
                httpd.serve_forever()

        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        url = f"http://localhost:{PORT}/{file_name}"
        webbrowser.open(url, new=2)

        time.sleep(4) # Waktu untuk browser memuat
        return True

    except Exception as e:
        print(f"❌ Gagal menjalankan fake hit: {e}")
        return False
    
    finally:
        os.chdir(original_dir)

def dapatkan_total_hit():
    """Meminta pengguna memasukkan jumlah TOTAL hit yang diinginkan."""
    while True:
        try:
            prompt = "Masukkan jumlah TOTAL hit yang diinginkan: "
            jumlah = int(input(prompt).strip())
            if jumlah > 0: return jumlah
            else: print("⚠ Jumlah harus lebih dari 0!")
        except ValueError:
            print("⚠ Masukkan angka yang valid!")

def list_dan_pilih_file_config():
    """Menampilkan file .txt yang tersedia dan meminta pengguna memilih."""
    try:
        files = [f for f in os.listdir('data_situs') if f.endswith('.txt')]
        if not files:
            print("❌ Tidak ada file .txt di folder 'data_situs'.")
            return []
    except FileNotFoundError:
        print("❌ Folder 'data_situs' tidak ditemukan.")
        return []
    
    print("\nFile konfigurasi yang tersedia:")
    for i, file_name in enumerate(files, 1):
        print(f"  {i}. {file_name}")

    prompt_teks = "Pilih nomor file (pisahkan koma jika > 1, atau ketik 'semua'): "
    pilihan_str = input(prompt_teks).strip()

    if pilihan_str.lower() == 'semua':
        return files

    try:
        nomor_terpilih = [int(n.strip()) for n in pilihan_str.split(',')]
        file_terpilih = [files[n - 1] for n in nomor_terpilih if 1 <= n <= len(files)]
        if not file_terpilih: print("⚠ Tidak ada nomor file valid yang dipilih.")
        return file_terpilih
    except (ValueError, IndexError):
        print("⚠ Input tidak valid. Harap masukkan nomor yang benar.")
        return []

def dapatkan_path_target():
     """Meminta pengguna memilih sumber path: otomatis, spesifik, atau dari file."""
     print("\nSilakan pilih metode untuk menentukan path target:")
     print("  1. Otomatis (Scrape dari setiap website)")
     print("  2. Spesifik (Input path manual untuk SEMUA website)")
     print("  3. Dari File (Gunakan 'TARGET_PATHS' dari setiap file .txt)")

     while True:
        pilihan = input("Pilih nomor [1/2/3]: ").strip()
        if pilihan == '1':
            return 'otomatis', []
        elif pilihan == '2':
            prompt = "Masukkan path target (pisahkan dengan koma): "
            input_path = input(prompt).strip()
            paths_raw = [p.strip() for p in input_path.split(',') if p.strip()]
            paths_final = [p if p.startswith('/') else '/' + p for p in paths_raw]
            if not paths_final:
                print("⚠ Tidak ada path valid yang dimasukkan. Coba lagi.")
                continue
            return 'spesifik', paths_final
        elif pilihan == '3':
            return 'file', []
        else:
            print("⚠ Pilihan tidak valid. Harap masukkan 1, 2, atau 3.")

def jalankan_bot_fakehit():
    """Fungsi utama yang telah diperbarui untuk menggunakan mode path."""
    print("\n======================================================")
    print("         📊 BOT FAKE HIT LANJUTAN 📊")
    print("======================================================")

    total_hit_per_properti = dapatkan_total_hit()

    while True:
        nama_file_terpilih = list_dan_pilih_file_config()
        if not nama_file_terpilih:
            input("Tekan Enter untuk keluar...")
            return
        list_konfigurasi = [baca_konfigurasi_file(f) for f in nama_file_terpilih]
        if all(list_konfigurasi): break
        print("❌ Terdapat kesalahan pada file konfigurasi. Silakan pilih kembali.\n")

    # LOGIKA BARU: Dapatkan mode path SATU KALI untuk semua properti
    mode_path, list_path_manual = dapatkan_path_target()

    print("\n------------------------------------------------------")
    sukses_global, gagal_global = 0, 0

    for config in list_konfigurasi:
        print(f"\n--- Memproses Properti: '{config['nama_file_sumber']}' ---")

        list_path_final = []

        # Tentukan list path final berdasarkan mode yang dipilih
        if mode_path == 'otomatis':
            list_path_final = scrape_situs_untuk_path(config['WEBSITE_URL'])
        elif mode_path == 'spesifik':
            list_path_final = list_path_manual
        elif mode_path == 'file':
            # Cek apakah TARGET_PATHS ada di config untuk properti ini
            if config.get('TARGET_PATHS'):
                list_path_final = config['TARGET_PATHS']
                print(f"  -> ℹ Ditemukan {len(list_path_final)} path dari file '{config['nama_file_sumber']}'.")
            else:
                print(f"  -> ⚠ Melewati properti karena mode 'Dari File' dipilih,")
                print(f"     tetapi 'TARGET_PATHS' tidak ditemukan di '{config['nama_file_sumber']}'.")
                continue

        if not list_path_final:
            print(f"  -> ⚠ Melewati properti karena tidak ada path yang bisa diproses.")
            continue

        if mode_path == 'file':
            total_semua_hit = total_hit_per_properti * len(list_path_final)
            print(f"  -> Siap mengirimkan {total_hit_per_properti} hit untuk SETIAP dari {len(list_path_final)} halaman (Total: {total_semua_hit} hit)...")
            for path_target in list_path_final:
                for i in range(total_hit_per_properti):

                    print(f"\n    --- Mengirim hit ke '{path_target}' ({i + 1}/{total_hit_per_properti}) ---")
                    if kirim_hit_via_browser(config['MEASUREMENT_ID'], path_target, config['WEBSITE_URL']):
                        sukses_global += 1
                        lokasi_pengguna = dapatkan_lokasi_pengguna()
                        print(f"          🌍 Lokasi pengunjung (IP bot): {lokasi_pengguna}")
                        print(f"          ✔ Tab browser dibuka untuk '{path_target}'")
                    else:
                        gagal_global += 1
                        print(f"          ❌ Gagal membuka browser untuk '{path_target}'")
                    time.sleep(1)
        else:
            print(f"  -> Siap mendistribusikan {total_hit_per_properti} total hit ke {len(list_path_final)} halaman...")
            for i in range(total_hit_per_properti):
                path_target = list_path_final[i % len(list_path_final)]
                if kirim_hit_via_browser(config['MEASUREMENT_ID'], path_target, config['WEBSITE_URL']):
                    sukses_global += 1
                    lokasi_pengguna = dapatkan_lokasi_pengguna()
                    print(f"      🌍 Lokasi pengunjung (IP bot): {lokasi_pengguna}")
                    print(f"      ✔ Tab browser #{i + 1} dibuka untuk '{path_target}'")
                else:
                    gagal_global += 1
                    print(f"      ❌ Gagal membuka browser untuk '{path_target}'")
                time.sleep(1)

        print("  -> ✅ Selesai untuk properti ini.")

    print("\n\n======================================================")
    print("✨ Proses Sesi Ini Selesai ✨")
    print(f"✔ Total Hit Berhasil: {sukses_global}")
    print(f"❌ Total Hit Gagal: {gagal_global}")
    print("======================================================")

def main():
    """Fungsi utama untuk menjalankan bot dan menawarkan perulangan."""
    print("\n======================================================")
    print("          📊 BOT FAKE HIT GOOGLE ANALYTICS 📊")
    print("======================================================")