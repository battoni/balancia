"""Python port of app.balancia/src/composables/brand/brandPalette.ts (rnc-4), kept identical on purpose.

Used by extract.py to check that the primary ramp in balancia.css is exactly what the app
computes at runtime from the platform firm's two colours. If brandPalette.ts changes, change this.
"""

from __future__ import annotations

AA_MINIMUM = 4.5
DARK_PANEL = (0x14, 0x14, 0x13)
DARK_CANVAS = (0x0A, 0x0A, 0x09)
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
SHADES = {600: 0.15, 700: 0.3, 800: 0.45, 900: 0.6, 950: 0.75}
LIGHTEN_STEP, LIGHTEN_LIMIT, LINEAR_THRESHOLD = 0.1, 10, 0.03928


def parse(hex_: str):
    v = hex_.lstrip("#")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def fmt(rgb) -> str:
    return "#" + "".join(f"{int(round(c)):02x}" for c in rgb)


def mix(a, b, w):
    return tuple(x + (y - x) * w for x, y in zip(a, b))


def luminance(rgb) -> float:
    def lin(c):
        s = round(c) / 255
        return s / 12.92 if s <= LINEAR_THRESHOLD else ((s + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def contrast(a: str, b: str) -> float:
    return ratio(parse(a), parse(b))


def lighten_until_readable(colour, grounds):
    current = colour
    for step in range(LIGHTEN_LIMIT):
        if all(ratio(current, g) >= AA_MINIMUM for g in grounds):
            return current
        current = mix(current, WHITE, LIGHTEN_STEP * (step + 1))
    return WHITE


def brand_palette(primary: str, accent: str) -> dict[str, str]:
    base = parse(primary)
    deepest = mix(base, BLACK, SHADES[950])
    highlight = lighten_until_readable(parse(accent), [deepest, DARK_PANEL])
    tint200 = lighten_until_readable(mix(highlight, WHITE, 0.45), [base])
    tint100 = lighten_until_readable(mix(tint200, WHITE, 0.45), [base])
    link = lighten_until_readable(mix(highlight, base, 0.5), [DARK_CANVAS, DARK_PANEL])
    out = {
        "50": mix(tint100, WHITE, 0.6), "100": tint100, "200": tint200, "300": highlight,
        "400": link, "500": base,
    }
    out.update({str(k): mix(base, BLACK, w) for k, w in SHADES.items()})
    return {f"--color-primary-{k}": fmt(v) for k, v in out.items()}
