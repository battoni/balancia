# Balancia — brand

The identity of **Balancia**, the platform behind every firm in this repo (formerly the placeholder
"Hub da Reforma"). Built 16/11/2026 with `/battoni-new-brand` (language `en`, mode `new`).

## Reading order

| File | Answers |
| --- | --- |
| [`BRIEF.md`](BRIEF.md) | What Balancia is, and what it is not |
| [`SYSTEM.md`](SYSTEM.md) | **The contract**: what to do before making anything new |
| [`tokens.md`](tokens.md) | Colour, type, radius and motion, readable |
| [`SURVEY.md`](SURVEY.md) | **Source of truth**: the 16 sections, the synthesis, the concept test |
| [`BRAND.md`](BRAND.md) | Spec v1: geometry, colour of the mark, lockup, clear space, minimum size |
| [`BRAND-DIRECTION.md`](BRAND-DIRECTION.md) | Every decision, why it was made and what was rejected |
| [`DESIGN-AI-BRIEF.md`](DESIGN-AI-BRIEF.md) | The brief for outside designers or design AIs (stands in for BRAND-BRIEF.md) |
| [`marks/README.md`](marks/README.md) | Round 1 (rejected) and round 2 (chosen), with the 16px verdicts |
| [`design-system/index.html`](design-system/index.html) | The rendered design system (open in a browser; light/dark toggle) |

There is no `image-prompt.md`: the mark is vector and final, so nothing is waiting on an image model.

## Sources of truth

- **Decisions:** `SURVEY.md`. Where another file disagrees, the survey wins.
- **Colour and type:** [`app.rnc/src/styles/theme/themes/balancia.css`](../app.rnc/src/styles/theme/themes/balancia.css), the app's theme
  since step 3 (rnc-4, 16/11/2026). `extract.py` reads it; the copy that lived in `design-system/`
  is gone. `tokens.md` is only a summary; the CSS wins.
- **The icon:** `logo/balancia-icon.svg` is the only drawn file. `build.py` generates every other
  file in `logo/`, and the copy in `design-system/assets/logo/`.
- **`design-system/tokens.json` is generated, never hand-written.**

## When something changes

1. **Icon or wordmark:** edit `logo/balancia-icon.svg`, or the ratios in `build.py`. Then run
   `python3 brand/build.py`.
2. **Theme:** edit `app.rnc/src/styles/theme/themes/balancia.css`. Then run `python3 brand/design-system/extract.py`,
   which rewrites `tokens.json` and `index.html`.
3. **The Claude Design version, once it exists:** revise it with the new `tokens.json`.

`python3 brand/design-system/extract.py --check` fails in three cases:
- `tokens.json` is stale.
- A contrast written in the CSS no longer measures true.
- The primary ramp drifts from the app's `brandPalette`.

You need `fontTools` and `Pillow` for `build.py`, Google Chrome for the PNGs, and git access to the
`feature/rnc-4-white-label-platform` branch for `extract.py`.

## Known gaps

- **Claude Design:** not created. The Artifact tool wasn't available in this session. Create it from
  `design-system/tokens.json` and `design-system/assets/` next time `/battoni-new-brand` runs with
  that tool.
- **The root domain:** `PLATFORM_ROOT_DOMAIN=balancia.com.br` is in `api.rnc/.env.example`, but the
  domain is unregistered, so nothing serves it yet.
- **Not protected yet:** the domain is unregistered and INPI is unfiled; see
  [`BRIEF.md`](BRIEF.md) and `SURVEY.md`.

Done in step 3 (rnc-4, 16/11/2026): `PLATFORM_NAME` = Balancia, the platform firm's slug `balancia`
(`hub` stays reserved), its colours `#0e5a5c` / `#2fb7a3`, Manrope on every screen, the teal neutrals on
the platform's screens (`data-platform`), `APlatformLogo` in `MFirmLogo`, `MNavbarBrand` and the root
site, the favicon set, and the "powered by Balancia" signature in tenant footers and e-mails. Then, the same day: no "hub" left in the copy; Balancia's sign-in has its own panel copy (`auth.platformBrand.*`, no Reforma slogan) on plain teal, without Battoni Dev's `ABrandPattern`; PrimeVue's `surface` ramp is teal-tinted on the platform's screens, each step at the bootstrap's luminance.
