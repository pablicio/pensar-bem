#!/usr/bin/env bash
set -euo pipefail
DIGEST="${1:?uso: implanta.sh DIGEST AMBIENTE}"
AMB="${2:?uso: implanta.sh DIGEST AMBIENTE}"
IMG="ghcr.io/mare-digital/embarque-api@$DIGEST"

for SRV in $(cat "infra/$AMB/servidores"); do
  echo "→ $SRV"
  ssh "deploy@$SRV" "cd /opt/embarque &&
    echo IMAGEM=$IMG > .imagem &&
    docker compose --env-file .imagem pull api &&
    docker compose --env-file .imagem up -d api"
  ./scripts/fumaca.sh "$SRV"
done
