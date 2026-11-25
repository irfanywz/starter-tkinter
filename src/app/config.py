"""Nama, versi, dan SEMUA path aplikasi. Satu-satunya tempat menghitung path.
Nama & versi diubah lewat `python dev.py rename|bump`, bukan manual."""
import sys
from pathlib import Path

APP_NAME = "Starter"        # nama tampilan, juga nama root folder di dalam zip
APP_VERSION = "0.2.0"
APP_ID = APP_NAME.replace(" ", "")  # dipakai untuk nama exe, _Data, _System

FROZEN = getattr(sys, "frozen", False)

if FROZEN:
    BASE_DIR = Path(sys.executable).resolve().parent         # folder tempat exe berada
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))  # = <APP_ID>_System
else:
    BASE_DIR = Path(__file__).resolve().parents[2]            # root proyek
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


def feature_data(name: str) -> Path:
    """Folder data milik satu fitur: <APP_ID>_Data/<name>/ (dibuat bila belum ada)."""
    d = DATA_DIR / name
    d.mkdir(parents=True, exist_ok=True)
    return d
