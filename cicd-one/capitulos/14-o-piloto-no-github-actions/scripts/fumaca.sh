#!/usr/bin/env bash
set -euo pipefail
URL="https://$1"
COMMIT="${GITHUB_SHA:0:7}"
for i in $(seq 1 20); do
  curl -fsS "$URL/saude" > /dev/null && break
  sleep 3
done
curl -fsS "$URL/versao" | grep -q "\"commit\":\"$COMMIT\""
curl -fsS "$URL/viagens?linha=soure" > /dev/null
