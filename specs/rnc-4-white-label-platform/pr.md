# Turn the Reforma hub into a white-label platform for accounting firms — rnc-4

Problem: Franco did not commit to the pilot, so a hub built for one firm (`firm_id` in the tables, but Franco in the header default, the build-time theme, the e-mails, the consent text and the routes) could not be shown to or run for a second firm. Outcome: the hub becomes a white-label subscription for accounting firms (beta first, about two paying firms for about three months): any number of firms on one deploy, each on its own subdomain with its own data, look, name and modules; Battoni Dev operates the platform from a console with an audited "view as"; nothing is deployed.

**Merge #4 first** (this branch sits on the run tooling).

## What was built, by phase

- F1a Firm by host, API: the firm comes from `X-Firm`, login and session are bound to it, 404 for unknown or reserved slugs, registration closed.
- F1b Firm by host, SPA: the host read once at boot, same-origin `/api`, "Escritório não encontrado", local `*.localhost` hosts.
- F2a Firm brand, product name, mail brand and versioned consent, API.
- F2b Runtime brand in both layouts, SPA (palette, logo, names, no flash).
- F2c1 Role `ceo` and `/reinaldo/*` become `gestao` and `/gestao/*`.
- F2c2 Franco and Reinaldo strings go to the host firm; guards that no tenant name appears in code.
- F3a Modules per firm, API (module gate, dependencies, degrade).
- F3b1 `FirmProvisioner` and `firm:create`.
- F3b2 Seeders per firm, the fictional demo firm Alvorada and the platform firm `hub`.
- F3c Modules per firm, SPA (rail, routes, degrade).
- F4a Platform operator and console, API.
- F4b Operator console, SPA.
- F6a Beta signup, API (lead on the platform firm).
- F6b Product site on the root, SPA.
- F5a Firm settings, API (contact, team, specialists' hours, consent versions).
- F5b Firm settings, SPA.
- F4c Logo upload and view-as, API.
- F4d Logo and view-as, SPA (banner, "Sair").
- F7 Deploy readiness: health check, trusted proxies, runbook, env inventory, route classes.
- F9a LGPD: privacy data, lead export and anonymise, `firm:offboard`, API.
- F9b LGPD: privacy page, lead export and anonymise, SPA.
- F7b MySQL 8: schema, seed and the full Pest suite on MySQL.

## R# to A# to test

| R# | A# | Test file::test |
| --- | --- | --- |
| R1, R2 | A1 | `api.rnc/tests/Feature/Firm/FirmByHostTest.php::starts diagnostic in firm, listed manager and never by another firm's team` |
| R3 | A2 | `api.rnc/tests/Feature/Firm/FirmByHostTest.php::A2 — a subdomain that is not a firm` |
| R4 | A3 | `api.rnc/tests/Feature/Auth/LoginFirmTest.php` |
| R5 | A4 | `api.rnc/tests/Feature/Firm/FirmMismatchTest.php` |
| R7 | A5 | `api.rnc/tests/Feature/Auth/RegistrationClosedTest.php` |
| R2, R6, R3 | A6 | `app.rnc/e2e/tenancy/firm-host.spec.ts` |
| R5, R6 | A7 | `app.rnc/e2e/tenancy/firm-host.spec.ts` |
| R8, R9 | A8 | `api.rnc/tests/Feature/Firm/PublicFirmBrandTest.php` |
| R12 | A9 | `api.rnc/tests/Feature/Mail/FirmMailBrandTest.php` |
| R13 | A10 | `api.rnc/tests/Feature/Lead/ConsentVersionTest.php` |
| R10 | A11 | `app.rnc/src/**/useBrandTheme.spec.ts` |
| R10, R11 | A12 | `app.rnc/e2e/brand/two-palettes.spec.ts` |
| R14 | A13 | `app.rnc/src/**/routes.local.spec.ts` |
| R14 | A14 | `api.rnc/tests/Feature/Auth/SeededRolesTest.php` |
| R15 | A15 | `api.rnc/tests/Arch/NoTenantNamesTest.php::in code, config, views, lang or routes` + `app.rnc/src/test/noTenantNames.spec.ts` |
| R15 | A16 | `app.rnc/e2e/brand/no-franco.spec.ts` |
| R16, R17 | A17 | `api.rnc/tests/Feature/Firm/ModuleGateTest.php` |
| R17 | A18 | `api.rnc/tests/Feature/Firm/ModuleCommandsTest.php` |
| R18 | A19 | `api.rnc/tests/Unit/Modules/Firm/FirmModulesServiceTest.php` |
| R19 | A20 | `api.rnc/tests/Feature/Briefing/BriefingDegradeTest.php` |
| R20 | A21 | `api.rnc/tests/Feature/Auth/MeFirmTest.php` |
| R21, R13 | A22 | `api.rnc/tests/Feature/Firm/CreateFirmCommandTest.php` |
| R22, R23 | A23 | `api.rnc/tests/Feature/Seed/DemoFirmSeedTest.php` |
| R17, R20 | A24 | `app.rnc/e2e/tenancy/modules.spec.ts` |
| R19 | A25 | `app.rnc/src/**/BriefingView.view.integration.spec.ts` |
| R24 | A26 | `api.rnc/tests/Feature/Platform/OperatorSignInTest.php` |
| R25, R11 | A27 | `api.rnc/tests/Feature/Platform/PlatformFirmsTest.php` |
| R25, R13 | A28 | `api.rnc/tests/Feature/Platform/ConsentDefaultTest.php` |
| R25 | A29 | `app.rnc/e2e/platform/console.spec.ts` |
| R25 | A30 | `app.rnc/e2e/platform/console.spec.ts` |
| R29 | A31 | `api.rnc/tests/Feature/Lead/BetaSignupTest.php` |
| R28 | A32 | `app.rnc/e2e/product/landing.spec.ts` |
| R29 | A33 | `app.rnc/e2e/product/landing.spec.ts` |
| R28 | A34 | `app.rnc/e2e/product/landing.spec.ts` |
| R30 | A35 | `api.rnc/tests/Feature/Firm/FirmSettingsTest.php` |
| R31 | A36 | `api.rnc/tests/Feature/Auth/FirmUsersTest.php` |
| R32 | A37 | `api.rnc/tests/Feature/Booking/SpecialistHoursTest.php` |
| R33 | A38 | `api.rnc/tests/Feature/Lead/ConsentVersionEndpointTest.php` |
| R30-R33 | A39 | `app.rnc/e2e/firm-settings/settings.spec.ts` |
| R30-R33 | A40 | `app.rnc/e2e/firm-settings/settings.spec.ts` |
| R27 | A41 | `api.rnc/tests/Feature/Platform/FirmLogoTest.php` |
| R26 | A42 | `api.rnc/tests/Feature/Platform/ViewAsTest.php` |
| R26, R27 | A43 | `app.rnc/e2e/platform/view-as.spec.ts` |
| R35 | A44 | `api.rnc/tests/Feature/HealthTest.php` |
| R34, R36 | A45 | `api.rnc/tests/Feature/EnvInventoryTest.php` |
| R37 | A46 | `api.rnc/tests/Feature/Access/Phase4AccessTest.php` |
| R38 | A47 | `api.rnc/tests/Feature/Firm/PublicPrivacyTest.php` + `app.rnc/e2e/site/privacy.spec.ts` |
| R39 | A48 | `api.rnc/tests/Feature/Pipeline/LeadPrivacyTest.php` + `app.rnc/e2e/pipeline/lead-privacy.spec.ts` |
| R40 | A49 | `api.rnc/tests/Feature/Firm/OffboardFirmCommandTest.php` |

R9 (one product-name config), R12 (mail brand) and the rest of R1-R40 not listed on their own are carried by the rows above; R21 and R37 are covered by A22 and A46.

## Verify review

Three `fable-reviewer` slices: security and tenancy, API spec and conventions, SPA.

Accepted and fixed:
- 16 API findings (P1-A1, P1-A2 part, P2-A3, P2-A4, P2-A5, P2-A6, PE1, PE3, P1-C1, P2-C2, P2-C3, P2-C4, P2-C6, three nits) in 6ad129e, 400d16a and 1588a01.
- SPA: P1-S1 and P2-S4 in 474124c; P2-S2, P2-S5, P2-S6 and the API's `platform.viewAsOffboarded` in 03951de; the roles screen kept to the operator (W118) in 970156d.

Not applied, with reason:
- PE2, the cross-firm username and e-mail availability check: inherent to global usernames, recorded as an Auth Known Gap.
- Offboarding of partners, portfolio clients, contracts, NF-e files and assistant notes: Known Gap in Firm RULES, an owner decision.
- P2-S3, the landing news line without a named source: editorial, the owner's call.
- P2-C5, the Platform and Offboarder cross-module read-only repositories: allowed by arcus and declared in the reader's RULES.
- A45 asserts the runbook text: the MySQL run itself is `make test-mysql`, owner-run.

## QA

Layer 1, full gate (14/11/2026, verify's final gate: `make pre-commit` static steps, sanitize, wt-test, then the suites): 2417 Pest · 1540 Vitest · 234 Playwright, all green.

Layer 2, Chrome, rounds 1-7 in the owner's Chrome at 1440 only (window minimum 606 px); 390 covered by Playwright where marked. Bugs found in Chrome and fixed:
- QA login host (13dae23).
- Beta lead detail and consent summary (f68d537 and the beta fields commit).
- Brand caches kept to their host and brand, dropped on logout and "Sair" (bcd247c; 4.11/4.12 prime to principal pinned, W123).
- Operador menu kept to the operator (4ab5397, W124).
- Brand reload on logout (16496bb, W126).
- A lead started under another brand is a new lead of that brand, on resume (76add80, C24, W127).
- 3.4 first-save toast pinned, not reproduced (5600215, W125).

Retest: 3.4 and 4.10 pass; 4.11/4.12 and 5.21 fixed as above; qa-script 5.2 expects the operator's rail by design (AM1). Gate after those fixes: 2419 Pest · 1554 Vitest (`--maxWorkers=2`) · 71 Playwright (site, brand, diagnostic, platform), all green; `make check-app` and `make sync-mirror-check` clean.

Final retest of 4.10–4.12, 5.2, 5.21 (14/11, 18:00): all pass — a new diagnostic under `?marca=principal` creates a Franco lead with Franco's consent (lead "Quitanda Teste Final"); the operator's rail shows Usuários/Permissões once; after leaving view-as and signing out, the root login shows "Hub da Reforma" and the access log records "Saiu da conta".

Human round: not run (owed); `/battoni-new-qa-session rnc-4` can make the doc.

## Database

Full Pest on SQLite (in-memory) and on MySQL 8 (`make test-mysql`), 2417 tests, all green on both after the verify fixes. F7b's MySQL fixes: an index name over MySQL's length limit, and `RoleService` duplicate detection (it relied on SQLite's error text). Migrations stay folded into `create_*` until the first deploy.

## Known gaps still open

- A 401 during view-as keeps the cached brand until the next public or firm answer.
- The firm name is empty before the first answer.
- Username and e-mail availability is checked across firms (global identifiers; Auth RULES).
- `firm:offboard` anonymises leads and logins only; partners, portfolio, contracts, NF-e and assistant notes keep their rows (Firm RULES).
- No per-action audit inside view-as, only start and end (Platform RULES, D20).
- A firm's sub-brands are edited only inside a view-as, not from the console (Platform SPA RULES).
- The product name is a placeholder until the brand is chosen; nothing is deployed.

## Suite counts

2419 Pest · 1554 Vitest · 234 Playwright at the last full gate, plus targeted runs after it (the 2419 Pest and 1554 Vitest above, 71 Playwright). Baseline before the feature: 1851 Pest · 1289 Vitest · 180 Playwright.

## Cost

Cost: not measured.

## Decided while you were away

- W1 plan: proposal.html skipped in away mode (spec D27; to reverse: `/battoni-new-proposal rnc-4 final`).
- W2 plan: the owner's phases are split into 17 builder phases with his labels kept (spec D28); his
  "F4b logo + view-as" is F4c/F4d because the console itself needed F4a (API) + F4b (SPA) (to reverse: n/a).
- W3 plan: human QA round off; Chrome rounds by role only (plan.md → QA; to reverse: `/battoni-new-qa-session rnc-4`).
- W4 F1a: AM4's "an unlisted origin returns 401" cannot hold — the API never runs Sanctum's
  stateful middleware (the api group starts the session; guard `web`), so the stateful list gates
  nothing. Not the "wildcard fails" stop: the list carries `*.localhost:5173` and the positive half
  holds (login on `franco.localhost:5173` then `auth/me` 200). `StatefulHostTest` asserts instead that
  CORS never grants an unlisted origin. To reverse: put `EnsureFrontendRequestsAreStateful` in the
  api group and give every test an Origin.
- W5 F1a: `UserFactory` defaults `firm_id` to the default firm (creating it) — AM1 + AM2 broke 105
  existing tests whose users had no firm; the alternative (a global `hub` row in every test) moved
  Franco's tests to the platform firm. To reverse: `'firm_id' => null` in the factory and give each
  test an explicit firm.
- W6 F1a: registration closed by a 404 middleware on routes that stay registered, not by not
  registering them (spec C1). To reverse: conditional `Route::post`.
- W7 F1a: QA login-as reads the firm from `X-Firm`, else the Host — a browser navigation sends no
  header (spec C2). To reverse: header only.
- W8 F1a: `POST auth/users` stamps the current firm (spec C3), pulled forward from F5a. To reverse: n/a.
- W9 F1a: a firm-less signed-in person sending ANY `X-Firm` gets 403 `firms.mismatch` (R5's "never
  falls through to the header", read with AM1). To reverse: ignore the header for a firm-less session.
- W10 F1b: funnel events on a firm host go by keepalive `fetch` with `X-Firm`, not the beacon (no
  headers on a beacon; spec C4). To reverse: beacon everywhere plus a firm field in the body.
- W11 F1b: the firm-not-found page is swapped in by `TheRouteGuard` (no route, the address stays), and
  the route renders while the firm answer is pending — a missing firm then replaces it. To reverse:
  hold the slot until `public/firm` answers (one round-trip on every hard navigation).
- W12 F1b: AM3's live check ran as HTTP calls through Vite's proxy with a cookie jar per host, not in
  Chrome (Chrome rounds are verify's, plan.md → QA); API on 8001 (Pitfalls). To reverse: n/a.
- W13 F1b: `seedAuthSession` answers `public/firm` with Franco by default — 8 back-office e2e tests
  that count console errors went red on the refused boot read. To reverse: mock it in each spec.
- W14 F2a: Franco's consent v1 is its rnc-1 sentence with `{escritorio}` where "Franco" was, filled
  with the full name — the main brand now reads "Autorizo a Franco Contabilidade…", Express/Prime
  unchanged (spec C5). A literal sentence would drop the sub-brand's name. To reverse: fill the main
  brand with `short_name`, or seed the literal sentence.
- W15 F2a: queued mails carry a `MailBrand` value object in their DTO, not a firm id resolved at
  render with `withoutGlobalScope` (plan text) — the values-not-models pattern AM6 already set; the
  worker resolves nothing. To reverse: carry `firmId` and resolve it in the composer.
- W16 F2a: e-mail links (report, briefing, footer) go to the firm's own host `<slug>.<root>` (spec
  C6) — a root link opened the platform firm, where the lead is absent. To reverse:
  `config('rnc.frontend_url')` in `MailBrand::siteUrlOf`.
- W17 F2a: Franco's `tagline` seeded null (the site keeps its own kicker and footer line, which one
  `tagline` would replace both of); its `proof` is the landing's four points, identical on screen. To
  reverse: a `tagline` in `FirmSeeder`.
- W18 F2a: under a sub-brand `logo_url` is null and the e-mail shows the initial tile, not the firm's
  logo — the brand has no logo and the firm's would contradict its name. To reverse: drop the
  `! $brand` guard in `PublicFirmResource` and `MailBrand::fromFirm`.
- W19 F2a: a firm with no consent version gets v1 from the platform default lazily on first need, as
  a safety net beside the seeders and `firm:create` (F3b1). To reverse: answer without consent words
  (or 409) until a version exists.
- W20 F2b: the host firm's read is its own composable (`useFirmBrand`, no `X-Brand`), and
  `usePublicFirm` reuses its answer on the main brand — the plan's single "boot fetch" read under a
  sub-brand would have put Express's colours on the back office. To reverse: one read carrying
  `X-Brand` for both layouts.
- W21 F2b: the "logo text" test is `MNavbarBrand.spec.ts`, not `TheLayout.spec.ts` — the rail's block
  is a new molecule shared by rail and drawer, and `TheLayout` stubs the navbar. To reverse: render
  the name in `TheLayout` itself.
- W22 F2b: off public pages `document.title` is `platform.name` alone; a public page keeps `useSeo`'s
  "page · firm". `index.html` reads "Carregando…" until then. To reverse: "firm · platform" in the
  back office.
- W23 F2b: `brandPalette`'s 400 is lightened until it reads on the dark canvas and panel (spec C7) —
  `celer-button-link-primary` measured 4.29:1 on Franco's runtime row. To reverse: the plain mix and
  a back-office override of the dark link.
- W24 F2c1: identifiers that only spell the old name are kept — `RoleSeeder::CEO_EXTRA_KEYS`,
  `BriefingRepository::CEO_ROLE`/`findActiveCeosOfFirm`, PHP `$ceo` variables, the test helpers'
  `$this->ceo` — AM6 limits the script to the slug, routes and keys, and a blind `ceo` → `gestao` over
  identifiers reaches past them. Prose naming the SLUG in comments and RULES.md moved with it. To
  reverse: rename the identifiers in F2c2.
- W25 F2c1: the old paths `/reinaldo/*` and `/ceo/*` are dropped with no redirect (A13 asks "not
  found"); a bookmark to `/reinaldo` lands on Not Found. To reverse: redirect routes from the old paths.
- W26 F2c2: the host firm's placeholders are `{firmShort}` / `{firmName}`, not `{firm}` (spec C8) —
  `{firm}` was the portal's and letter's own parameter. To reverse: rename those first.
- W27 F2c2: `?marca=principal` or the host firm's slug drops the sub-brand (spec C9). To reverse:
  `BRAND_QUERY.main = 'franco'`.
- W28 F2c2: a firm with no `proof` shows no proof strip (spec C10). To reverse: generic i18n fallback.
- W29 F2c2: the screens that drew `ALogo`'s default name draw `MFirmLogo` (a molecule reading
  `useFirmBrand`, like `MNavbarBrand`) rather than each passing the firm. To reverse: a prop per screen.
- W30 F2c2: `RoleSeeder` keeps `firstOrCreate`, so a database seeded before keeps "CEO"/"Reinaldo" labels
  until `make fresh-seed`; W24's identifiers (`CEO_EXTRA_KEYS`, `$ceo`) still kept. To reverse:
  `updateOrCreate` on name/description.
- W31 F2c2: the footer's credentials line (Franco's certifications) stays static copy — it names no
  tenant; recorded as a Site Known Gap for the console phases. To reverse: a firm field now.
- W32 F3a: `FirmFactory` defaults `modules` to every key (the model's default stays none) — with an
  empty default every existing test of a gated route would have needed its firm's modules set.
  To reverse: drop the factory default and give each test its modules.
- W33 F3a: the plan's `FirmModules::FRANCO_ONLY` is `OPERATOR_ONLY` — the names guard (F2c2) refuses a
  tenant's name in `app/`, and R18 frames `channel` as the operator's to set. To reverse: rename.
- W34 F3a: `auth/me`'s `firm.modules` lists the opt-in keys only (core is always on, never listed); the
  brand summary is flat (`short_name`, `logo_text`, `logo_url`, `brand_primary`, `brand_accent`,
  `is_platform`, like `public/firm`); `view_as` is `{slug, name}` or null. A19 is proven on
  `FirmModulesService` (unit) — no route writes modules before F4a's console. To reverse: list core too.
- W35 F3a: without `portfolio` the briefing keeps its pipeline counts and nulls only the fee ranges;
  `contracts` has no briefing action to drop (spec C11). To reverse: `pipeline: null`.
- W36 F3a: a gated route answers 404 `modules.disabled` (not a bare 404) and the module check runs
  after `auth` and the key. To reverse: put `module:` first, or answer `notFound` with no key.
- W37 F3a: with `brands` off every `X-Brand` is unknown (404 `brands.notFound`; the beacon falls back)
  (spec C12). To reverse: ignore the header.
- W38 F3a: the client timeline (`clients/{id}/events`, under `fiscal.read`) and the lead detail's
  partner matches and referral are gated by their owner — `portfolio` and `partners` — not by the screen
  that calls them; F3c must stop the lead detail asking for matches without `partners`. To reverse:
  `module:fiscal` on the timeline, leave the lead routes ungated.
- W39 F3b1: a command line has no operator, so `firm:create` writes the modules with the NEW MANAGER as
  `FirmModulesService::set`'s actor (`briefing` is not operator-only); the console (F4a) passes its
  operator. To reverse: a system actor, or an operator-only check that skips the CLI.
- W40 F3b1: `--email` is optional and becomes the firm's mailbox too; the manager's first/last name
  come from the username (`helena.acme` → Helena / Acme); a new firm's hours are weekdays 09–18 (the
  platform firm's); the password is 16 letters and digits (`Str::password` without symbols, so it
  copies from a terminal). To reverse: require `--email`, add `--manager-name`, symbols on.
- W41 F3b1: the six default sector pages moved to Content's `Helpers/DefaultSectorPages`, and the
  specialist hours to Booking's `SpecialistService` — the provisioner writes other modules' tables
  only through their services (arcus rule), and `SectorPageSeeder` / `SpecialistSeeder` now use the
  same paths (rows unchanged). Refusal keys: new `firms.slugInvalid` / `slugReserved` / `slugTaken` /
  `nameRequired`, `users.form.usernameRequired` / `emailInvalid` / `emailTaken`, reused
  `users.form.usernameTaken`; the SPA locales get them with F4a's console. To reverse: inline writes.
- W42 F3b2: the demo seeders loop the seeded firms through one trait (`SeedsEachDemoFirm`) and Alvorada
  reuses Franco's invented lists — board names shifted 13, portfolio and contracts from seeds +100
  (320 clients, its landing's "300+"), the same eight "(exemplo)" partners and ten notes — rather than
  lists of its own. To reverse: per-firm constant lists in each seeder.
- W43 F3b2: `gestao.hub` lives in a new local-only `PlatformManagerSeeder`, not `LocalUsersSeeder` (which
  runs under `testing` and would grow `SeedShapeTest`'s exact list, AM7). To reverse: move it there and
  add it to that list.
- W44 F3b2: in Alvorada the knowledge base's people are stand-ins by role — Helena edits, the first team
  member asks, Bruno/Camila review and answer in turn for Franco's four specialists; `equipe.alvorada`
  is "Lívia Fontana". To reverse: name Alvorada's people in `AssistantNoteSeeder`.
- W45 F3b2: F3b's "`make fresh-seed` prints the people" is not added — the seed prints its seeders and
  NfeSeeder's per-firm counts; the people stay in this file's table. To reverse: a summary line at the
  end of `seeders.local.php`.
- W46 F3b2: AM3's moved check ran as HTTP calls through Vite's proxy with a cookie jar per host (as
  W12), API on 8001; Chrome rounds stay verify's. To reverse: n/a.
- W47 F3c: `public/firm` answers the firm's whole opt-in list (`modules`, as `auth/me`), not a
  `has_chat` flag — the public site may need `brands` or `partners` next, and which modules a firm has is
  no secret worth a second shape (spec C13). To reverse: a flag per public need.
- W48 F3c: the sign-in answers (`auth/login`, `auth/phone/verify`) carry `firm` and `platform` like
  `auth/me` (spec C13) — without them the rail after a fresh login had no modules until a reload. To
  reverse: a `fetchMe()` after every sign-in in the SPA.
- W49 F3c: `meta.module` is set in `routes.local.ts` (`ofModule`) for whole route sets, not in each
  module's route files (plan text) — one place shows the split, and a route file stays plain data. To
  reverse: a `meta.module` on each route record.
- W50 F3c: `/gestao` (`/management`) lands on the metrics while `briefing` is off, through
  `meta.moduleFallback` on the redirect routes, instead of not-found (spec C14). To reverse: drop the meta.
- W51 F3c: the rail is filtered in `navItems.local.ts` (LOCAL), not in the synced `TheNavbar`'s
  `isVisibleNavItem`; the portal entry is `partners`', repricing `portfolio`'s. Without `partners` the Radar
  draws no batch column and the Contracts no legal referral and no "enviados ao jurídico" tile (W38's lead
  routing gone too). To reverse: a `module` field on the core `NavItem` and a TheNavbar check.
- W52 F3c: A24's live check ran as HTTP calls on the worktree API (8001) plus a Playwright spec on a mocked
  session for the rail and the not-found screen; Chrome rounds stay verify's (as W12, W46). To reverse: n/a.
- W53 F4a: the console's routes need the key AND the firm-less `operador` (`EnsurePlatformOperator`), and
  `RoleService` refuses `platform.*` to any other role — the plan named only the keys; with the key alone a
  per-user override or a firm-placed `operador` would open the console. To reverse: drop `platform.operator`
  from the routes and `refuseOperatorOnlyKeys`.
- W54 F4a: `POST platform/firms/{id}/manager` creates OR resets by username — the firm's own `gestao` is reset
  (sessions ended, 200), a free username is created there (201), any other account (another firm's, or a member
  here who is not the manager) is 422 `users.form.usernameTaken` and untouched. To reverse: two routes, or
  reset any account of the firm.
- W55 F4a: the default consent must contain `{escritorio}` (422 `platform.consentPlaceholderMissing`, ≤ 1000
  characters) — spec C15. To reverse: drop `namesTheFirm` from `UpdateConsentDefaultRequest`.
- W56 F4a: the live check ran as HTTP calls on the worktree API (8001) with a cookie jar, not in Chrome — no
  screen in this phase; Chrome rounds stay verify's (as W12, W46, W52). To reverse: n/a.
- W57 F4b: one `MAddEditFirmForm` with two modes — create asks only what `POST platform/firms` takes (name,
  slug with its address preview, manager username, optional e-mail) and the look is edited from the row after;
  the new firm joins the list at once while the dialog keeps the one-time password on screen. The plan listed
  look fields on the same form; the API's create takes none. To reverse: a create that chains a `PATCH`.
- W58 F4b: the manager login is a form molecule `MFirmManagerForm` in `MMainDialog` (plan: `MManagerLoginDialog`),
  per celer-07's form contract; the password component `MOneTimePassword` is shared with the create. To reverse:
  rename.
- W59 F4b: the operator's landing is `HomeView` replacing itself with the console when `platform.is_operator`, no
  `firm` AND the key `platform.firms` — the key guards against a redirect loop if the console were refused. To
  reverse: drop the key from the check.
- W60 F4b: the live check ran as HTTP calls on the worktree API (8001) with a cookie jar, plus the A30 Playwright
  spec on a mocked API; Chrome rounds stay verify's (as W56). To reverse: n/a.
- W61 F6a: a `GET public/beta-signups/consent` (`{text, version}`, platform firm only) was added beside the POST —
  F6b's form shows "the API's text" before any lead exists, and the diagnostic's way (`PublicLeadResource`) needs a
  lead. The POST answers `{company, channel}` (an allow-list for the success state). To reverse: drop the GET and
  put the words in `public/firm` for the platform firm.
- W62 F6a: "hub's users with `leads.read`" is read as `TeamNotifier`'s team — active `equipe` and `gestao`, the two
  roles granted `leads.read` — for both bell and e-mail (`TeamNotifier::mailTeam`, one copy per member); a per-user
  `leads.read` override and the firm-less operator are not rung. To reverse: query users by effective permission.
- W63 F6a: a tenant gets 404 from a new `platform.firm` middleware BEFORE the body is validated (a firm host never
  sees a 422 that betrays the route), and `BetaSignupService` refuses again. The throttle runs first, so a tenant's
  calls count too. To reverse: the service's null alone (a tenant would then get 422 on a bad body).
- W64 F6a: the beta lead's timeline gets the existing `contato.capturado` `{consent}` line (no new event type the
  SPA would have to learn); its token is born expired like a portfolio lead's; `source`/`medium` are optional
  from the site (default `direto`), as on the diagnostic. To reverse: a `beta.inscricao` event type.
- W65 F6a: the form's fields are fixed as `company, name, role, email, phone, city, uf, clients_band, message?`
  with four clients bands (`ate_100`, `de_101_a_300`, `de_301_a_1000`, `acima_1000`) and UF from the 27 units; phone
  required (normalised to `55…`), message ≤ 1000. To reverse: change `BetaSignupRequest`/`BetaClientsBand`.
- W66 F6a: the consent stored and shown is the platform firm's current version as R29 says — today the generic
  partner-introduction sentence, which reads oddly for a beta; the operator rewrites it in the console (F4a) and a
  new version applies. Not a hard stop. To reverse: a beta-specific consent text (spec change).
- W67 F6a: the live check ran as HTTP calls on the worktree API (8001), no screen in this phase; Chrome rounds stay
  verify's (as W56). To reverse: n/a.
- W68 F6b: the `/` route picks its view from the host firm's `is_platform` (the boot read) in a lazy loader
  (`loadHomeView`), instead of the plan's "picked by the public layout"; the layout follows the same flag for its nav, CTA
  and footer (`useProductSite`). A firm that could not be read gets the firm landing (an outage must not turn a firm's
  site into the product's). To reverse: one view at `/` switching inside `ThePublicLayout`.
- W69 F6b: R28's "the diagnostic never shows at the root" is a `beforeEnter` (`firmSiteOnly`) on `/diagnostico` and on
  `/reforma/:slug` (a firm's sector pages), landing on `/`; `/relatorio/:token` stays open (it is reached by a token in an
  e-mail). To reverse: drop the `beforeEnter`s.
- W70 F6b: the landing gained an `OProductUrgency` organism (three dated facts, the law, the day checked, the CBS's
  requested delay as news) beside the plan's five; the module menu leaves out `channel` (one network's, operator-only);
  the demo link opens in a new tab. To reverse: fold the facts into the hero; add `channel` to `PRODUCT_OPT_IN_MODULES`.
- W71 F6b: W66 fixed — `PlatformFirmSeeder` writes hub's consent v2 = `BETA_CONSENT` ("Autorizo a equipe do {escritorio}
  a entrar em contato comigo e com o meu escritório … sobre o programa beta … conforme a LGPD"), only while hub is still at
  version 1, so a re-seed never stacks a version on the operator's own words; the platform default (what new firms copy)
  is untouched. To reverse: drop the block; the operator writes the words in the console.
- W72 F6b: on a 422 the beta form shows its own per-field sentence for each field the API names, never the API's message
  (the API answers in its own locale and prose); a 429 says to wait a minute; other failures say to try again. To reverse:
  show `errors.<field>[0]` through `translateError`.
- W73 F6b: the live check ran as HTTP calls on the worktree API (8001) with cookie jars — consent v2, signup 201, the lead
  on `gestao.hub`'s board with channel `beta`, not on `reinaldo`'s; `helena.alvorada`'s login hit the login throttle (429)
  after the run's earlier logins, so alvorada's board was not read live (firm scoping is Pest-proven since F1a). The
  Chrome rounds (QA round 1) stay verify's (as W56). To reverse: n/a.
- W74 F6b: `e2e/product/landing.spec.ts` was written after the components, so it was not seen red before the code; its
  contrast sweep was proven by a mutation instead (hero lede in `text-muted` → 1.21:1, red). The Vitest and Pest files
  were red first. To reverse: n/a.
- W75 F5a: the credentials line (W31) is a nullable `firms.credentials` string, answered by `public/firm` and edited by the manager
  in `PATCH firm/settings` (not the operator's look form); Franco's line comes from `FirmSeeder::CREDENTIALS`, every other firm starts
  with none and its footer drops the "Credenciais" block; the product site shows none. The line is the firm's own words in one
  language — the English site prints it as written (spec C16). To reverse: a look field in the console, or keep a static fallback.
- W76 F5a: a firm member can never give `operador` or `parceiro`, even holding every key of the role (`Rules\TeamRole`, 422
  `users.form.roleNotAssignable`), on create AND update — AM2 named only `operador`; a partner login is the partner screen's, made
  with its partner. Only the firm-less operator passes. To reverse: drop `TeamRole` and rely on `AssignableRole`'s key cap.
- W77 F5a: the manager gets `users.read|create|update|archive|reset_password` but NOT `users.delete` (deactivate is R31's word) and
  not `users.search` (no route uses it). To reverse: add the keys to `RoleSeeder::GESTAO_FIRM_KEYS`.
- W78 F5a: "a newly flagged specialist starts on the firm's hours" — flagging (create or `PATCH is_specialist: true`) makes the row
  through `SpecialistService::startOnFirmHours`; a person who already had a row keeps its hours. Switching the flag off keeps the row
  and hides the person from the agenda and the hours list (bookable = flagged), so its hours and past meetings survive (spec C17).
  A `GET specialists` list was added beside the plan's `GET/PUT specialists/{id}/hours` (the hours screen needs the people). To
  reverse: delete the row on unflag; drop the list.
- W79 F5a: a new consent text must hold `{escritorio}` (422 `leads.consentPlaceholderMissing`, ≤ 1000) like the platform default
  (C15); the history answers the stored words unfilled (the SPA previews them) with `author {id, name}` or null. To reverse: accept
  any non-empty text.
- W80 F5a: the live check ran as HTTP calls on the worktree API (8001) with a cookie jar — no screen in this phase; Chrome rounds stay
  verify's (as W56). To reverse: n/a.
- W81 F5b: a team login's password (new or reset) is drawn in the browser — 16 letters and digits without look-alikes from
  `crypto.getRandomValues` (`useOneTimePassword`) — sent once and shown once with `MOneTimePassword`; `auth/users` takes the password
  from the caller and F5a added no generate route. The reset sends the password alone. To reverse: a server-side generate route that
  answers the password, as the console's manager login does.
- W82 F5b: the live check ran as HTTP calls on the worktree API (8001) with a cookie jar, plus the A40 Playwright spec on a mocked API;
  the Chrome rounds (QA round 3) stay verify's (as W56). The plan's "a new diagnostic stores v2, an old lead keeps v1" is F5a's Pest
  (A38), not re-run live. To reverse: n/a.
- W83 F5b: the four settings screens are the last children of "Gestão" in the rail, all behind `firm.settings` (the team's route asks
  `users.read` like its API; inside it each `users.*` key hides its own button); the role is two radio choices (Equipe, Gestão) read from
  `auth/roles` by slug, not a select; the consent form also refuses saving the current version's exact words. To reverse: a separate
  "Escritório" group; a select; allow an identical version.
- W84 F4c: view-as and the logo ride `platform.firms` (no new key) behind the same two locks as the console (`platform.operator`) —
  the plan named no key, and the operator-only person check is what keeps them the operator's. To reverse: a `platform.view_as` key
  in Auth's permission groups, refused to other roles by `RoleService`.
- W85 F4c: `DELETE platform/view-as` with nothing active answers 200 `data: null` (idempotent), not 404 — a second "Sair", or a view-as
  a sign-in elsewhere already closed, is not an error for the banner. Nested start is 409 `platform.viewAsActive`, the platform firm 422
  `platform.viewAsPlatformFirm`, each with a `code`. To reverse: 404 on an empty stop.
- W86 F4c: the audit row also keeps the IP (`ip_address`, the request's direct peer), beyond the plan's columns, as the brief asked
  (spec C18); behind the deploy's proxy it needs trusted proxies (Platform Known Gap, F7). To reverse: drop the column.
- W87 F4c: "close stale on sign-in" is a listener on Laravel's `Login` event (every door: password, phone code, QA login-as), not a call
  in `AuthService`, and it closes ALL of the person's open rows — so signing in from another browser ends a view-as left open there.
  To reverse: call `ViewAsService::closeLeftOpen` from each sign-in service and close only rows older than the session lifetime.
- W88 F4c: the session holds the audit row's id, not the firm's, and `ViewAsFirm` (Firm) delegates to Platform's `ViewAsService::current`
  (memoised per request) — closing the row ends the view-as wherever the session lives, and a leaked key points at a row that is not
  the holder's. The logo writer is Firm's `FirmLogoService` (Platform writes no firm). To reverse: store the firm id in the session.
- W89 F4d: the F4c gap "proxy `/storage` or show the 8000 URL" took the proxy: Vite proxies `/storage` beside `/api` to the same target
  (local, test mode, preview) and the SPA rewrites `logo_url` to a path on its own host (`toStorageAssetPath`), so the logo loads on every
  firm host and in production through the vhost (AM10). The API keeps answering `APP_URL/storage/...`. To reverse: drop the rewrite and
  show the API's URL as it comes.
- W90 F4d: the logo is saved on its own button ("Enviar logo") inside the look dialog, not with the look's "Salvar" — the upload is a
  multipart call to its own route and its answer replaces the row without closing the dialog or losing unsaved look fields. A "Remover
  logo" uses F4c's `DELETE`. The SPA refuses non-PNG/JPEG/WebP and > 512 KB before sending; the 1024 px sides stay the API's. To reverse:
  send the file with "Salvar".
- W91 F4d: the banner is mounted by `TheLocalOverlays.local.vue` (TheLayout's LOCAL slot) and placed in flow at the top of the content
  column (`order-first`), not `position: fixed` — it never covers a row and needs no sync edit of `TheLayout`. "Acessar como suporte" lands
  on Home (which no longer bounces the operator to the console while `view_as` is set); "Sair" returns to the console; both read `auth/me`
  and reload the host brand, so the back office wears the viewed firm's palette and logo. To reverse: a fixed bar and stay on the console.
- W92 F4d: the view-as log screen is `/plataforma/acessos` (+ `/platform/view-as-log`) on `platform.firms` (the API's key, W84), with a rail
  entry "Acessos de suporte" under "Plataforma", 25 a page. To reverse: a tab on the firms screen.
- W93 F4d: during a view-as the rail offers only the viewed firm's core screens — `auth/me` keeps `firm` null for the operator and `view_as`
  carries slug and name only, so `hasModule` answers none. Left as a Known Gap in app Platform `RULES.md` (the fix is an API field,
  `view_as.modules`, outside an SPA phase). To reverse: add `modules` to `view_as` in Auth's `UserResource` and read it in `hasModule`.
- W94 F4d: the live check ran in headless Chromium (Playwright, a scratch script) against the worktree API on 8001 behind Vite on 5173,
  signing in by QA login-as with the session hint set; the Chrome rounds (QA round 5) stay verify's (as W56). To reverse: n/a.
- W95 F7: MySQL 8 not run (R36) — `mysql -uroot` without a password is refused (`ERROR 1045`, as rnc-1's W1) and no password was tried;
  the full Pest ran on SQLite in memory (2354). `docs/deploy/runbook.md` → "Database" gives the owner the exact commands (create
  `rnc_test` + `rnc`, `DB_*` in the shell over phpunit.xml's unforced `<env>`, `make fresh-seed` with `.env` on MySQL). To reverse: run them
  and write the count there. **Retired by F7b (W112):** it held only because the password was unknown; the owner gave it and the suite
  and seed ran on MySQL 8.
- W96 F7: F4d's W93 closed — `auth/me`'s `platform.view_as` carries the viewed firm's opt-in `modules` (`FirmModules::enabled`), and the
  User store's `hasModule` reads them while a view-as is set (else the person's firm's); `firm` stays null for the operator. The app
  Platform Known Gap is retired with its reason. To reverse: drop the field and the store's first branch.
- W97 F7: `GET api/health` answers in the `ApiResponse` envelope — `{data: {status: ok, db: ok}}`, 503 `{data: {status: down, db: down}}`
  — and runs without `StartSession`, `EnsureAccountActive` and `ResolveCurrentFirm` (each reads the database in production; the probe
  must say "down", not 500). The controller does its `select 1` with no service/repository. To reverse: a bare JSON body.
- W98 F7: trusted proxies come from `config/trustedproxy.php` → `env('TRUSTED_PROXIES')` (Laravel's global `TrustProxies` reads that key),
  unset = none trusted; not `$middleware->trustProxies(at: env(...))` in `bootstrap/app.php`, since `env()` outside config is null under
  `config:cache`. To reverse: set the list in `bootstrap/app.php`.
- W99 F7: the runbook's web server is Nginx, one server block for `<root>` and `*.<root>`: SPA `dist/` as root with a history fallback,
  `^~ /api/` to PHP-FPM with the API's `index.php`, `^~ /storage/` by `alias` to `storage/app/public/` (AM10); the production domain,
  the mail domain and the host stay `<root>`/owner's choice ("Open before go-live"). To reverse: n/a (a document).
- W100 F7: A46's sweep check finds rnc-4's routes by the locks rnc-4 introduced (`permission:platform.firms`, `permission:platform.consent`,
  `permission:firm.settings`, `platform.firm`) and fails when one is missing from `Phase4AccessTest`'s list; every listed route must be
  registered and classified. `GET health` is listed (its proof is `HealthTest`). To reverse: a hand-kept list only.
- W101 F9a: a lead's export and anonymisation sit behind `leads.update` AND `firm.settings` (two `permission:` middlewares) — the
  manager's existing key, no new `leads.privacy` key; the team holds the first only and gets 403. To reverse: a new key in
  `permission-groups.local.php` granted to `gestao`.
- W102 F9a: `firm:offboard` exports (firm, logins without password, every lead with consents and timeline) to
  `offboarding/<slug>-<time>.json` on the private `local` disk, then anonymises every lead and writes `firms.offboarded_at` in one
  transaction; `--confirm` required; the platform firm, an unknown slug and an already closed firm refused. Other modules' rows
  (partners, clients, referrals, NF-e, notes) are not wiped — Firm Known Gap. Spec C20. To reverse: close only, no anonymisation.
- W103 F9a: anonymise wipes, beyond A48's name/e-mail/phone/CNPJ, the company, `visitor_uuid`, `lost_reason`, the report link and
  the team's free text on the timeline, and replaces the diagnostic token by an expired one; idempotent. Spec C19. To reverse: A48's four only.
- W104 F9a: `GET public/privacy` answers stable keys (`collected`, `retention`, `sharing`) and names (controller = the firm,
  operator = `platform.name`, requests = the firm's mailbox and phone) — the notice's prose stays in F9b's template. To reverse:
  prose from the API.
- W105 F9a: the live check ran on the API alone (8001, Python urllib with a cookie jar); no SPA change, so no browser. To reverse: n/a.
- W106 F9b: `/privacidade` answers at the root too (no `firmSiteOnly`), and the footer links to it there: the beta form keeps a firm's
  contact under the platform's consent, so the platform is a controller with a notice of its own; with `is_platform` the page names it
  controller and drops the operator line. Spec C21. To reverse: `beforeEnter: firmSiteOnly` and hide the footer link on the product site.
- W107 F9b: the diagnostic's privacy link sits under the consent, outside its `<label>` (following it never ticks the box), and opens in
  a new tab (`target="_blank"`): the diagnostic's token lives only in the page, so leaving it would start the visitor over. To reverse:
  same-tab link.
- W108 F9b: "Anonimizar" asks in a `ConfirmPopup` (celer-07: a yes/no destructive action is a popup, not an `MMainDialog`) whose message
  says it cannot be undone; after it, "Anonimizar" is gone, "Exportar dados" stays (the export of what is left), and "Dados anonimizados
  em …" shows to every reader of the lead, not only the manager. The panel is "Dados do lead (LGPD)" in the detail's side column. To
  reverse: an `MMainDialog` confirmation; the notice for managers only.
- W109 F9b: no live check against the real API and no browser on 5173: the two endpoints were proven live in F9a (W105) and the SPA side by
  the two new e2e files with the API mocked; the Chrome rounds stay verify's (as W56, W94). To reverse: run QA round 6 now.
- W110 F9b: the API's 403 `firms.offboarded` gets its sentence (`firms.offboarded` in both locales) and no handler of its own — the API has
  already invalidated the session, so the next call is a 401 and the existing handler takes the person to the login screen. To reverse:
  treat it like `firms.mismatch` in `errorHandler`.
- W111 F9b: the export downloads as `lead-<id>-dados.json`, the API's `data` as it came, indented (2 spaces), built in the browser from the
  JSON answer (no file endpoint). To reverse: a `Content-Disposition` download from the API.
- W112 F7b: MySQL 8 proven (retires W95) — schema + local seed clean, full Pest 2399 green on MySQL as on SQLite. JSON key order is
  treated as no contract: MySQL's re-ordering is absorbed in the tests (`toBeIgnoringKeyOrder`), not by turning JSON columns into
  text; `client_contracts`' unique is named `client_contracts_period_unique`; `make test-mysql` lives in `Makefile.local` (the sync
  never touches it) and reads the password from the environment. No MySQL-vs-SQLite difference left open, so no Known Gap. To
  reverse: n/a (a proof); JSON columns to `text` if key order ever becomes part of a contract.
- W113 verify P2-A3: a view-as start on an offboarded firm is 422 `platform.viewAsOffboarded` (code `view_as_offboarded`), like the
  platform firm's 422 — the console lists the firm, so "not found" would lie; an open view-as whose firm is offboarded mid-visit falls
  back to the platform firm. The SPA needs the new key in `PLATFORM_ERROR_KEYS` and both locales (app builder). Spec C23. To reverse:
  404 `firms.notFound`.
- W114 verify P2-A4: `auth/login` is resolved as a visitor's request over any live session (host's `X-Firm`, else the default firm),
  and the login ends the session's view-as as `logout` BEFORE checking the password — a failed sign-in still ends it, since the person
  chose to replace the session. To reverse: end it only after a successful `authenticate`.
- W115 verify P1-A2: an offboarded firm's logins are anonymised in place, never deleted (timeline authors and audit rows still point at
  them): name "Pessoa removida", username `desligado.<id>`, e-mail/phone/CPF/birth date null, a random 64-character password,
  inactive, sessions ended. Spec C22. To reverse: deactivate only (C20 as it was).
- W116 verify P2-C2: the one demo guard allows `local` AND `testing` (the Pest suite seeds Franco's demo data); `BrandSeeder` and
  `ChannelSeeder` joined it so the runbook's "nothing invented outside local" is true for every demo seeder. To reverse: per-seeder
  `production` checks.
- W117 verify PE1: role writes need `platform.operator` on top of `permissions.update`. No spec change — `RoleSeeder` already keeps the
  roles screen (`permissions.*`) the operator's; the route now enforces it. Tests write roles as `platformOperatorWithPermissions`.
  To reverse: drop the alias from `$rolesWrite`.
- W118 verify (SPA): the API keeps role writes to the operator (W117), but the rail's operator group opens on `users.read`, which the
  manager holds, and a key can be granted to a firm role. The roles routes now declare `meta.role: 'operador'` (`attachAuthGuard` checks
  it with `meta.permission`) and the rail's link carries `role: 'operador'`. The synced settings block's "Perfis" link still gates on the
  key alone (a Known Gap in `RolesAndPermissions/RULES.md`: a role slug in a synced file). No spec change — D25 already keeps roles off
  the manager. To reverse: drop `role` from the two route metas and the nav item.
- W119 verify P1-S1: found while testing the escape — an EMPTY firm name prints its linked key (`firm.short`) because vue-i18n's
  `linked()` treats an empty result as unresolved; only before the firm first answers, with no stored answer. Not fixed (an invisible
  placeholder would leak into titles and copied text); Known Gap in `locales/RULES.md`. To reverse: n/a.
- W120 verify P2-S2: the post-date twins (`cbsKey`, `<key>Started`) also cover the FIRM landing's title and description, which said the
  same "começa a ser cobrada em 01/01/2027" as the product landing lines the finding named. "Até a lei mudar, vale 01/01/2027" stays (still
  true). To reverse: drop the `cbsKey` calls in `LandingView`.
- W121 Chrome QA 1.11: the QA login-as lands on the firm's own site (`MailBrand::siteUrlOf`) when the address named a firm (firm host or
  `X-Firm`), the root otherwise — built from config, never the Host header echoed. Every other `rnc.frontend_url` read already went through
  `siteUrlOf` per firm or is the platform's root by design. To reverse: redirect to `config('rnc.frontend_url')` again.
- W122 Chrome QA 1.10: a `beta` lead's detail shows the beta form's rows (role, city/UF, clients band with the Site's band labels, message)
  instead of the empty diagnostic rows, and its consent summary is channel-aware ("contatado sobre o beta"); the stored text and version are
  shown as given. No API change — `LeadDetailResource` already sent the whole `profile`. No C# — spec behaviour (R29, D29) unchanged; this
  is the detail showing what was stored. To reverse: drop the `LEAD_CHANNEL.BETA` branches in `LeadView`.
- W123 Chrome QA 4.11/4.12: not reproduced on full page loads (headless Chromium on franco.localhost:5173, the running stack):
  `?marca=principal` clears `app.rnc:brand` and every later public call goes without `X-Brand`. 4.11 as scripted opens plain
  `/diagnostico` after 4.10's `?marca=prime`, which keeps Prime for the tab by design (rnc-3 R2). Pinned by `publicBrand.spec` and
  `brands.spec` (red with the main-brand clear removed). The cached FIRM brand was the real hole (5.21): kept as `{ firm, host }`,
  dropped by `reload()`, `forget()` on logout, "Sair" reloads even when `auth/me` fails. Not done: the 401 path in `errorHandler`
  (an import cycle `@Providers` → `@Composables`); the next `public/firm` answer replaces it. No C#.
- W124 Chrome QA 5.2: the Operador workspace, its landing (`/operador`) and the bootstrap Users screen ask `role: 'operador'` besides
  `users.read` (the manager holds it since F5a for /gestao/equipe); TheNavbar's footer drops its core Usuários/Permissões (the
  operator saw them twice). Personalização stays everyone's (browser preferences). Franco's manager keeps "Canal RNC" under Gestão.
  `GET auth/users` still answers a manager 200 — the screen, not the data, is the operator's. No C# (A26's operator rail unchanged;
  the manager never had the group in the spec). To reverse: drop `role` from `WORKSPACES`/the two routes and restore the footer entries.
- W125 Chrome QA 3.4 (first "Salvar" on /gestao/escritorio without a toast): not reproduced — a first save and a second each toast once
  (`FirmContactView` spec, red with the first toast skipped); the screen keeps no dirty state. Likely the driver read the page after the
  3.5 s toast had gone, or a Chrome `type="time"` field not yet committed (the inline "horário" error, no toast). Left as is.
- W126 Chrome QA 5.21, second round (rail's account "Sair" during a view-as → root's login in Alvorada's brand, sessionStorage
  empty): reproduced headless on the live stack — after `POST auth/logout` the `GET public/firm` that `forget()` sends was
  `net::ERR_ABORTED`. `completeLogout` pushes the login and forgets in the same tick; the route guard (`attachAuthGuard`) aborts every
  request in flight on that navigation, a cancelled `API` call never settles, so the firm stayed null and the translations kept
  Alvorada's `{firmShort}` / `{firmName}`. Picked: the brand read outlives navigation (`outlivesNavigation` on `ApiParams`, no global
  signal) — the brand is the page's, not a screen's, and every `forget()` / `reload()` / `load()` caller is then safe whatever it
  navigates around it. Rejected: reordering (`push().then(forget)`) — fixes one caller and leaves the trap; a full reload of `/entrar`
  — drops the "Até logo" toast and the SPA's own reset. The 401 path (session expired mid view-as) still does not call `forget()`
  (bcd247c's Known Gap). Reverse: drop the flag from `useFirmBrand`.
- W127 Chrome QA 4.11/4.12 (lead 86 "Franco Prime" with Prime's consent after a full load of `/diagnostico?marca=principal`):
  reproduced headless on the live stack. The SPA was right — the second start left without `X-Brand`, title "Franco Contabilidade"
  — and the API answered the SAME token with Prime's consent: `LeadService::startLead` reopens the visitor's open `visitante`
  (same `rnc:visitor` uuid in localStorage, no stored diagnostic token) and kept the brand it was born under. The hypothesis of a
  resumed client-side token was wrong; the resume is server-side, by visitor. Picked: reopen only under the same brand, else a new
  lead of the current one (C24) — keeps rnc-3 R4's "brand written once" and the per-brand start counts honest. Rejected: re-brand
  the reopened lead (rewrites where a counted Prime start came from); re-apply the lead's brand to the page (overrides the visitor's
  explicit `?marca=`). Cost: an empty Prime `visitante` stays on the board (QA-only path). Also: `ResolveCurrentBrand` sets the main
  brand on a request without the header — `CurrentBrand` is `scoped` and kept the previous request's brand inside one test.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
