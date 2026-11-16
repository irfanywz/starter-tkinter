import time

import customtkinter as ctk

from ...core.worker import run_in_background
from .base import BasePage


class HomePage(BasePage):
    title = "Beranda"

    def build(self) -> None:
        ctk.CTkLabel(self.body, text="Ini halaman contoh. Salin file ini untuk membuat halaman baru.",
                     justify="left").pack(anchor="w", pady=(0, 16))
        ctk.CTkButton(self.body, text="Uji toast", command=lambda: self.win.toast("Halo dari toast!")).pack(
            anchor="w", pady=4)
        self.task_btn = ctk.CTkButton(self.body, text="Uji tugas latar (2 detik)", command=self._run_task)
        self.task_btn.pack(anchor="w", pady=4)

    def _run_task(self) -> None:
        self.task_btn.configure(state="disabled")

        def work():
            time.sleep(2)
            return "Tugas selesai"

        def done(msg):
            self.task_btn.configure(state="normal")
            self.win.toast(msg)

        def fail(e):
            self.task_btn.configure(state="normal")
            self.win.toast(f"Gagal: {e}")

        run_in_background(work, self.win.run_on_ui, done, fail)
