# reporting_logic.py (Versi Paling Simpel)

import os
import pandas as pd
from dotenv import load_dotenv
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from datetime import datetime

load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

def baca_info_situs(nama_file: str):
    """Membaca informasi dari file .txt di dalam folder data_situs."""
    path_file = os.path.join('data_situs', nama_file)
    info = {}
    with open(path_file, 'r') as f:
        for line in f:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                info[key.strip()] = value.strip()
    return info

def buat_laporan_per_situs():
    folder_data = 'data_situs'
    try:
        files = [f for f in os.listdir(folder_data) if f.endswith('.txt')]
        if not files:
            print("❌ Tidak ada file .txt ditemukan di folder 'data_situs'.")
            return
    except FileNotFoundError:
        print("❌ Folder 'data_situs' tidak ditemukan.")
        return

    print("\nFile konfigurasi situs yang tersedia:")
    for i, file_name in enumerate(files, 1):
        print(f"  {i}. {file_name}")

    try:
        pilihan = int(input("\nPilih nomor file situs yang ingin dibuat laporannya: ").strip())
        if pilihan < 1 or pilihan > len(files):
            print("⚠️ Nomor yang dipilih tidak valid.")
            return
        nama_file = files[pilihan - 1]
    except ValueError:
        print("⚠️ Masukkan angka yang valid.")
        return

    info_situs = baca_info_situs(nama_file) 
    
    property_id = info_situs['PROPERTY_ID']
    site_name = info_situs['NAMA_SITUS']
    nama_basis_file = os.path.splitext(nama_file)[0]
    nama_file_csv = f"laporan_{nama_basis_file}.csv"
    
    ga_client = BetaAnalyticsDataClient()
    property_name_for_api = f"properties/{property_id}"
    print(f"\n--- Mengambil data untuk '{site_name}' ---")

    request = RunReportRequest(
        property=property_name_for_api,
        dimensions=[Dimension(name="date"), Dimension(name="country")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="28daysAgo", end_date="today")]
    )
    response = ga_client.run_report(request)
    
    report_data = [{'tanggal': r.dimension_values[0].value, 'negara': r.dimension_values[1].value, 'pengguna_aktif': r.metric_values[0].value} for r in response.rows]
    
    final_df = pd.DataFrame(report_data)
    final_df.to_csv(nama_file_csv, index=False)
    print(f"✅ Laporan berhasil disimpan ke file: '{nama_file_csv}'")

def buat_laporan_keseluruhan():
    """Langsung membuat laporan gabungan dari semua file .txt."""
    folder_data = 'data_situs'
    all_report_data = []
    ga_client = BetaAnalyticsDataClient()

    print("--- Memulai Laporan Gabungan ---")
    for nama_file in os.listdir(folder_data):
        if nama_file.endswith(".txt"):
            info_situs = baca_info_situs(nama_file)
            site_name = info_situs['NAMA_SITUS']
            property_id = info_situs['PROPERTY_ID']
            
            print(f"-> Mengambil data dari: {site_name}")
            property_name_for_api = f"properties/{property_id}"
            request = RunReportRequest(property=property_name_for_api, dimensions=[Dimension(name="date")], metrics=[Metric(name="activeUsers")], date_ranges=[DateRange(start_date="7daysAgo", end_date="today")])
            response = ga_client.run_report(request)
            for row in response.rows:
                all_report_data.append({'site_name': site_name, 'tanggal': row.dimension_values[0].value, 'pengguna_aktif': row.metric_values[0].value})

    final_df = pd.DataFrame(all_report_data)
    nama_file_output = f"laporan_gabungan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    final_df.to_csv(nama_file_output, index=False)
    print("\n✅ Laporan gabungan berhasil disimpan.")