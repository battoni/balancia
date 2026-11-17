# Balancia

Plataforma white-label para escritórios de contabilidade atravessarem a Reforma Tributária (CBS a partir de 01/01/2027) e crescerem com ela. Cada escritório recebe, no próprio subdomínio e com a própria marca, um site público com diagnóstico de impacto para empresários, um back office para trabalhar os leads e uma rede de parceiros. A Balancia é o produto da Battoni Dev; os escritórios são inquilinos dela.

## De onde veio

O projeto nasceu como o "Hub da Reforma" da Franco Contabilidade (rnc-1 a rnc-3, por isso a pasta local e os IDs antigos ainda se chamam `rnc`). Em 13/11/2026 virou uma plataforma vendida por assinatura a vários escritórios (rnc-4), e em 16/11/2026 ganhou o nome e a marca Balancia. A Franco continua como um inquilino, ao lado de um escritório fictício de demonstração, o Alvorada.

## Como funciona

- **Um escritório por subdomínio.** `franco.<domínio>`, `alvorada.<domínio>`: cada um com site, back office e portal de parceiros na marca dele. Localmente é `<slug>.localhost:5173`, nunca `127.0.0.1`.
- **A raiz é a própria Balancia.** O domínio raiz serve o site do produto, com o cadastro do beta; quem se cadastra vira lead no pipeline da própria plataforma (a "firma zero", slug `balancia`).
- **Papéis.** `operador` (a Battoni Dev: opera a plataforma, sem escritório, e só entra num escritório pelo "ver como", auditado e com faixa na tela), `gestao` (o gestor do escritório: equipe, marca, consentimento, métricas) e `equipe` (trabalha os leads; `is_specialist` marca o especialista que atende as reuniões). Parceiros entram pelo portal deles.
- **O que o empresário vê.** Conteúdo sobre a Reforma, o diagnóstico de impacto, o agendamento de uma conversa e o consentimento de LGPD, cujo texto o gestor edita e versiona.
- **Multiempresa desde o início.** Toda tabela de negócio tem `firm_id`; um escritório novo é uma linha, não um deploy.

## O repositório

| Pasta | O que é |
| --- | --- |
| [`api.balancia/`](./api.balancia/) | API em Laravel (PHP 8.4): escritórios, autenticação e papéis, conteúdo, diagnóstico, agenda, pipeline, parceiros, métricas, LGPD. Testes em Pest |
| [`app.balancia/`](./app.balancia/) | SPA em Vue 3: o site público (`ThePublicLayout`) e o back office (`TheLayout`), com o tema do escritório aplicado em tempo de execução. Testes em Vitest e Playwright |
| [`brand/`](./brand/) | A marca da Balancia: comece por [`brand/SYSTEM.md`](./brand/SYSTEM.md); a versão renderizada é `brand/design-system/index.html` |
| [`specs/`](./specs/) | Uma pasta por feature (`spec.md`, `plan.md`, `state.md`, roteiro de QA). A mais recente é [`specs/rnc-4-white-label-platform/`](./specs/rnc-4-white-label-platform/) |
| [`docs/deploy/`](./docs/deploy/) | Como a demonstração é publicada (`docs/deploy/demo/README.md`) e o runbook |
| [`codelumen/`](./codelumen/) | Manual de convenções de código (VitePress) |
| `cortex/`, `.claude/`, `scripts/` | Ferramentas de IA e o fluxo de features (`/battoni-*`); ver [`CLAUDE.md`](./CLAUDE.md) |

## Rodar localmente

Requisitos: PHP 8.3+ (8.4 recomendado), Composer, Node 24 (`source ~/.nvm/nvm.sh && nvm use 24`; no Node 20 o Vitest quebra com `ERR_REQUIRE_ESM`).

```bash
make fresh-seed   # recria o banco SQLite com a plataforma, a Franco, o Alvorada e as pessoas
make serve-api    # API em http://localhost:8000
make serve-app    # SPA em http://localhost:5173
```

Depois abra `http://localhost:5173` (site da Balancia), `http://franco.localhost:5173` ou `http://alvorada.localhost:5173`. As pessoas criadas pelos seeders e a senha estão no `state.md` da feature atual e no roteiro de QA. Os e-mails vão para `api.balancia/storage/logs/laravel.log`.

Testes: `make check-api` e `make check-app`.

## Demonstração online

https://balancia.battoni.dev (plataforma), https://franco.balancia.battoni.dev e https://alvorada.balancia.battoni.dev. Só dados inventados; o banco é recriado a cada `make deploy-demo`.

## Licença

Projeto privado. Todos os direitos reservados.
