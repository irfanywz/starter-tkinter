"""Alur start: folder -> log -> settings -> single instance -> window -> mainloop."""
from .config import APP_ID, APP_NAME, APP_VERSION, SETTINGS_FILE, ensure_dirs
from .shared.log import get_logger, install_global_handlers, setup_logging
from .shared.settings import Settings
from .shell.single_instance import SingleInstance

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

    from .shell.window import AppWindow  # import UI setelah lolos single-instance

    window = AppWindow(Settings(SETTINGS_FILE))
    install_global_handlers(lambda t, m: window.run_on_ui(lambda: window.show_error(t, m)))
    guard.start_listening()
    try:
        window.mainloop()
    finally:
        guard.release()
        log.info("Exit")
