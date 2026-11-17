# Balancia — tokens (readable summary)

A summary for people. **The source is [`app.rnc/src/styles/theme/themes/balancia.css`](../app.rnc/src/styles/theme/themes/balancia.css)**. Where this file and the CSS disagree,
the CSS wins. Machine copy: [`design-system/tokens.json`](design-system/tokens.json), which
`design-system/extract.py` generates.

## Brand

| Token | Value | Role |
| --- | --- | --- |
| `--brand-teal` | `#0e5a5c` | Primary; 7.97:1 on white |
| `--brand-mint` | `#2fb7a3` | Accent; 7.48:1 on `#0b1416`; never text on light |
| `--brand-pale-mint` | `#bfeee5` | The logo's lower form on dark only |

The primary ramp `--color-primary-50 … 950` is `brandPalette('#0e5a5c', '#2fb7a3')`: exactly what the
app computes at runtime for the platform firm (rnc-4, `brandPalette.ts`). `extract.py` fails if they
drift apart.

| 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 950 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `#e6f6f4` | `#c0e9e3` | `#8dd7cc` | `#2fb7a3` | `#35948c` | `#0e5a5c` | `#0c4c4e` | `#0a3f40` | `#083233` | `#062425` | `#041617` |

## Neutrals (teal-tinted, Balancia's own screens only)

| Role | Light | Contrast | Dark | Contrast |
| --- | --- | --- | --- | --- |
| canvas | `#ffffff` | | `#0b1416` | |
| panel | `#f2f6f6` | | `#111d20` | |
| panel-muted | `#e2eaea` | | `#17262a` | |
| heading | `#0f1f20` | 16.97:1 | `#e8f6f3` | 16.79:1 |
| body | `#1b2b2c` | 14.70:1 | `#d3e3e1` | 14.07:1 |
| muted | `#506264` | 6.42:1 | `#8ea3a2` | 7.03:1 |
| subtle | `#6f8384` | 4.00:1, large text only | `#728887` | 4.96:1 |
| line | `#d3dede` | | `#22363a` | |
| line-strong | `#c3d0d0` | | `#2e464a` | |

Ratios are measured on canvas. Firm tenants keep the bootstrap's warm neutrals.

## Type

**Manrope** for everything, weights 400 to 800 (OFL, `design-system/assets/fonts/`). `--font-mono`
stays the bootstrap's Sometype Mono, for codes, CNPJs and numeric tables.

| Style | Size / weight | Use |
| --- | --- | --- |
| display | 48 / 800 | Site hero, pitch titles |
| h1 | 32 / 700 | Page titles |
| h2 | 24 / 700 | Section titles |
| h3 | 18 / 600 | Card titles |
| body | 14 / 400 | UI text (the app's base size) |
| label | 13 / 500 | Labels, buttons |
| caption | 12 / 500 | **The floor** |
| figure | inherit / 700, tabular-nums | The number that matters |

## Inherited from the bootstrap (not overridden)

- **Radius:** xs 3 · sm 5 · md 8 · lg 12 · xl 16 px.
- **Shadows and relief:** the bootstrap's `--shadow-*` and `--relief-*`.
- **State colours:** success `#22c55e` · info `#3b82f6` · warn `#f59e0b` · danger `#ef4444`.
- **Motion:** instant 90ms · quick 180ms · calm 320ms · settle 520ms · stagger 55ms.
- **Curves:** settle `cubic-bezier(0.32, 0.72, 0, 1)` · drift `cubic-bezier(0.12, 0.6, 0.25, 1)`.
- **Reduced motion:** everything maps to instant.
