"""Ganti nama aplikasi: python scripts/rename_app.py "Nama Baru"
Mengubah APP_NAME di meta.py dan name di pyproject.toml. Sisanya (exe, _Data, _System, zip) mengikuti otomatis."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        sys.exit(__doc__)
    name = sys.argv[1].strip()
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    meta = ROOT / "src" / "app" / "meta.py"
    meta.write_text(re.sub(r'APP_NAME = "[^"]+"', f'APP_NAME = "{name}"', meta.read_text(encoding="utf-8")),
                    encoding="utf-8")
    pp = ROOT / "pyproject.toml"
    pp.write_text(re.sub(r'(?m)^name = "[^"]+"', f'name = "{slug}"', pp.read_text(encoding="utf-8"), count=1),
                  encoding="utf-8")
    print(f'Nama aplikasi sekarang: "{name}". Catat di CHANGELOG.md.')


if __name__ == "__main__":
    main()
