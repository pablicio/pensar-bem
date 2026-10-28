#!/bin/sh
set -e

if [ -z "$DATABASE_URL" ]; then
  echo "entrypoint: falta a variável DATABASE_URL" >&2
  exit 1
fi

exec "$@"
