---
version: 1.0.0
origin: balancia
---

# RULES — APlatformLogo

> For AI agents. Last updated: 2026-11-16 (Balancia rename, step 3).

## Purpose

Balancia's own mark (brand/SYSTEM.md §5), for the platform firm's screens: the root site, the console's
rail, the root's sign-in. `ALogo` stays the FIRM's mark; this one is the product's. Callers decide with
`useFirmBrand().isPlatform` (`MFirmLogo`, `MNavbarBrand`, `ThePublicLayout`).

**The behaviour contract lives in `.claude/rules/celer-09-brand-mark-contract.md`.**

## Intentional Decisions

- **A raster mark: `<img>` of brand/logo/'s SVGs** (`@Assets` `BALANCIA_LOGO`, `?no-inline`). It takes
  `variant` and `tone` and nothing else — no motion on an `<img>` (celer-09). The files are copies of
  `brand/logo/`; when `brand/build.py` regenerates them, copy them again into `src/assets/brand/balancia/`.
- **`variant`**: `full` the lockup, `min` the icon.
- **`tone="brand"` renders the light and the dark file and lets `dark:` hide one.** Which FILE matches
  the ground is not a colour a token can flip, so this is the one-off `dark:` is for.
- **`tone="inherit"` is the white file**: the mark sits on a filled teal band (the sign-in aside).
- **Sized by the parent's font**, `1.75em` high like `ALogo`; the lockup's 20px minimum holds at the
  app's 14px base (24.5px).
- **`alt` is the wordmark's text, `Balancia`** (`BALANCIA_NAME`), the product's name, never a person's.

## Do Not

- Recolour, stretch, retype or animate it (brand/SYSTEM.md §5).
- Use `ABrandMark`, `ABrandPattern` or `ABrandSignature` for Balancia: they are Battoni Dev's.
- Show it on a firm tenant's screens — a tenant gets `MPoweredBy` at most.
