"""Tray icon (pystray). Callback dipanggil dari thread pystray -> selalu lewatkan ke window.run_on_ui."""
from typing import Callable

import pystray
from PIL import Image

from ..config import APP_ID, APP_NAME, ICON_PNG
from ..shared.log import get_logger

log = get_logger(__name__)


class Tray:
    def __init__(self, on_show: Callable[[], None], on_quit: Callable[[], None]):
        self.on_show = on_show
        self.on_quit = on_quit
        self.icon: pystray.Icon | None = None

    def start(self) -> bool:
        try:
            image = Image.open(ICON_PNG)
            menu = pystray.Menu(
                pystray.MenuItem("Tampilkan", lambda *_: self.on_show(), default=True),
                pystray.MenuItem("Keluar", lambda *_: self.on_quit()),
            )
            self.icon = pystray.Icon(APP_ID, image, APP_NAME, menu)
            self.icon.run_detached()
            return True
        except Exception:
            log.exception("Tray gagal dibuat")
            self.icon = None
            return False

    def stop(self) -> None:
        if self.icon:
            self.icon.stop()
            self.icon = None
