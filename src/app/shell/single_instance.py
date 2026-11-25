"""Cegah aplikasi dibuka ganda. Instance kedua mengirim sinyal 'show' ke instance pertama lalu keluar."""
import socket
import threading
import zlib
from typing import Callable


class SingleInstance:
    def __init__(self, app_id: str, on_activate: Callable[[], None]):
        self.port = 40000 + zlib.crc32(app_id.encode()) % 20000
        self.on_activate = on_activate
        self._sock: socket.socket | None = None

    def acquire(self) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", self.port))
            s.listen(5)
        except OSError:
            s.close()
            try:  # sudah ada instance lain -> suruh dia tampil
                with socket.create_connection(("127.0.0.1", self.port), timeout=1) as c:
                    c.sendall(b"show")
            except OSError:
                pass
            return False
        self._sock = s
        return True

    def start_listening(self) -> None:
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self) -> None:
        while self._sock:
            try:
                conn, _ = self._sock.accept()
                with conn:
                    if conn.recv(16) == b"show":
                        self.on_activate()
            except OSError:
                break

    def release(self) -> None:
        if self._sock:
            self._sock.close()
            self._sock = None
