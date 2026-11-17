# Cortex — AI Brain

Cortex is the **knowledge layer** of balancia's AI infrastructure. It holds the history of decisions, reusable prompts, and documentation about the overall AI setup.

Rules are not stored here — they live at the monorepo root and activate automatically based on file path.

---

## Getting started on a new project

```text
1. Clone balancia
2. Delete the modules you won't use
3. Rename folders to match your project (e.g. api.balancia → api.myproject)
4. Run /battoni-setup-project — maps all rules and commands to your folder names
5. Run /battoni-start-session — loads the right rules before you begin
```

---

## Available commands

Commands work in both **Claude Code** (as `/command-name`) and **Cursor** (as `/command-name` in chat).

| Command | What it does |
| --- | --- |
| `/battoni-setup-project` | One-time setup after cloning — maps folder names, updates globs, removes unused modules |
| `/battoni-start-session` | Loads the right rules for the projects you're working on before planning begins |
| `/battoni-explain-balancia` | Gives a new developer a full end-to-end overview of the AI setup and how to use it |
| `/battoni-pre-commit` | Runs lint, format, locales, tests, and the convention reviews — commits nothing |
| `/battoni-commit` | Presents a bottom-up conventional-commit plan and commits it (no AI signature) |
| `/battoni-create-pr` | Generates a PR title and description for the current branch for review (does not save) |
| `/battoni-publish-pr` | Pushes and opens a draft PR against `development`, requests a reviewer, sets the Vercel preview |
| `/battoni-review-vue-conventions` | Reviews all app.balancia Vue/TS changes on the current branch and fixes violations |
| `/battoni-review-arcus-code` | Reviews all api.balancia PHP changes on the current branch and fixes violations |
| `/battoni-review-design-conventions` | Reviews app.balancia changes for design-system violations (runs in plan mode) |
| `/battoni-generate-api-rules` | Generates a `RULES.md` for a unit in `api.balancia/` |
| `/battoni-generate-component-rules` | Generates a `RULES.md` for a folder in `app.balancia/src/` |
| `/battoni-rules-sync` | Checks that each changed unit's `RULES.md` still describes its code, and drives the version + `CHANGELOG.md` bump |
| `/battoni-grill-me` | Grills you on a task, scaled to its difficulty, until the plan is validated |
| `/battoni-improve` | Turns an AI mistake into a rule change and opens a PR after you approve the draft |
| `/battoni-agent-handoff` | Writes an AI-to-AI handoff document so another agent can resume with no prior context |

---

## Rules

Rules activate automatically when you open or edit a matching file — no manual loading needed during implementation. Use `/battoni-start-session` when planning without files open.

| Rule file | Activates for | Tool |
| --- | --- | --- |
| `arcus-api-architecture` | Any file in `api.balancia/**` | Claude + Cursor |
| `celer-01-vue-checklist` | `app.balancia/**/*.vue`, `app.balancia/**/*.ts` | Claude + Cursor |
| `celer-02-vue-imports` | `app.balancia/**/*.vue`, `app.balancia/**/*.ts` | Claude + Cursor |
| `celer-03-vue-script` | `app.balancia/**/*.vue`, `app.balancia/**/*.ts` | Claude + Cursor |
| `celer-04-vue-template` | `app.balancia/**/*.vue` | Claude + Cursor |
| `celer-05-module-conventions` | `app.balancia/**/*.vue`, `app.balancia/**/*.ts` | Claude + Cursor |
| `shared-conventions` | Always | Claude + Cursor |
| `project-context` | Always | Cursor only |

Rules live in `.claude/rules/` (Claude) and `.cursor/rules/` (Cursor). When you add rules for a new module, add both formats.

---

## Playbooks

| File | What it is |
| --- | --- |
| `playbooks/OVERNIGHT-BUILD.md` | An unattended multi-hour build with parallel agents: contract, plan file, foundation before fan-out, conflict rules, browser traps, verification, the morning report |
| `playbooks/OVERNIGHT-KICKOFF.md` | The kit that starts one: terminal prep, the first message with slots to fill, and what to watch from another terminal |
| `playbooks/planning/` | The shapes of the planning documents: product memory, estimate, roadmap, phase spec |

## QA

| File | What it is |
| --- | --- |
| `qa/CHECKLIST-QA.template.md` | The shape of a manual QA checklist: scope cut at the fork commit, a table of cuts, numbered intentional behaviours, fixes to verify with their commit, and the report format |

