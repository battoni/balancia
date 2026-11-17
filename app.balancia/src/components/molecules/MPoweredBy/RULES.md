---
version: 1.0.0
origin: balancia
---

# RULES — MPoweredBy

> For AI agents. Last updated: 2026-11-16 (Balancia rename, step 3).

## Purpose

The product's discreet signature under a firm tenant's pages (brand/SYSTEM.md §5): Balancia's icon at
16px and "powered by {name}". `ThePublicLayout` draws it in the footer's bottom bar whenever the site is
not the platform's own. The e-mail layout carries its own (`api.balancia/resources/views/mail/layout.blade.php`).

## Intentional Decisions

- **One colour, never larger**: `text-muted text-xs`, and the icon is inline SVG painting with
  `currentColor` — the mono version of the mark, coloured by the words beside it.
- **`name` comes from the caller** (`platform.name` from `useFirmBrand`), so the molecule reads nothing
  itself; with no name it draws nothing.
- **The icon is `aria-hidden`**: the words already say the name.

## Do Not

- Make it bigger, give it the brand's colours or a link that competes with the firm's own.
- Show it on the platform's own site — Balancia does not sign under itself.
