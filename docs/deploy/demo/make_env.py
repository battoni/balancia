"""Write /var/www/balancia/api.balancia/.env from .env.example with the demo server's values.

Runs ON the server as root: python3 -I make_env.py (docs/deploy/demo/README.md). Secrets come from /root/balancia/* (generated there, never printed).
Re-runnable: an existing APP_KEY is kept.
"""
import os
import re
import secrets

ROOT = "balancia.battoni.dev"
API = "/var/www/balancia/api.balancia"
SECRETS = "/root/balancia"
os.umask(0o077)


def secret(name: str, length: int = 24) -> str:
    path = f"{SECRETS}/{name}"
    if not os.path.exists(path):
        with open(path, "w") as h:
            h.write(secrets.token_urlsafe(length))
    return open(path).read().strip()


existing = {}
if os.path.exists(f"{API}/.env"):
    for line in open(f"{API}/.env"):
        if "=" in line and not line.startswith("#"):
            k, v = line.rstrip("\n").split("=", 1)
            existing[k] = v

resend_key = open(f"{SECRETS}/resend_key").read().strip() if os.path.exists(f"{SECRETS}/resend_key") else ""

values = {
    "APP_NAME": "api.balancia",
    "APP_ENV": "production",
    "APP_KEY": existing.get("APP_KEY", ""),
    "APP_DEBUG": "false",
    "APP_URL": f"https://{ROOT}",
    "FRONTEND_URL": f"https://{ROOT}",
    "LOG_STACK": "daily",
    "LOG_LEVEL": "warning",
    "LOG_DAILY_DAYS": "14",
    "DB_CONNECTION": "mysql",
    "DB_HOST": "127.0.0.1",
    "DB_PORT": "3306",
    "DB_DATABASE": "balancia",
    "DB_USERNAME": "balancia",
    "DB_PASSWORD": secret("db_password"),
    "SESSION_DRIVER": "database",
    "SESSION_DOMAIN": "null",
    "SESSION_SAME_SITE": "lax",
    "SESSION_SECURE_COOKIE": "true",
    "QUEUE_CONNECTION": "database",
    "CACHE_STORE": "database",
    "MAIL_MAILER": "resend" if resend_key else "log",
    "RESEND_API_KEY": resend_key,
    "MAIL_VERIFIED_DOMAINS": '"mail.balancia.battoni.dev"',
    "MAIL_FROM_ADDRESS": '"nao-responda@mail.balancia.battoni.dev"',
    "MAIL_FROM_NAME": '"Balancia"',
    "REGISTRATION_ENABLED": "false",
    "LOGIN_CODE_SENDER": "log",
    "LOGIN_CODE_EXPOSE": "false",
    "ASSISTANT_DRIVER": "curated",
    "SANCTUM_STATEFUL_DOMAINS": f"{ROOT},*.{ROOT}",
    "SUPERADMIN_PASSWORD": secret("superadmin_password", 15),
    "SEEDER_PWD": secret("seeder_password", 12),
    "CORS_ALLOWED_ORIGINS": f"https://{ROOT}",
    "CORS_ALLOWED_ORIGINS_PATTERNS": "'#^https://[a-z0-9-]+\\." + ROOT.replace(".", "\\.") + "$#'",
    "PLATFORM_NAME": "Balancia",
    "PLATFORM_ROOT_DOMAIN": ROOT,
    "DEFAULT_FIRM_SLUG": "balancia",
}

out, seen = [], set()
for line in open(f"{API}/.env.example"):
    line = line.rstrip("\n")
    m = re.match(r"^([A-Z0-9_]+)=", line)
    if m and m.group(1) in values:
        if m.group(1) in seen:
            continue
        seen.add(m.group(1))
        out.append(f"{m.group(1)}={values[m.group(1)]}")
    else:
        out.append(line)
for k, v in values.items():
    if k not in seen:
        out.append(f"{k}={v}")

with open(f"{API}/.env", "w") as h:
    h.write("\n".join(out) + "\n")
os.chmod(f"{API}/.env", 0o640)
print("wrote .env; mail:", values["MAIL_MAILER"], "; missing from template:", [k for k in values if k not in seen])
