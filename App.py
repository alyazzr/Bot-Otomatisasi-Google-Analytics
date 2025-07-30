import typer
import os
from fakehit import jalankan_bot_fakehit
from reporting import buat_laporan_per_situs, buat_laporan_keseluruhan
from visualisasi import buka_dashboard_visualisasi
from fakehit import main

def clear_screen():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_laporan():
    """Menampilkan dan mengelola sub-menu laporan."""
    while True:
        clear_screen()
        typer.secho("--- 📖 Menu Laporan ---", fg=typer.colors.BLUE, bold=True)
        typer.echo("[1] Buat Laporan Per Website")
        typer.echo("[2] Buat Laporan Gabungan")
        typer.echo("[3] Kembali ke Menu Utama")
        pilihan = typer.prompt("Pilihan Anda")

        if pilihan == '1':
            buat_laporan_per_situs()
        elif pilihan == '2':
            buat_laporan_keseluruhan()
        elif pilihan == '3':
            return  # Kembali ke menu utama
        else:
            typer.secho("❌ Pilihan tidak valid.", fg=typer.colors.RED)
            continue

        if not tanya_lanjut():
            raise typer.Exit()

def tanya_lanjut():
    """Menampilkan prompt lanjutan setelah selesai suatu aksi."""
    typer.echo("\nApa yang ingin Anda lakukan selanjutnya?")
    typer.echo("[1] Kembali ke menu utama")
    typer.echo("[2] Keluar dari program")
    pilihan = typer.prompt("Pilihan Anda").strip()

    return pilihan == '1'  # True jika kembali ke menu utama, False jika keluar

def main():
    """Fungsi utama yang menjalankan loop menu utama."""
    while True:
        clear_screen()
        typer.secho("🤖 Selamat Datang di Bot Utama 🤖", fg=typer.colors.CYAN, bold=True)
        typer.echo("===================================")
        typer.echo("[1] Kirim Fake Hit")
        typer.echo("[2] Laporan")
        typer.echo("[3] Visualisasi")
        typer.echo("[4] Keluar")
        pilihan = typer.prompt("Pilihan Anda")

        if pilihan == '1':
            while True:
                jalankan_bot_fakehit()
                lanjut = typer.prompt(
                    "Lakukan sesi fake hit lagi? (y/n)",
                    default="n",
                    show_default=False
                ).lower()
                if lanjut != 'y':
                    break

            if not tanya_lanjut():
                break

        elif pilihan == '2':
            try:
                menu_laporan()
            except typer.Exit:
                break  # Jika user pilih keluar dari menu laporan

        elif pilihan == '3':
            buka_dashboard_visualisasi()

            if not tanya_lanjut():
                break

        elif pilihan == '4':
            typer.echo("👋 Sampai jumpa!")
            break

        else:
            typer.secho("❌ Pilihan tidak valid.", fg=typer.colors.RED)
            if not tanya_lanjut():
                break

if __name__ == "__main__":
    main()
