"""Alat bantu developer (satu file).

  python dev.py bump patch|minor|major|X.Y.Z   naikkan versi (config.py + pyproject.toml)
  python dev.py rename "Nama Aplikasi"         ganti nama (exe, _Data, _System, zip ikut otomatis)
  python dev.py icon                           buat ulang placeholder assets/icon.ico & icon.png

Setelah bump/rename, catat di CHANGELOG.md.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "src" / "app" / "config.py"
PYPROJECT = ROOT / "pyproject.toml"


def bump(arg: str) -> None:
    text = CONFIG.read_text(encoding="utf-8")
    m = re.search(r'APP_VERSION = "(\d+)\.(\d+)\.(\d+)"', text)
    if not m:
        sys.exit("APP_VERSION tidak ditemukan di config.py")
    old = ".".join(m.groups())
    major, minor, patch = map(int, m.groups())
    if arg == "major":
        new = f"{major + 1}.0.0"
    elif arg == "minor":
        new = f"{major}.{minor + 1}.0"
    elif arg == "patch":
        new = f"{major}.{minor}.{patch + 1}"
    elif re.fullmatch(r"\d+\.\d+\.\d+", arg):
        new = arg
    else:
        sys.exit(__doc__)
    CONFIG.write_text(re.sub(r'APP_VERSION = "[^"]+"', f'APP_VERSION = "{new}"', text), encoding="utf-8")
    py = PYPROJECT.read_text(encoding="utf-8")
    PYPROJECT.write_text(re.sub(r'(?m)^version = "[^"]+"', f'version = "{new}"', py, count=1), encoding="utf-8")
    print(f"Versi: {old} -> {new}  (catat di CHANGELOG.md)")


def rename(name: str) -> None:
    name = name.strip()
    if not name:
        sys.exit(__doc__)
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    CONFIG.write_text(re.sub(r'APP_NAME = "[^"]+"', f'APP_NAME = "{name}"', CONFIG.read_text(encoding="utf-8")),
                      encoding="utf-8")
    py = PYPROJECT.read_text(encoding="utf-8")
    PYPROJECT.write_text(re.sub(r'(?m)^name = "[^"]+"', f'name = "{slug}"', py, count=1), encoding="utf-8")
    print(f'Nama aplikasi sekarang: "{name}" (catat di CHANGELOG.md)')


def icon() -> None:
    from PIL import Image, ImageDraw

    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((16, 16, 240, 240), radius=56, fill=(31, 106, 165, 255))
    d.polygon([(100, 78), (100, 178), (186, 128)], fill=(255, 255, 255, 255))
    img.save(out / "icon.png")
    img.save(out / "icon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("Icon dibuat di", out)


def main() -> None:
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "bump":
        bump(a[1])
    elif len(a) == 2 and a[0] == "rename":
        rename(a[1])
    elif a == ["icon"]:
        icon()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
