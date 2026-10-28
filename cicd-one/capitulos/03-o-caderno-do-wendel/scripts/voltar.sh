#!/usr/bin/env bash
set -euo pipefail
SRV="${1:?uso: voltar.sh SERVIDOR}"
ssh "deploy@$SRV" bash -s <<'EOF'
set -euo pipefail
cd /opt/embarque/releases
ANTERIOR="$(ls -1 | tail -n 2 | head -n 1)"
ln -sfn "$PWD/$ANTERIOR" /opt/embarque/current
sudo systemctl restart embarque-api
echo "voltou para $ANTERIOR"
EOF
