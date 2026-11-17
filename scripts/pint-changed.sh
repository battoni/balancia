#!/usr/bin/env bash
# Run Laravel Pint on api.balancia PHP files changed on this branch (+ uncommitted) — never the whole tree.
# Usage: scripts/pint-changed.sh [base-branch]   (default: main)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BASE="${1:-main}"
ARCUS="$ROOT/api.balancia"
PINT="$ARCUS/vendor/bin/pint"

if [ ! -x "$PINT" ]; then
  echo "✗ Pint not installed. One-time setup:" >&2
  echo "    (cd api.balancia && composer require laravel/pint --dev)" >&2
  exit 1
fi

cd "$ROOT"

# Union: committed vs the fork point from main + staged + unstaged + untracked, api.balancia PHP only.
CHANGED="$( {
  git diff --name-only --diff-filter=d "$BASE"...HEAD -- api.balancia
  git diff --name-only --diff-filter=d -- api.balancia
  git diff --cached --name-only --diff-filter=d -- api.balancia
  git ls-files --others --exclude-standard -- api.balancia
} 2>/dev/null | grep -E '\.php$' | sort -u || true)"

if [ -z "$CHANGED" ]; then
  echo "Pint: no changed api.balancia PHP files vs $BASE — nothing to format."
  exit 0
fi

CONFIG_ARG=()
[ -f "$ARCUS/pint.json" ] && CONFIG_ARG=(--config "$ARCUS/pint.json")

# `${arr[@]+"${arr[@]}"}` and not the bare `"${arr[@]}"`, because of `set -u` above: in bash 3.2
# — which is what macOS ships and therefore what every developer here runs — expanding an EMPTY
# array under `set -u` is an "unbound variable" error, not an empty list. There is no
# `api.balancia/pint.json`, so the array is always empty and this line always died:
#
#     scripts/pint-changed.sh: line 35: CONFIG_ARG[@]: unbound variable
#
# Pint had therefore never run from this script on a Mac. It passed review because the failure
# is a bash error on the last line, which reads like an environment problem rather than a gate
# that never executed. Do not "simplify" this back.
echo "$CHANGED" | sed "s|^|$ROOT/|" | xargs "$PINT" ${CONFIG_ARG[@]+"${CONFIG_ARG[@]}"}
