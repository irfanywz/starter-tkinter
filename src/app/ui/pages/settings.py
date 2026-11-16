import os
import subprocess
import sys

import customtkinter as ctk

from ...paths import DATA_DIR
from .base import BasePage


class SettingsPage(BasePage):
    title = "Pengaturan"

    def build(self) -> None:
        s = self.win.settings

        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(anchor="w", pady=6)
        ctk.CTkLabel(row, text="Tema").pack(side="left", padx=(0, 12))
        ctk.CTkOptionMenu(row, values=["System", "Light", "Dark"], command=self._set_theme).pack(side="left")
        row.winfo_children()[1].set(s.get("theme"))

        self.tray_var = ctk.BooleanVar(value=s.get("close_to_tray"))
        ctk.CTkCheckBox(self.body, text="Tombol tutup (X) menyembunyikan ke tray", variable=self.tray_var,
                        command=lambda: s.set("close_to_tray", self.tray_var.get())).pack(anchor="w", pady=6)

        ctk.CTkButton(self.body, text="Buka folder Data", command=self._open_data).pack(anchor="w", pady=6)

    def _set_theme(self, value: str) -> None:
        ctk.set_appearance_mode(value)
        self.win.settings.set("theme", value)

    def _open_data(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if sys.platform == "win32":
            os.startfile(DATA_DIR)  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["xdg-open", str(DATA_DIR)])
