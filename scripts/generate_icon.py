"""Generate integration icon.png from assets/icon.svg colors."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "custom_components" / "yandex_eat" / "icon.png"
SIZE = 256


def main() -> None:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bg = (26, 26, 46, 255)
    accent = (252, 63, 29, 255)
    yellow = (255, 204, 0, 255)
    white = (255, 255, 255, 255)

    draw.rounded_rectangle((0, 0, SIZE - 1, SIZE - 1), radius=56, fill=bg)
    draw.ellipse((40, 40, 216, 216), fill=accent)
    draw.arc((72, 118, 184, 196), start=200, end=-20, fill=white, width=12)
    draw.ellipse((94, 108, 114, 128), fill=bg)
    draw.ellipse((142, 108, 162, 128), fill=bg)
    draw.pieslice((72, 84, 184, 168), start=180, end=0, fill=white)
    draw.rounded_rectangle((92, 62, 164, 84), radius=11, fill=bg)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
