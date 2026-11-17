#!/usr/bin/env bash
#
# The server half of `make deploy-demo` (scripts/deploy-demo.sh), which has already moved the
# tree to the commit being published. Run as root on the demo server, from anywhere.
#
# Adapted from api.lifeshifter/deploy.sh, which earned every step here the hard way on
# 2026-09-02, each omission looking like a different bug:
#
#   - no `composer install` → a class-not-found on the two endpoints that use a new package,
#     while every other route kept working, so the deploy looked fine.
#   - no cache rebuild → routes frozen from before the pull: a new route answers 405 naming
#     the methods of the `{id}` route that swallowed it.
#   - `artisan` or `composer` as root → files the web user cannot read, which took an API
#     fully down: `storage/framework/views` unwritable meant 500 on EVERY route, reported as
#     a `tempnam()` warning naming neither the directory nor the cause.
#
# Ordering is not cosmetic: dependencies before migrations (a migration may use a new
# package), ownership before the caches are written, caches before the reload that reads them.
#
# ─────────────────────────────────────────────────────────────────────────────────────────
# THIS SCRIPT DROPS THE DATABASE ON EVERY DEPLOY, AND THAT IS THE POINT HERE.
#
# The demo holds invented data only, and the schema is still folded into the `create_*`
# migrations (arcus §3, runbook "The folded migrations end at the first deploy" — the owner kept
# folding for the demo, 17/11/2026). A plain `migrate --force` runs PENDING migrations only, so a
# column added to a create that already ran would be missing here, the code would read `null`
# and the screen would lie with no error anywhere. So the demo rebuilds.
#
# **A production deploy MUST NOT copy this.** With real firms, `migrate:fresh` is a data-loss
# incident with a green check mark next to it — that deploy follows the runbook instead.
# This file is LOCAL in the sync manifest and never travels.
# ─────────────────────────────────────────────────────────────────────────────────────────
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

WEB_USER="${DEPLOY_WEB_USER:-www-data}"
FPM_SERVICE="${DEPLOY_FPM_SERVICE:-php8.4-fpm}"
WORKER="${DEPLOY_WORKER:-balancia-worker}"
HEALTH_URL="${DEPLOY_HEALTH_URL:-https://balancia.battoni.dev/api/health}"

echo "==> Installing PHP dependencies"
COMPOSER_ALLOW_SUPERUSER=1 composer install --no-dev --optimize-autoloader --no-interaction --no-progress --quiet

echo "==> Handing the tree back to ${WEB_USER}"
# Before anything runs artisan as the web user: composer just rewrote vendor/ as root.
chown -R "${WEB_USER}":"${WEB_USER}" vendor storage bootstrap/cache
chmod -R ug+rwX storage bootstrap/cache

echo "==> Discarding the cached config"
# The seeders read `config('seeding.*')`, and the previous deploy ended with a config cache built
# from the previous tree and `.env`: a rotated SUPERADMIN_PASSWORD would not reach the
# super-admin, and a config file this pull added would be missing. Rebuilt at the bottom.
sudo -u "${WEB_USER}" php artisan optimize:clear --quiet

echo "==> Rebuilding the database: reference rows, then the demo"
# `--force` lets these run outside a terminal; production refuses without it.
sudo -u "${WEB_USER}" php artisan migrate:fresh --seed --force --quiet
# The demo seeders write only under `local`/`testing` (DemoEnvironment). The app itself runs as
# `production` — the QA login-as and the mail previews stay off — and only this one command sees
# `local`: a real environment variable wins over `.env`, and the config is not cached yet.
# The NF-e seeder alone takes about a minute here.
sudo -u "${WEB_USER}" env APP_ENV=local php artisan db:seed --force --quiet

echo "==> Linking public storage"
# Only when missing: `storage:link` treats an existing link as an error. Created as root because
# public/ belongs to root (api.impressao, 2026-09-04).
if [ ! -e public/storage ]; then
    php artisan storage:link --quiet
    chown -h "${WEB_USER}":"${WEB_USER}" public/storage
fi

echo "==> Rebuilding caches"
chown -R "${WEB_USER}":"${WEB_USER}" storage bootstrap/cache
sudo -u "${WEB_USER}" php artisan optimize --quiet

echo "==> Restarting the queue worker and reloading ${FPM_SERVICE}"
# queue:restart asks the worker to exit after its current job; supervisor starts it again on
# the new code. Without it the worker runs the old classes until its --max-time.
sudo -u "${WEB_USER}" php artisan queue:restart --quiet
supervisorctl status "${WORKER}" >/dev/null || supervisorctl start "${WORKER}"
systemctl reload "${FPM_SERVICE}"

echo "==> Health check"
# Through the public hostname, NOT 127.0.0.1: this droplet serves several projects, and an
# address with no Host header lands on somebody else's default vhost.
curl --fail --silent --show-error --location --max-time 20 -o /dev/null "${HEALTH_URL}"
echo "==> API at $(git rev-parse --short HEAD)"
