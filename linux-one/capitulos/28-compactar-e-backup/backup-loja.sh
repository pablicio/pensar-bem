#!/bin/bash
# Backup diário do banco e da configuração da loja.
set -euo pipefail

DESTINO=/var/backups/loja
DIA=$(date +%F)
mkdir -p "$DESTINO"

sudo -u postgres pg_dump loja \
  | gzip > "$DESTINO/banco-$DIA.sql.gz"
tar -czf "$DESTINO/config-$DIA.tar.gz" -C / opt/loja/config

# guarda 30 dias; apaga o que for mais velho
find "$DESTINO" -name "*.gz" -mtime +30 -delete

echo "backup $DIA: $(du -sh "$DESTINO" | cut -f1)" >&2
