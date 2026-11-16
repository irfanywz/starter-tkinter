"""Penangkap error global: semua error tak tertangani dicatat ke log dan ditampilkan ke pengguna."""
import sys
import threading
from typing import Callable

from .logger import get_logger

log = get_logger("uncaught")


def install_global_handlers(show_error: Callable[[str, str], None]) -> None:
    def hook(exc_type, exc, tb):
        log.error("Uncaught exception", exc_info=(exc_type, exc, tb))
        show_error("Terjadi kesalahan", f"{exc_type.__name__}: {exc}")

    sys.excepthook = hook
    threading.excepthook = lambda a: hook(a.exc_type, a.exc_value, a.exc_traceback)
