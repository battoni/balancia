# Balancia — Brand survey

> **Source of truth.** Where any other file in `brand/` disagrees with this one, this one wins.
> Answered by Guilherme Battoni (Battoni Dev) on 16/11/2026, in `/battoni-new-brand` (language
> `en`, mode `new`). The product UI is pt-BR; voice samples below are in Portuguese on purpose.

Balancia is the **product** brand (the platform firms subscribe to). It is not a tenant brand: each
accounting firm runs on Balancia under its own name and colours. Franco Contabilidade's navy/cyan
theme is a tenant theme and is not part of this identity.

Naming context (16/11/2026): replaces the placeholder "Hub da Reforma" (`PLATFORM_NAME`,
`api.rnc/config/platform.php`, rnc-4). Chosen over Partida, Haver, Contrapartida and Honorária after
a registro.br and INPI (pePI, radical search) check: balancia.com.br free, nothing active in classes
35/36/41/42.

## 1. Essence

| | |
| --- | --- |
| Official name | **Balancia**, capitalised |
| Meaning | balanço / balancete (balance sheet, trial balance) + balance: the firm's portfolio back in balance |
| What it is | "A plataforma que faz o escritório contábil ganhar clientes novos e cobrar o justo dos que já tem." |
| Problem it solves | Firms lose clients to whoever answers "how much does this change for me?" first, and under-charge the clients they have |
| Transformation | The firm wins new clients through its own branded site and repricing becomes a yearly routine |
| Real differentiator | **The whole package in one place**: the firm's branded site + diagnostic + funnel + the repricing letter. Simulators are free, RD Station has no accounting, BTAX has no funnel |
| If it vanished tomorrow | The firm would lose the balance of its client portfolio: the yearly check that every client pays what they should, plus a steady flow of new ones |

## 2. Central concept

- **Idea / metaphor:** the balance sheet that closes — two sides that match.
- **Visual raw material:** two blocks in equilibrium.
- **Mechanic that can become form:** the funnel narrowing to a client — **only as hidden construction**
  (e.g. negative space), never a drawn funnel (see 6 and 13).

## 3. Personality

- **Traits:** confiável · precisa · profissional.
- **Should look like:** a well-closed balance sheet — everything aligned, totals underlined, calm confidence.
- **Must never look like:** a generic marketing CRM.
- **If it were a person:** a sharp young consultant with a spreadsheet (energy inside sober traits: modern and quick, never loud).
- **If it were a place:** a bright modern office, glass walls, a whiteboard full of numbers.
- **If it were an object:** a precision ruler with clean marks.

## 4. Audience

- Owner/partner of a **small-to-mid accounting firm** (10–300 clients); decides and pays (the `gestao` role).
- **35–55**, comfortable with software but not technical (lives in Domínio/Questor/Omie and WhatsApp).
- Values **revenue** first (new clients, fairer fees).
- Wants **simplicity**: it works out of the box (implementation is done for them).

## 5. Positioning

- **Professional, accessible premium** — matches R$ 490–1.490/month.
- Visual benchmark: **Conta Azul and Omie** polish.
- Must not look like: **RD Station**, **Receita Federal / gov.br**, **Domínio / Questor** (legacy ERPs), **Reforma simulators** (Portal Contábeis, SimuladorDaReforma).
- **Familiar shape, own detail.**

## 6. Symbol

- Symbol + wordmark; the **symbol works alone** (favicon, app icon).
- **Abstract geometric: two blocks that close the balance**, with a closing rule.
- *Superseded 16/11/2026 by round 2:* two complementary **rounded forms** (dark teal over mint) split by a rising S-shaped gap, which together read as a soft "B". Round 1's rectangles were rejected as UI-icon-like; see `marks/README.md`.
- **Must survive 16px** (hard requirement).
- **Shapes to avoid:** scales of justice · drawn funnels and rockets · upward arrows and rising bar charts.
  (Calculators/coins/R$ not vetoed, but kept out: they contradict "precision ruler".)

