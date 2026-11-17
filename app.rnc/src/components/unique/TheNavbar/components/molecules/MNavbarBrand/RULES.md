---
version: 1.2.0
origin: rnc
---

# RULES — MNavbarBrand

> For AI agents. rnc-4 F2b, 14/11/2026.

## Purpose

The back office's brand block at the top of the rail (`ONavbarDesktop`) and the drawer
(`ONavbarDrawer`): the host firm's tile (`ALogo variant="min"`), its logo text, and the product's
name (`platform.name`, R9) under them.

## Intentional Decisions

- **It reads `useFirmBrand` itself, with no props** (rnc-4 R10): the firm is the app's, not the
  navigation's, and both organisms stay presentational. `TheNavbar` passes nothing for it.
- **Nothing renders until a firm is known** — the tab's stored answer or the API's. `ALogo` falls
  back to a name the build carries when given an empty one; an empty block for one request is better
  than the wrong firm.
- **The tile is the firm's uploaded logo when it has one** (rnc-4 R27, `logoUrl` as `src`); the logo
  text under it stays. During a view-as it is the viewed firm's (the brand is reloaded on start and
  "Sair").
- `data-testid="navbar-firm-name"` and `navbar-platform-name` are what the specs and
  `e2e/brand/two-palettes.spec.ts` read.

- **The platform firm's tile is Balancia's icon** (`APlatformLogo`, Balancia rename step 3), and the
  `platform.name` line is left out there — "Balancia / Balancia" would name the product twice.

## Do Not

- Do not take the firm's name from `VITE_*` or a constant: the same build serves every firm.
