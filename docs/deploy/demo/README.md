# Demo server — balancia.battoni.dev

The demo runs on the Battoni Dev droplet (`ssh root@server.battoni.dev`, 138.197.6.208, Ubuntu 24.04,
1 GB RAM shared with the other client APIs). It follows `../runbook.md` with `<root>` =
`balancia.battoni.dev`, except where this page says otherwise. Set up on 17/11/2026.

| Host | What |
| --- | --- |
| `https://balancia.battoni.dev` | the platform firm (`balancia`): the product site and the operator's console |
| `https://franco.balancia.battoni.dev` | Franco Contabilidade |
| `https://alvorada.balancia.battoni.dev` | Alvorada Contabilidade, the invented demo firm |

## Every deploy

From the main checkout, on an up-to-date, clean `main`:

```bash
make deploy-demo
```

`scripts/deploy-demo.sh` builds the SPA locally, moves the server's tree to the same commit, runs
`api.balancia/deploy.sh` there, uploads `dist/`, and checks every host from outside. About two
minutes, most of it the NF-e seeder.

**The database is rebuilt on every deploy** (`migrate:fresh`, then the demo seeders once with
`APP_ENV=local`). The demo holds invented data only, and the schema is still folded into the
`create_*` migrations: the owner kept folding for the demo (17/11/2026). Anything typed into the
demo is gone after the next deploy. A production deploy does not copy this — see `../runbook.md`.

## Where things are on the server

| What | Where |
| --- | --- |
| Repository | `/var/www/balancia` (clone of `battoni/balancia`, `main`) |
| API env | `/var/www/balancia/api.balancia/.env`, written by `make_env.py` |
| Secrets | `/root/balancia/` (root only): `db_password`, `superadmin_password`, `seeder_password`, `resend_key` |
| Vhost | `/etc/nginx/sites-available/balancia.battoni.dev` (`nginx.conf` here, plus certbot's TLS lines) |
| Queue worker | supervisor `balancia-worker` (`/etc/supervisor/conf.d/balancia-worker.conf`), log `/var/log/balancia-worker.log` |
| Scheduler | `www-data`'s crontab: `schedule:run` every minute |
| Logs | `api.balancia/storage/logs/laravel-*.log`, `/var/log/nginx/balancia-*.log` |
| Database | MySQL 8, database and user `balancia` (rights on `balancia` only) |

## Differences from the runbook

- **No wildcard certificate.** `battoni.dev`'s DNS panel has no API for certbot's DNS-01
  challenge, so one certificate names each host (HTTP-01). DNS does have the wildcard
  (`A *.balancia → 138.197.6.208`). A new firm's host needs its name added:
  `certbot --nginx --expand -d balancia.battoni.dev -d www.balancia.battoni.dev -d franco.balancia.battoni.dev -d alvorada.balancia.battoni.dev -d <slug>.balancia.battoni.dev`.
- **`fastcgi_param SCRIPT_NAME /index.php`** in the `/api/` location. `fastcgi_params` sets it to
  the request path, and Symfony would take `/api/…` as the base URL.
- **Mail** goes through Resend from `nao-responda@mail.balancia.battoni.dev` once `resend_key`
  exists and the domain is verified; until then `MAIL_MAILER=log`. Re-run `make_env.py` after
  adding the key, then `php artisan optimize` as `www-data`.

## Setting it up again

```bash
# on the server, as root
cd /var/www && git clone git@github.com:battoni/balancia.git balancia
cd balancia/api.balancia && COMPOSER_ALLOW_SUPERUSER=1 composer install --no-dev -o
mkdir -m 700 -p /root/balancia                       # make_env.py generates the secrets in it
python3 -I ../docs/deploy/demo/make_env.py && php artisan key:generate --force
mysql -e "CREATE DATABASE balancia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE USER 'balancia'@'localhost' IDENTIFIED BY '$(cat /root/balancia/db_password)'; GRANT ALL ON balancia.* TO 'balancia'@'localhost';"
chown root:www-data .env && chmod 640 .env
cp ../docs/deploy/demo/nginx.conf /etc/nginx/sites-available/balancia.battoni.dev
ln -s /etc/nginx/sites-available/balancia.battoni.dev /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
certbot --nginx -d balancia.battoni.dev -d www.balancia.battoni.dev -d franco.balancia.battoni.dev -d alvorada.balancia.battoni.dev
# supervisor program and cron line: the table above; then, from the laptop:
make deploy-demo
```
