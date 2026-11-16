# Balancia — decisions and why

Every decision below was closed by Guilherme Battoni on 16/11/2026. Each one gives the reason it was
chosen and what was rejected. The full answers are in [`SURVEY.md`](SURVEY.md).

| Decision | Why | Rejected |
| --- | --- | --- |
| **Name: Balancia** | Hints at accounting (balanço, balancete) without saying "contábil". Easy on a phone call. Outlives the Reforma. balancia.com.br free; nothing active at INPI in 35/36/41/42 | Partida (a class-42 filing by Performancetech), Haver (registered in 35 and 36), Honora (live legal software), Razão (an accounting firm owns the .com.br), Contrapartida (long; registered in 41), Honorária (runner-up: risk of refusal as descriptive) |
| **Concept: the balance sheet that closes** | Accountants live débito = crédito; it ties straight to the name | Scales of justice (a legal cliché), growth bars (fintech default), a spirit level (too abstract) |
| **Symbol: two rounded forms split by an S-gap (round 2)** | Character and a memorable silhouette, a soft "B", and it survives 16px | Round 1's ten rectangle marks read as UI icons (layout, pause, menu): see [`marks/README.md`](marks/README.md) |
| **Personality: confiável · precisa · profissional** | A buyer who checks the maths and trusts the firm's clients to the product | Humanizada (kept for the voice, not the visuals) |
| **Palette: petrol teal + mint, solid** | Steps out of the segment's corporate blue without turning playful; green-blue reads as balance and money | Ink navy + emerald (too close to the blue crowd), indigo (too "tech"), forest + brass (too traditional), the seed blue + yellow (the gov.br pair) |
| **Typeface: Manrope, heavy** | Geometric-grotesk, precise, free, good pt-BR accents; the heavy weight holds next to the round icon | Semibold 600 (thin beside the icon), Plus Jakarta Sans (friendlier, less neutral), Inter (everywhere) |
| **Voice: "você", direct and calm, numbers first** | Wise's plain speech; the buyer wants the figure | A formal, impersonal voice (Domínio-like); a playful "a gente" voice (too light for fees) |
| **Imagery: real screenshots, real customers** | The repricing letter is the product's best picture | Stock photos of accountants, 3D-tilted mockups, Reforma imagery |
| **Motion: 150–200ms, ease-out, Linear-style** | Polish without spectacle | Static UI (loses the micro-interactions the owner asked for) |
| **Tenant visibility: a discreet "powered by Balancia"** | Free reach without competing with the firm's own brand | Invisible (no reach), visible in the back office (competes with the firm's brand) |

**How the symbol was made:**
1. Round 1: ten marks drawn here. All were rejected.
2. Round 2: the owner ran [`DESIGN-AI-BRIEF.md`](DESIGN-AI-BRIEF.md) in an outside design AI and picked direction 01, "Fluxo em Equilíbrio".
3. The AI's SVG was garbled, so the shape was redrawn here.
4. It was rebuilt once more after the owner saw kinks at zoom. Every join is now smooth and every small corner has one radius.

The brief also stands in for the BRAND-BRIEF.md a designer would get.
