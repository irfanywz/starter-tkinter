"""Naikkan versi: python scripts/bump_version.py patch|minor|major|X.Y.Z
Mengubah src/app/meta.py dan pyproject.toml. Setelah itu isi CHANGELOG.md."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "src" / "app" / "meta.py"
PYPROJECT = ROOT / "pyproject.toml"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    arg = sys.argv[1]
    text = META.read_text(encoding="utf-8")
    cur = re.search(r'APP_VERSION = "(\d+)\.(\d+)\.(\d+)"', text)
    if not cur:
        sys.exit("APP_VERSION tidak ditemukan di meta.py")
    major, minor, patch = map(int, cur.groups())
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
    META.write_text(re.sub(r'APP_VERSION = "[^"]+"', f'APP_VERSION = "{new}"', text), encoding="utf-8")
    py = PYPROJECT.read_text(encoding="utf-8")
    PYPROJECT.write_text(re.sub(r'(?m)^version = "[^"]+"', f'version = "{new}"', py, count=1), encoding="utf-8")
    print(f"Versi: {cur.group(0).split('\"')[1]} -> {new}  (jangan lupa catat di CHANGELOG.md)")


if __name__ == "__main__":
    main()
