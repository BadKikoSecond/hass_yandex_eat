"""Prepare repository logo from the source PNG with transparent background."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "logo-source.png"
ASSETS_ICON = ROOT / "assets" / "icon.png"
HA_ICON = ROOT / "custom_components" / "yandex_eat" / "icon.png"
BRAND_ICON = ROOT / "custom_components" / "yandex_eat" / "brand" / "icon.png"
BRAND_ICON_2X = ROOT / "custom_components" / "yandex_eat" / "brand" / "icon@2x.png"


def remove_white_background(img: Image.Image, threshold: int = 248) -> Image.Image:
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if r >= threshold and g >= threshold and b >= threshold:
                pixels[x, y] = (r, g, b, 0)
    return rgba


def save_resized(img: Image.Image, path: Path, size: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(path, format="PNG", optimize=True)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Source logo not found: {SOURCE}")

    transparent = remove_white_background(Image.open(SOURCE))
    save_resized(transparent, ASSETS_ICON, 512)
    save_resized(transparent, HA_ICON, 256)
    save_resized(transparent, BRAND_ICON, 256)
    save_resized(transparent, BRAND_ICON_2X, 512)
    print(f"Wrote {ASSETS_ICON}")
    print(f"Wrote {HA_ICON}")
    print(f"Wrote {BRAND_ICON}")
    print(f"Wrote {BRAND_ICON_2X}")


if __name__ == "__main__":
    main()
