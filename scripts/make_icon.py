"""Buat placeholder assets/icon.ico & icon.png. Ganti dengan icon asli kapan saja (nama file tetap)."""
from pathlib import Path

from PIL import Image, ImageDraw

out = Path(__file__).resolve().parents[1] / "assets"
out.mkdir(exist_ok=True)
img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle((16, 16, 240, 240), radius=56, fill=(31, 106, 165, 255))
d.polygon([(100, 78), (100, 178), (186, 128)], fill=(255, 255, 255, 255))
img.save(out / "icon.png")
img.save(out / "icon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("icon dibuat di", out)
