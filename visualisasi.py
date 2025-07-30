import webbrowser
import typer

URL_DASHBOARD = "https://lookerstudio.google.com/reporting/62b8d180-bd38-4791-80a7-081ea9b5e1ce"

def buka_dashboard_visualisasi():
    """Membuka link dasbor visualisasi di browser."""
    typer.echo(f"🚀 Membuka dasbor di browser...")
    try:
        webbrowser.open(URL_DASHBOARD, new=2)
        typer.secho("✅ Dasbor berhasil dibuka.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"❌ Gagal membuka browser. Error: {e}", fg=typer.colors.RED)