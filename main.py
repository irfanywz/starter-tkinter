"""Entry point. Dipakai `uv run python main.py` dan juga oleh PyInstaller."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from app.main import run  # noqa: E402

if __name__ == "__main__":
    run()
