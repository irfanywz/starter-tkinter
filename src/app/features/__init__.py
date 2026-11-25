"""Registry fitur. Urutan = urutan menu sidebar.
Fitur baru: buat folder features/<nama>/page.py (turunan BasePage), lalu tambah 1 baris di FEATURES.
Registry sengaja manual (bukan auto-scan) agar PyInstaller pasti ikut membundle modulnya."""
from .about.page import AboutPage
from .home.page import HomePage
from .settings.page import SettingsPage

FEATURES = [
    ("home", "Beranda", HomePage),
    ("settings", "Pengaturan", SettingsPage),
    ("about", "Tentang", AboutPage),
]
