"""Semua path aplikasi. Jangan hitung path di tempat lain."""
import sys
from pathlib import Path

from .meta import APP_ID

FROZEN = getattr(sys, "frozen", False)

if FROZEN:
    BASE_DIR = Path(sys.executable).resolve().parent   # folder tempat exe berada
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))  # = NamaAplikasi_System
else:
    BASE_DIR = Path(__file__).resolve().parents[2]      # root proyek
    RESOURCE_DIR = BASE_DIR

DATA_DIR = BASE_DIR / f"{APP_ID}_Data"   # SEMUA data yang disimpan masuk sini
LOG_DIR = DATA_DIR / "logs"
SETTINGS_FILE = DATA_DIR / "settings.json"
ASSETS_DIR = RESOURCE_DIR / "assets"
ICON_ICO = ASSETS_DIR / "icon.ico"
ICON_PNG = ASSETS_DIR / "icon.png"


def ensure_dirs() -> None:
    for d in (DATA_DIR, LOG_DIR):
        d.mkdir(parents=True, exist_ok=True)
