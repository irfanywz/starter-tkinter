import customtkinter as ctk


class Toast(ctk.CTkLabel):
    """Notifikasi singkat di tengah bawah window."""

    def __init__(self, master):
        super().__init__(master, text="", corner_radius=10, fg_color=("gray20", "gray30"),
                         text_color="white", padx=16, pady=8)
        self._job = None

    def show(self, message: str, ms: int = 2200) -> None:
        if self._job:
            self.after_cancel(self._job)
        self.configure(text=message)
        self.place(relx=0.5, rely=0.96, anchor="s")
        self.lift()
        self._job = self.after(ms, self.place_forget)