## Skills (Claude Code only)

Skills are demand-loaded specializations — they load only when the task context requires them, keeping the context window lean.

| Skill | Loads when |
| --- | --- |
| `arcus-laravel-best-practices` | Writing, reviewing, or refactoring any Laravel PHP code in api.balancia |
| `arcus-pest-testing` | Writing or editing any test file in api.balancia |
| `arcus-tailwindcss` | Working with Tailwind classes in api.balancia Blade templates |
| `celer-advanced-patterns` | Building a new module, composable, or complex form in app.balancia |
| `celer-testing` | Writing or editing app.balancia tests |

Skills live in `.claude/skills/`. Each skill has a `SKILL.md` as its entry point.

---

## Agents (Claude Code only)

Agents run in an isolated context window with limited tools. Use them for focused tasks that shouldn't pollute the main conversation.

| Agent | What it does |
| --- | --- |
| `code-reviewer` | Read-only review of a PR or branch — produces a structured violation report, never edits |
| `security-auditor` | Security scan of a feature or file — checks OWASP top 10, auth gaps, exposed secrets, never edits |

Invoke with: *"Use the code-reviewer agent to review this branch"*

---

## Hooks (Claude Code only)

Hooks run automatically — no manual trigger needed.

| Hook | Trigger | What it does |
| --- | --- | --- |
| `post-edit.sh` | After any file edit | Runs Pint on api.balancia PHP files; runs ESLint on app.balancia Vue/TS files |
| `pre-edit-rules.sh` | Before editing a app.balancia file | Injects the folder's `RULES.md` chain (up to `src/`) so local rules win |
| `pre-bash-guard.sh` | Before any Bash command | Blocks dangerous patterns (`rm -rf /`, `git push --force`, etc.) |

---

## Adding or updating a rule

1. Edit the canonical rule in `.claude/rules/`
2. Run `make sync-mirror` to regenerate the `.cursor/rules/` mirror
3. Add an entry to `CHANGELOG.md`
4. Commit both sides

`make sync-mirror-check` runs in `make pre-commit` and as a CI job, so a drifted mirror can never reach `main`.

---

## What lives in Cortex

| File | Purpose |
| --- | --- |
| `CHANGELOG.md` | History of every AI infrastructure decision and change |
| `generate-component-rules.md` | Pointer to the component `RULES.md` prompt — the command `battoni-generate-component-rules` is the only copy |
| `sync/cursor_mirror.py` | Keeps `.cursor/rules` mirrors identical to canonical `.claude` |
| `sync/handoff.py` | Ejects a clean, tooling-free copy for client delivery |

---

## Client handoff

When a balancia-built app is delivered to a client, we hand over a clean,
self-documenting codebase **without** the reusable framework and AI tooling.
`make handoff` (→ `sync/handoff.py`) produces that copy in one step:

```bash
make handoff                               # all app projects → ../balancia-handoff
make handoff PROJECTS="app.balancia" VERIFY=1     # just app.balancia, and prove it builds
make handoff OUT=/path PROJECTS="app.balancia api.balancia" FORCE=1
```

It:

1. **Exports the committed tree** (`git archive HEAD`) into a copy — never touches your working repo, never includes uncommitted or gitignored files.
2. **Strips the tooling** — `.claude/`, `.cursor/`, `cortex/`, `codelumen/`, `plans/`, every `CLAUDE.md`, and the tooling targets/jobs in `Makefile` and `ci.yml` (a dropped project's CI job goes too).
3. **Keeps every `RULES.md`** — they carry no AI-plumbing references, so they stand alone as plain documentation.
4. **Re-inits git** — one `Initial commit`, so the stripped tooling is not recoverable from history.

`--verify` runs the kept projects' build to prove the copy stands alone. The
eject enforces the split technically; the **contract** should still retain
framework IP and license the app.

---

## Design principles

- **Monorepo-always** — balancia is always used as a whole. Modules are never forked standalone. Rules live at root, not inside each module.
- **Single canonical source** — each rule's body lives once in `.claude/rules/`; `.cursor/rules/` is a generated mirror kept identical by `make sync-mirror`.
- **Glob routing** — rules activate automatically by file path. No manual loading during implementation.
- **Planning gap** — `/battoni-start-session` loads the right rules before any files are open. `project-context.mdc` in Cursor does this automatically when you name a project.
