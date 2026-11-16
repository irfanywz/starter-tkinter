import customtkinter as ctk

from ...meta import APP_NAME, APP_VERSION
from ...paths import DATA_DIR
from .base import BasePage


class AboutPage(BasePage):
    title = "Tentang"

    def build(self) -> None:
        for text in (f"{APP_NAME}  v{APP_VERSION}", f"Folder data: {DATA_DIR}"):
            ctk.CTkLabel(self.body, text=text, justify="left", wraplength=640).pack(anchor="w", pady=4)
