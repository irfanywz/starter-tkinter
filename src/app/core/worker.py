"""Jalankan pekerjaan berat di thread lain tanpa membekukan UI."""
import threading
from typing import Any, Callable

from .logger import get_logger

log = get_logger(__name__)


def run_in_background(
    fn: Callable[[], Any],
    ui: Callable[[Callable[[], None]], None],
    on_done: Callable[[Any], None] | None = None,
    on_error: Callable[[Exception], None] | None = None,
) -> None:
    """`ui` = AppWindow.run_on_ui. Callback on_done/on_error dijamin jalan di thread UI."""

    def target() -> None:
        try:
            result = fn()
        except Exception as e:  # noqa: BLE001
            log.exception("Background task gagal")
            if on_error:
                ui(lambda: on_error(e))
        else:
            if on_done:
                ui(lambda: on_done(result))

    threading.Thread(target=target, daemon=True).start()
