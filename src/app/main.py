"""Alur start: folder -> log -> settings -> single instance -> window -> mainloop."""
from .core.errors import install_global_handlers
from .core.logger import get_logger, setup_logging
from .core.settings import Settings
from .core.single_instance import SingleInstance
from .meta import APP_ID, APP_NAME, APP_VERSION
from .paths import SETTINGS_FILE, ensure_dirs

try:  # daftarkan dukungan AVIF di Pillow bila terpasang
    import pillow_avif  # noqa: F401
except ImportError:
    pass


def run() -> None:
    ensure_dirs()
    setup_logging()
    log = get_logger(__name__)
    log.info("Start %s v%s", APP_NAME, APP_VERSION)

    window = None

    def activate() -> None:
        if window:
            window.run_on_ui(window.show_window)

    guard = SingleInstance(APP_ID, activate)
    if not guard.acquire():
        return  # sudah ada instance lain, dia sudah disuruh tampil

    from .ui.app_window import AppWindow  # import UI setelah lolos single-instance

    window = AppWindow(Settings(SETTINGS_FILE))
    install_global_handlers(lambda t, m: window.run_on_ui(lambda: window.show_error(t, m)))
    guard.start_listening()
    try:
        window.mainloop()
    finally:
        guard.release()
        log.info("Exit")
