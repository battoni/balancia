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
- **Colour and type:** [`design-system/balancia.css`](design-system/balancia.css) today. When step
  3 copies it into `app.rnc/src/styles/theme/`, **the app's copy wins**. At that point, point
  `extract.py` at the app's file and delete this copy. `tokens.md` is only a summary; the CSS wins.
- **The icon:** `logo/balancia-icon.svg` is the only drawn file. `build.py` generates every other
  file in `logo/`, and the copy in `design-system/assets/logo/`.
- **`design-system/tokens.json` is generated, never hand-written.**

## When something changes

1. **Icon or wordmark:** edit `logo/balancia-icon.svg`, or the ratios in `build.py`. Then run
   `python3 brand/build.py`.
2. **Theme:** edit `design-system/balancia.css`. Then run `python3 brand/design-system/extract.py`,
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
- **Not in the app yet (step 3, rnc-4):**
  - `PLATFORM_NAME` = Balancia.
  - Platform firm colours `#0e5a5c` and `#2fb7a3`, replacing `#1f4e79` and `#f2a900`.
  - Manrope and the teal neutrals on the platform's screens.
  - The logo in `MNavbarBrand` and `ALogo`.
  - The favicon set from `logo/`.
  - The root domain balancia.com.br.
- **Not protected yet:** the domain is unregistered and INPI is unfiled; see
  [`BRIEF.md`](BRIEF.md) and `SURVEY.md`.
