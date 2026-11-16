"""Registry halaman. Urutan = urutan menu sidebar. Tambah halaman baru cukup di sini."""
from .about import AboutPage
from .home import HomePage
from .settings import SettingsPage

PAGES = [
    ("home", "Beranda", HomePage),
    ("settings", "Pengaturan", SettingsPage),
    ("about", "Tentang", AboutPage),
]
