#!/usr/bin/env python3
"""Build Balancia's logo files from the icon source and Manrope (wght 800, see wordmark()).

    python3 brand/build.py

Reads  brand/logo/balancia-icon.svg          (the hand-built icon, the only drawn source)
       brand/design-system/assets/fonts/Manrope-Variable.ttf
Writes brand/logo/*.svg                      (icon, lockups: light, dark, mono)
       brand/logo/png/*.png, favicon.ico     (rasterised with headless Chrome)
       brand/design-system/assets/logo/      (a copy, for the design system)

The wordmark is converted to outlines here, so no logo file depends on a font being installed.
Rerun after any change to the icon; never edit the generated files by hand.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

BRAND = Path(__file__).resolve().parent
LOGO = BRAND / "logo"
FONT = BRAND / "design-system/assets/fonts/Manrope-Variable.ttf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TEAL, MINT, PALE, INK_LIGHT, INK_DARK = "#0e5a5c", "#2fb7a3", "#bfeee5", "#0e5a5c", "#e8f6f3"

# Icon geometry on its 512 canvas (from balancia-icon.svg): x 82-438, y 52-460.
ICON_BOX = (82, 52, 438, 460)
CAP_RATIO = 0.80      # wordmark cap height / icon height (as in the preview the owner approved, 16/11/2026)
GAP_RATIO = 0.40      # space between icon and wordmark / icon height
TRACKING = -0.02      # letter spacing in em
PAD = 0.12            # clear space around the lockup / icon height


def icon_paths() -> list[tuple[str, str]]:
    source = (LOGO / "balancia-icon.svg").read_text()
    return re.findall(r'<path fill="(#[0-9a-fA-F]{6})" d="([^"]+)"', source)


def wordmark(text: str) -> tuple[str, float, float, float]:
    """Return (path d, width, cap height, units per em) for `text` in Manrope wght 800, baseline at y=0."""
    # wght 800 on purpose: Chrome renders Manrope "font-weight: 700" visibly heavier than the font's
    # own 700 master, and the owner approved that browser render (16/11/2026). Measured side by side,
    # the 800 outlines match it; the 700 outlines look thin next to the icon.
    font = TTFont(FONT)
    glyphs, cmap = font.getGlyphSet(location={"wght": 800}), font.getBestCmap()
    upem = font["head"].unitsPerEm
    cap = font["OS/2"].sCapHeight
    pen, x = SVGPathPen(glyphs), 0.0
    for ch in text:
        name = cmap[ord(ch)]
        glyphs[name].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        x += glyphs[name].width + TRACKING * upem
    width = x - TRACKING * upem
    return pen.getCommands(), width, cap, upem


def lockup(colors: tuple[str, str, str]) -> str:
    """Horizontal lockup: icon left, wordmark right, both vertically centred."""
    top_c, bottom_c, ink = colors
    ix0, iy0, ix1, iy1 = ICON_BOX
    icon_h = iy1 - iy0
    d, w, cap, _ = wordmark("Balancia")
    scale = CAP_RATIO * icon_h / cap
    text_x = ix1 + GAP_RATIO * icon_h
    baseline = iy0 + icon_h / 2 + CAP_RATIO * icon_h / 2
    pad = PAD * icon_h
    vb_x, vb_y = ix0 - pad, iy0 - pad
    vb_w = text_x + w * scale + pad - vb_x
    vb_h = icon_h + 2 * pad
    fills = [top_c, bottom_c]
    icon = "\n".join(f'    <path fill="{fills[i]}" d="{p}"/>' for i, (_, p) in enumerate(icon_paths()))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x:.0f} {vb_y:.0f} {vb_w:.0f} {vb_h:.0f}">\n'
        f'  <g id="icon">\n{icon}\n  </g>\n'
        f'  <g id="wordmark" fill="{ink}" transform="translate({text_x:.2f} {baseline:.2f}) scale({scale:.5f})">\n'
        f'    <path d="{d}"/>\n  </g>\n</svg>\n'
    )


def icon(colors: tuple[str, str]) -> str:
    fills = list(colors)
    paths = "\n".join(f'    <path fill="{fills[i]}" d="{p}"/>' for i, (_, p) in enumerate(icon_paths()))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">\n  <g id="icon">\n{paths}\n  </g>\n</svg>\n'


def rasterize(svg: Path, out: Path, size: int, background: str | None = None) -> None:
    """Render `svg` into a size x size PNG; the icon gets ~10% inner margin on a background."""
    inner = int(size * 0.8) if background else size
    bg = f"background:{background};" if background else ""
    html = (
        f'<html><body style="margin:0;width:{size}px;height:{size}px;display:flex;align-items:center;'
        f'justify-content:center;{bg}"><img src="{svg.as_uri()}" style="width:{inner}px;height:{inner}px">'
        f"</body></html>"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as page:
        page.write(html)
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
         "--default-background-color=00000000", f"--window-size={size},{size}",
         f"--screenshot={out}", Path(page.name).as_uri()],
        check=True, capture_output=True,
    )


def main() -> None:
    files = {
        "balancia-icon.svg": None,  # the source; read, never rewritten
        "balancia-icon-dark.svg": icon((MINT, PALE)),
        "balancia-icon-mono.svg": icon(("#000000", "#000000")),
        "balancia-icon-white.svg": icon(("#ffffff", "#ffffff")),
        "balancia-logo.svg": lockup((TEAL, MINT, INK_LIGHT)),
        "balancia-logo-dark.svg": lockup((MINT, PALE, INK_DARK)),
        "balancia-logo-mono.svg": lockup(("#000000", "#000000", "#000000")),
        "balancia-logo-white.svg": lockup(("#ffffff", "#ffffff", "#ffffff")),
    }
    for name, body in files.items():
        if body is not None:
            (LOGO / name).write_text(body)

    png = LOGO / "png"
    png.mkdir(exist_ok=True)
    source = LOGO / "balancia-icon.svg"
    for size in (16, 32, 48, 64):
        rasterize(source, png / f"favicon-{size}.png", size)
    rasterize(source, png / "apple-touch-icon.png", 180, background="#ffffff")
    rasterize(source, png / "icon-192.png", 192, background="#ffffff")
    rasterize(source, png / "icon-512.png", 512, background="#ffffff")
    rasterize(source, png / "icon-maskable-512.png", 512, background="#ffffff")

    from PIL import Image
    Image.open(png / "favicon-64.png").save(
        LOGO / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
    )
    assets = BRAND / "design-system/assets/logo"
    assets.mkdir(parents=True, exist_ok=True)
    for svg in LOGO.glob("*.svg"):
        (assets / svg.name).write_text(svg.read_text())
    (assets / "favicon.ico").write_bytes((LOGO / "favicon.ico").read_bytes())

    print(f"logo: {len(files)} svg, {len(list(png.glob('*.png')))} png, favicon.ico")


if __name__ == "__main__":
    main()
