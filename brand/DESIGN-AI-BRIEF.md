# Balancia — logo brief for an outside design AI (ChatGPT, Gemini)

Written 16/11/2026 from the full brand survey ([`SURVEY.md`](SURVEY.md), the source of truth) and
the rejected first round ([`marks/README.md`](marks/README.md)). Paste the prompt below as is.
Attach `marks/round-1-rejected.png` so the model sees what was already rejected.

---

## Prompt to paste

You are a senior brand identity designer. Design the logo (symbol + wordmark) for **Balancia**.

**What Balancia is.** A white-label SaaS for Brazilian accounting firms (escritórios de
contabilidade). Each firm gets its own branded website with a free tax-impact diagnostic and
meeting booking, a back office to work its new contacts, and a tool that reprices the fees of the
clients it already has. One-line promise (pt-BR): *"A plataforma que faz o escritório contábil
ganhar clientes novos e cobrar o justo dos que já tem."* The real differentiator is having the whole
package in one place: free tax simulators exist, and marketing CRMs exist without accounting, but
nothing else ties the firm's own site to the funnel and to the fee repricing. The launch demand
comes from Brazil's tax reform (CBS starts 01/01/2027), but the brand must outlive it, since the
transition ends in 2033.

**The name.** "Balancia", capitalised (never all-caps, never all-lowercase). It comes from
*balanço / balancete* (balance sheet, trial balance) and "balance". The idea: the firm's client
portfolio back in balance. Pronounced ba-lan-SEE-a.

**Who sees it.** The buyer is the owner or partner of a small-to-mid Brazilian accounting firm,
35–55 years old, comfortable with software but not technical, who values revenue (more clients,
fairer fees) and wants something that works out of the box. The logo appears on Balancia's own
site, in the sales pitch and in the platform console. End clients mostly see the firm's brand,
with only a small one-colour "powered by Balancia" signature.

**Positioning and personality.** Professional, accessible premium (R$ 490–1.490/month). As
polished as Conta Azul or Omie, never looking like a free tax simulator. Traits: trustworthy,
precise, professional. If it were a person: a sharp young consultant with a spreadsheet. A place:
a bright modern office with glass walls and a whiteboard full of numbers. An object: a precision
ruler with clean marks. It should feel like a well-closed balance sheet, where everything is aligned
and the totals are underlined. It must never look like a generic marketing CRM.

**Concept direction (the owner's choices, a starting point, not a cage).** Metaphor: the balance
sheet that closes, two sides that match (débito = crédito). Raw material: two forms in
equilibrium. The funnel (many contacts narrowing into one client) may hide in the construction,
for example in negative space, but must never be drawn. Abstract geometric symbol, symmetric,
2–3 shapes, slightly softened corners, built with negative space. **The symbol must work alone
as a favicon and stay recognisable at 16×16 px.**

**Typography.** A geometric-grotesk sans (Manrope or Plus Jakarta Sans), semibold (600).
Horizontal lockup with the symbol on the left, balanced, so neither part dominates.

**Colour.** Solid fills only, no gradients.
- Primary: petrol teal `#0e5a5c` (7.97:1 on white).
- Accent: mint `#2fb7a3`. It is never used as text on light backgrounds (2.49:1).
- Dark background: `#0b1416`. On dark backgrounds the mark turns mint, with pale mint `#bfeee5` as the accent.
- The mark must also work in a single colour and in black and white.

**References.** For each, what to adapt and what not to copy:
- Stripe: adapt the typographic precision; not the gradients.
- Wise: adapt the plain voice; not the neon green.
- Mercury: adapt the quiet premium; not the cold near-black.
- Conta Azul: adapt the local clarity; not the blue or the playful illustrations.
- Linear: adapt the minimal geometric symbol and the polish; not the dark developer look.
- Pipefy: adapt the clean geometric mark of a Brazilian B2B company; not the pipe or workflow imagery.

**Forbidden.**
- Shapes: scales of justice; drawn funnels or rockets; upward arrows; rising bar charts; calculators, coins, $ or R$ signs.
- Colours: blue with yellow (Brazilian government look); orange as the main colour (RD Station); red as a brand colour (it means loss to an accountant); generic corporate blue.
- Imagery: Brazilian flag colours or tax-reform imagery; anything that reads as government, cheap, free, or pushy sales.

**What was already tried and rejected (see the attached image).** Ten geometric marks built from
rectangles: a T-account; two pillars on a rule; two blocks over one wide block; a block over a
double underline; a B made of stacked blocks; interlocking L-brackets; a spirit level; a notched
square; and two leaning pages. They passed the 16px test, but the owner disliked all of them. The
diagnosis: literal arrangements of rectangles read as generic UI icons (layout, pause, hamburger
menu, box) rather than as a brand. **Do not give me rectangles arranged in a grid.** I need a form
with character and a memorable silhouette that still carries the idea of two sides in balance and
still survives 16px.

**Deliver.**
1. Six genuinely different directions, each with a one-sentence rationale linking it to "the balance that closes" and a note on how it holds at 16px.
2. For each direction: the symbol alone, the horizontal lockup with "Balancia", and the mark on a dark background.
3. If you can output vectors, give clean SVG: a `viewBox` with no width or height, solid fills, no fonts (the wordmark converted to paths, or left out), no strokes thinner than 40 units on a 512 canvas, a `<g id="icon">` and a `<g id="wordmark">`, and no background rectangle.
4. Then tell me which one you'd pick and why, in two sentences.

---

## Bringing results back

Save what you like into `brand/marks/round-2/` (SVG if possible, PNG otherwise), with the source
(ChatGPT or Gemini) in the file name. Then resume `/battoni-new-brand` in `refine` mode on the
chosen mark: the survey, the synthesis and the palette stay as they are, and phase 4 (16px ladder,
B&W, light/dark, the 15 questions) runs on the new mark before the documents and the design system
are written.
