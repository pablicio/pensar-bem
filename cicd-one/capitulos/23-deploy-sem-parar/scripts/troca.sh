#!/usr/bin/env bash
set -euo pipefail
IMG="ghcr.io/mare-digital/embarque-api@${1:?digest}"
SRVS=$(cat infra/producao/servidores)

for S in $SRVS; do
  ATUAL=$(ssh "deploy@$S" cat /opt/embarque/cor)
  NOVA=$([ "$ATUAL" = azul ] && echo verde || echo azul)
  ssh "deploy@$S" ./prepara.sh "$NOVA" "$IMG"
done

for S in $SRVS; do
  ssh "deploy@$S" ./vira.sh
done
