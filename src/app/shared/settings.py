"""Pengaturan sederhana berbasis JSON di folder Data."""
import json
from pathlib import Path
from typing import Any

from .log import get_logger

log = get_logger(__name__)

DEFAULTS: dict[str, Any] = {
    "theme": "System",          # System | Light | Dark
    "close_to_tray": True,      # tombol X menyembunyikan ke tray
    "geometry": "960x600",
    "maximized": False,
}


class Settings:
    def __init__(self, path: Path):
        self.path = path
        self.data: dict[str, Any] = dict(DEFAULTS)
        self.load()

    def load(self) -> None:
        try:
            if self.path.exists():
                self.data.update(json.loads(self.path.read_text(encoding="utf-8")))
        except Exception:
            log.exception("Gagal membaca settings, pakai default")

    def save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            log.exception("Gagal menyimpan settings")

    def get(self, key: str) -> Any:
        return self.data.get(key, DEFAULTS.get(key))

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()
