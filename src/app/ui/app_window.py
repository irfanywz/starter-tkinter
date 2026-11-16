"""Window utama: sidebar + area halaman + toast + tray + simpan posisi window."""
import queue
from tkinter import messagebox
from typing import Callable

import customtkinter as ctk

from ..core.logger import get_logger
from ..core.tray import Tray
from ..meta import APP_NAME
from ..paths import ICON_ICO
from .pages import PAGES
from .widgets.toast import Toast

log = get_logger(__name__)


class AppWindow(ctk.CTk):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._ui_queue: queue.Queue[Callable[[], None]] = queue.Queue()

        ctk.set_appearance_mode(settings.get("theme"))
        ctk.set_default_color_theme("blue")
        self.title(APP_NAME)
        self.minsize(720, 460)
        self.geometry(settings.get("geometry"))
        if settings.get("maximized"):
            self.after(50, lambda: self.state("zoomed"))
        self.after(250, self._set_icon)  # CTk menimpa icon di awal, jadi diset belakangan
        self.report_callback_exception = self._on_callback_exception

        self._build()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.tray = Tray(on_show=lambda: self.run_on_ui(self.show_window),
                         on_quit=lambda: self.run_on_ui(self.quit_app))
        self.tray.start()
        self._poll_ui_queue()

    # ---------- layout ----------
    def _build(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(self, width=180, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)
        ctk.CTkLabel(sidebar, text=APP_NAME, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 16))

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=0, column=1, sticky="nsew")

        self.pages = {}
        self.nav_buttons = {}
        for key, label, cls in PAGES:
            self.pages[key] = cls(content, self)
            btn = ctk.CTkButton(sidebar, text=label, anchor="w", fg_color="transparent",
                                text_color=("gray10", "gray90"), hover_color=("gray75", "gray30"),
                                command=lambda k=key: self.show_page(k))
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[key] = btn

        self.toast_widget = Toast(self)
        self.show_page(PAGES[0][0])

    def show_page(self, key: str) -> None:
        for k, page in self.pages.items():
            page.pack_forget()
            self.nav_buttons[k].configure(fg_color="transparent")
        self.pages[key].pack(fill="both", expand=True)
        self.nav_buttons[key].configure(fg_color=("gray75", "gray30"))
        self.pages[key].on_show()

    # ---------- util untuk halaman ----------
    def toast(self, message: str, ms: int = 2200) -> None:
        self.toast_widget.show(message, ms)

    def run_on_ui(self, fn: Callable[[], None]) -> None:
        """Aman dipanggil dari thread mana pun; fn dijalankan di thread UI."""
        self._ui_queue.put(fn)

    def _poll_ui_queue(self) -> None:
        try:
            while True:
                self._ui_queue.get_nowait()()
        except queue.Empty:
            pass
        except Exception:  # noqa: BLE001
            log.exception("Error di callback UI")
        self.after(50, self._poll_ui_queue)

    # ---------- window lifecycle ----------
    def show_window(self) -> None:
        self.deiconify()
        self.lift()
        self.focus_force()

    def on_close(self) -> None:
        self._save_window_state()
        if self.settings.get("close_to_tray") and self.tray.icon:
            self.withdraw()
        else:
            self.quit_app()

    def quit_app(self) -> None:
        self._save_window_state()
        self.tray.stop()
        self.destroy()

    def _save_window_state(self) -> None:
        maximized = self.state() == "zoomed"
        self.settings.data["maximized"] = maximized
        if not maximized and self.state() == "normal":
            self.settings.data["geometry"] = self.geometry()
        self.settings.save()

    def _set_icon(self) -> None:
        try:
            self.iconbitmap(str(ICON_ICO))
        except Exception:  # noqa: BLE001
            pass  # non-Windows / icon tidak ada

    def show_error(self, title: str, message: str) -> None:
        messagebox.showerror(title, message, parent=self)

    def _on_callback_exception(self, exc, val, tb) -> None:
        log.error("Tk callback exception", exc_info=(exc, val, tb))
        self.show_error("Terjadi kesalahan", f"{exc.__name__}: {val}")
