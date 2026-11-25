"""Logging ke Data/logs + penangkap error global."""
import logging
import sys
import threading
from logging.handlers import RotatingFileHandler
from typing import Callable

from ..config import LOG_DIR


def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(LOG_DIR / "app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def install_global_handlers(show_error: Callable[[str, str], None]) -> None:
    """Error tak tertangani -> dicatat ke log + ditampilkan ke pengguna."""
    log = get_logger("uncaught")

    def hook(exc_type, exc, tb):
        log.error("Uncaught exception", exc_info=(exc_type, exc, tb))
        show_error("Terjadi kesalahan", f"{exc_type.__name__}: {exc}")

    sys.excepthook = hook
    threading.excepthook = lambda a: hook(a.exc_type, a.exc_value, a.exc_traceback)
