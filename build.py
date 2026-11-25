"""Build exe + zip:  uv run python build.py

Hasil:
  dist/<APP_NAME>/<APP_ID>.exe
  dist/<APP_NAME>/<APP_ID>_System/   (= _internal milik PyInstaller, di-rename lewat --contents-directory)
  dist/<APP_NAME> <VERSI>.zip        (root folder di dalam zip: "<APP_NAME>", tanpa versi)
Folder <APP_ID>_Data dibuat otomatis oleh aplikasi saat pertama dijalankan.
"""
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from app.config import APP_ID, APP_NAME, APP_VERSION  # noqa: E402

DIST = ROOT / "dist"
WORK = ROOT / "build"


def main() -> None:
    import PyInstaller.__main__ as pyi

    for d in (DIST, WORK):
        shutil.rmtree(d, ignore_errors=True)

    icon = ROOT / "assets" / "icon.ico"
    if not icon.exists():
        sys.exit("assets/icon.ico tidak ada. Jalankan: uv run python dev.py icon")

    pyi.run([
        str(ROOT / "main.py"),
        "--name", APP_ID,
        "--noconfirm", "--clean", "--onedir", "--windowed",
        "--contents-directory", f"{APP_ID}_System",
        "--paths", str(ROOT / "src"),
        "--icon", str(icon),
        "--add-data", f"{ROOT / 'assets'}{os.pathsep}assets",
        "--collect-all", "customtkinter",
        "--collect-all", "tkinterdnd2",
        "--hidden-import", "pillow_avif",
        "--hidden-import", "pystray._win32",
        "--distpath", str(DIST),
        "--workpath", str(WORK),
        "--specpath", str(WORK),
    ])

    built = DIST / APP_ID
    final = DIST / APP_NAME
    if built != final:
        built.rename(final)

    zip_base = DIST / f"{APP_NAME} {APP_VERSION}"
    shutil.make_archive(str(zip_base), "zip", root_dir=DIST, base_dir=APP_NAME)
    print(f"\nSelesai:\n  folder: {final}\n  zip   : {zip_base}.zip")


if __name__ == "__main__":
    main()
