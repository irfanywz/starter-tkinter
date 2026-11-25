import customtkinter as ctk


class BasePage(ctk.CTkFrame):
    """Semua halaman fitur turunan kelas ini."""

    title = "Halaman"

    def __init__(self, master, win):
        super().__init__(master, fg_color="transparent")
        self.win = win  # AppWindow: akses settings, toast(), run_on_ui()
        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=22, weight="bold")).pack(
            anchor="w", padx=24, pady=(20, 12))
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self.build()

    def build(self) -> None:
        """Isi halaman: tambahkan widget ke self.body."""

    def on_show(self) -> None:
        """Dipanggil tiap halaman ditampilkan."""
