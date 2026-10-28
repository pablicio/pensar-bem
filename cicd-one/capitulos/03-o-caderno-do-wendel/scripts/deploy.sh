#!/usr/bin/env bash
set -euo pipefail

COMMIT="${1:?uso: deploy.sh COMMIT SERVIDOR}"
SRV="${2:?uso: deploy.sh COMMIT SERVIDOR}"
NOME="$(date +%Y%m%d-%H%M)-${COMMIT:0:7}"
DIR="/opt/embarque/releases/$NOME"

git archive --format=tar.gz -o /tmp/api.tgz "$COMMIT" api/
scp /tmp/api.tgz "deploy@$SRV:/tmp/api.tgz"

ssh "deploy@$SRV" bash -s <<EOF
set -euo pipefail
mkdir -p "$DIR"
tar xzf /tmp/api.tgz -C "$DIR" --strip-components=1
ln -s /opt/embarque/shared/.env "$DIR/.env"
python3.12 -m venv "$DIR/.venv"
"$DIR/.venv/bin/pip" install -q -r "$DIR/requirements.txt"
ln -sfn "$DIR" /opt/embarque/current
sudo systemctl restart embarque-api
redis-cli -n 2 FLUSHDB
EOF

curl -fsS "https://$SRV/saude" > /dev/null
echo "ok: $NOME em $SRV"