## 7. Visual language

- **Shapes:** geometric with slightly softened corners.
- **Symmetry:** symmetric — the sides match.
- **Complexity:** extremely simple, 2–3 shapes.
- **Construction:** blocks + negative space. The closing rule must be thick or come from the negative space.

## 8. Typography

- **Manrope** (geometric-grotesk, free, pt-BR accents).
- **Bold (700)**. *Changed 16/11/2026 from semibold 600: next to the round-2 icon, 600 looked thin and 700 matches the chosen reference (owner's call).*
- **Balanced lockup, symbol left.**

## 9. Colour

| Role | Value | Measured |
| --- | --- | --- |
| Primary — petrol teal | `#0e5a5c` | 7.97:1 on white (text OK) · 2.34:1 on `#0b1416` (not on dark) |
| Accent — mint | `#2fb7a3` | 2.49:1 on white (never text on light) · 7.48:1 on `#0b1416` |
| Dark ground | `#0b1416` | |

- **Solid only**, no gradients.
- Must work in one colour, B&W, on light and on dark. On dark grounds the mark is **mint**.
- **Avoid:** blue + yellow together (gov.br) · orange as the main colour (RD Station) · red as a brand colour (loss/debt; errors only).
- The platform firm's seed `#1f4e79` + `#f2a900` (PlatformFirmSeeder, rnc-4) is exactly the vetoed pair and is replaced.

## 10. References

| Brand | Adapt | Do not copy |
| --- | --- | --- |
| Stripe | Typographic precision | The gradients |
| Wise | Plain-language voice | The neon green |
| Mercury | Quiet premium: space, few colours | The near-black coldness |
| Conta Azul | Local, approachable clarity | The blue, the playful illustration |
| Linear | Minimal geometric symbol, product polish **and the micro-interactions** | The dark-first developer aesthetic |
| Pipefy | A clean geometric mark from a Brazilian B2B | Workflow/pipe imagery |

## 11. Competitors

- Segment: Reforma simulators (Portal Contábeis, ITWorks, SimuladorDaReforma), RD Station, Zappy Contábil, BTAX/Inttax.
- **Overused, avoid:** corporate blue everywhere · Brazilian flag colours / Reforma imagery · stock photos of smiling accountants with calculators.
- **Stance:** distance from the simulators; approach Conta Azul/Omie polish.

## 12. Applications and scale

- Favicon + browser tab (console and root site) · navbar/sidebar of the console and root site · pitch deck and proposals · "powered by Balancia" footer in transactional e-mails · login and loading screens.
- Not now: social avatar, docs, print/merch.
- Scale: 16–24px · 32–64px · large; recognisable without the name.

## 13. Restrictions

- **Tenant visibility:** discreet one-colour "powered by Balancia" in tenant footers and e-mails only; the firm's brand leads.
- **Never carry:** "cheap tool / free simulator" · political or government association · aggressive sales ("feche mais", "venda mais").
- The Reforma may appear in **campaign copy**, never as brand imagery (section 11). The partner, his firm and Franco never appear in the brand.

## 14. Voice and tone

- **"Você"**, direct and calm. Short sentences that lead with the number that matters.
- No humour and no emoji in the product.
- Glossary: **escritório** (never "empresa"/"tenant") · **contato** on screen ("lead" stays technical) · **reajuste de honorários** · **diagnóstico**.
- Vetoed words: "grátis" and "simulador" in the brand layer; "feche mais", "venda mais".
- Samples: "Não conseguimos salvar o reajuste. Seus dados estão intactos; tente de novo em instantes." · "Carta pronta: 42 clientes, R$ 18.300 a mais por ano."

## 15. Imagery

- **Product screenshots + real numbers**, minimal photography.
- Photos only of **real customers' firm owners**, natural light, at their desk. Never stock.
- Screenshots: real UI in a frame on a soft teal tint, 12px radius, **no tilt**, no glow.

## 16. Iconography and motion

- **Font Awesome 7 Regular** by default, **Solid only for the active state**; PrimeIcons only inside PrimeVue components.
- Icon without a label: only universal ones (close, search, menu), always with `aria-label`.
- **Motion:** quick and calm, 150–200ms, ease-out, Linear-style micro-interactions; the logo's two blocks settle level on the loading screen.
- **Reduced motion:** nothing moves and everything still works.

## Synthesis — the contract

> "Create a visual identity for Balancia, a white-label growth platform for Brazilian accounting
> firms, aimed at owners and partners of small-to-mid firms, whose core promise is to win new
> clients and charge fair fees to the ones they already have. The brand must convey trust and
> precision. The symbol must visually represent a balance sheet that closes (two sides that match)
> through two symmetric blocks in equilibrium with a closing rule, using a simple geometric language
> with slightly softened corners and negative space, with a semibold geometric-grotesk typeface and
> a solid petrol-teal and mint palette. The identity must work as a favicon, console navbar, pitch
> deck, e-mail signature and loading mark, and stay recognisable at 16px without the name. Avoid
> scales of justice, funnels, arrows and bar charts, the segment's corporate blue, blue-with-yellow,
> and any aesthetic associated with marketing CRMs, government portals or free tax simulators."

Confirmed by Guilherme Battoni, 16/11/2026.

## Concept test (phase 4) — 16/11/2026, on the round-2 mark

Run on `logo/balancia-icon.svg` (round 2, "Fluxo em Equilíbrio", rebuilt with smooth joins after
the owner spotted kinks at zoom). Evidence: `marks/round-2/ladder-src/size-ladder.html` (real
16/32/96px rasters), `marks/round-2/preview.html` (light, dark, grey, black).

| # | Question | Answer |
| --- | --- | --- |
| 1 | Makes sense without the name? | Yes: two forms that fit along one curve, a whole that closes; also reads as a soft "B" |
| 2 | Recognisable small? | Yes: at real 16px the two pieces stay separate and the S-gap stays open |
| 3 | Belongs to the product? | Yes: balance that closes (débito = crédito), the portfolio back in balance |
| 4 | Different from competitors? | Yes: no blue, no %, no chart, no funnel, no scale; round forms in a segment of rectangles and blue |
| 5 | Works in black and white? | Yes: `balancia-icon-mono.svg`; the gap carries the split, not the colour |
| 6 | Light and dark? | Yes: teal/mint on light, mint/pale mint on dark (`balancia-icon-dark.svg`) |
| 7 | Simple to reproduce? | Yes: two paths |
| 8 | Recognisable without detail? | Yes: there is no detail; the silhouette is the mark |
| 9 | Explainable logic? | Yes: "two sides that match, one gap that flows: the balance closes" |
| 10 | Holds if the product grows? | Yes: nothing in it is tied to the Reforma, a tax or a feature |
| 11 | A real product mark, not an illustration? | Yes |
| 12 | Text pairs 4.5:1 in both schemes? | Yes: teal on white 7.97, ink `#e8f6f3` on `#0b1416` 16.79, mint on dark 7.48. Mint is never text on light (2.49). The mint piece on white is 2.49:1; logos are exempt from WCAG 1.4.11, and the teal piece and the gap carry the silhouette |
| 13 | Two writers following section 14 sound the same? | Yes, with the pairs in `SYSTEM.md` §6 |
| 14 | A new photo picked only by section 15 fits? | Yes: the rule is narrow (real screenshots; real customers only) |
| 15 | Any decision only in someone's head? | Closed by writing: wordmark weight and proportions are in `build.py`; the rest is in this file and `SYSTEM.md` |

Changes after the survey, decided by the owner on 16/11/2026: the symbol (round 2 replaces round
1's rectangles, section 6) and the wordmark weight (700 instead of 600, section 8).
