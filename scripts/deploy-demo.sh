#!/usr/bin/env bash
#
# Publish main to the demo server (https://balancia.battoni.dev and its firm hosts).
# `make deploy-demo` from the main checkout. The server half is api.balancia/deploy.sh;
# the server's setup, once, is docs/deploy/demo/README.md.
#
# The SPA is built HERE, not on the server: the droplet has 1 GB of RAM shared with six other
# projects and MySQL, and a Vite build there competes with all of them for it. So the build has
# to come from the very commit the server publishes, which is why this refuses a dirty tree or a
# HEAD that is not origin/main: a dist/ built from local edits would sit on top of an API from
# main, and the mismatch shows up as a screen calling an endpoint that is not there.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

HOST="${DEMO_HOST:-root@server.battoni.dev}"
DIR="${DEMO_DIR:-/var/www/balancia}"
ROOT_DOMAIN="${DEMO_ROOT_DOMAIN:-balancia.battoni.dev}"
OUT="$(mktemp -d)/dist"

echo "==> Checking that this checkout is origin/main, clean"
git fetch --quiet origin main
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "✗ uncommitted changes: the build would not match what the server pulls." >&2
    exit 1
fi
SHA="$(git rev-parse HEAD)"
if [ "${SHA}" != "$(git rev-parse origin/main)" ]; then
    echo "✗ HEAD ${SHA:0:7} is not origin/main — pull or push first." >&2
    exit 1
fi

echo "==> Building the SPA for ${ROOT_DOMAIN}"
# Real environment variables win over app.balancia/.env, so the developer's local values never
# leak into the bundle. The set is the runbook's "Env inventory — SPA".
(
    cd app.balancia
    VITE_API_URL=/api \
    VITE_ROOT_DOMAIN="${ROOT_DOMAIN}" \
    VITE_APP_URL="https://${ROOT_DOMAIN}" \
    VITE_DEMO_FIRM_SLUG=alvorada \
    VITE_ACTIVE_THEME=hub \
    VITE_DEFAULT_LANGUAGE=pt-BR \
    VITE_LOGIN_FLOW=username \
    VITE_DOCS_URL= \
    VITE_SENTRY= \
    VITE_LOCAL_SSL_KEY= \
    VITE_LOCAL_SSL_CERT= \
    npx vite build --mode production --outDir "${OUT}" --emptyOutDir --logLevel warn
)
if grep -rq "localhost:8000" "${OUT}/assets"; then
    echo "✗ the bundle names localhost:8000 — a local value reached the build." >&2
    exit 1
fi

echo "==> Publishing the API (${SHA:0:7}) on ${HOST}"
# The server pulls and rebuilds BEFORE the new dist/ lands, so the window where the new screens
# call the old API is the rsync's few seconds rather than the minute of the seeders.
#
# The tree is moved to the commit HERE, before deploy.sh starts: bash reads a script as it runs,
# so a deploy.sh that reset its own file mid-run would carry on executing the new file's bytes
# from the old file's offset.
ssh -o BatchMode=yes "${HOST}" bash -s -- "${DIR}" "${SHA}" <<'REMOTE'
set -euo pipefail
cd "$1"
git fetch --quiet origin main
git merge-base --is-ancestor "$2" origin/main
git checkout --quiet main
git reset --hard --quiet "$2"
bash api.balancia/deploy.sh
REMOTE

echo "==> Uploading the SPA"
rsync -a --delete "${OUT}/" "${HOST}:${DIR}/app.balancia/dist/"
ssh -o BatchMode=yes "${HOST}" "chmod -R a+rX ${DIR}/app.balancia/dist"

echo "==> Checking from outside"
for host in "${ROOT_DOMAIN}" "franco.${ROOT_DOMAIN}" "alvorada.${ROOT_DOMAIN}"; do
    curl --fail --silent --show-error --max-time 20 -o /dev/null "https://${host}/api/health"
    curl --fail --silent --show-error --max-time 20 -o /dev/null "https://${host}/painel"
    echo "    ${host} ok"
done
echo "==> Demo at ${SHA:0:7}: https://${ROOT_DOMAIN}"
