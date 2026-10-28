#!/bin/bash
# Arquiva por mês as leituras com mais de 90 dias e
# deixa no CSV só os últimos 90 dias.
set -euo pipefail

CSV=/home/pi/monitor/leituras.csv
DESTINO=/home/pi/arquivo
CORTE=$(date -d '90 days ago' +%F)

log() { echo "$(date '+%F %T') $*" >&2; }

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

mkdir -p "$DESTINO"
log "corte: $CORTE"

# meses antigos (AAAA-MM), sem o cabeçalho
meses=$(awk -F, -v c="$CORTE" 'NR>1 && $1 < c {
  print substr($1,1,7) }' "$CSV" | sort -u)

for mes in $meses; do
  arq="$DESTINO/leituras-$mes.csv.gz"
  [[ -e $arq ]] && { log "$mes já arquivado"; continue; }
  grep "^$mes" "$CSV" | gzip > "$arq"
  log "$mes -> $arq"
done

# o CSV novo: cabeçalho + leituras a partir do corte
head -n 1 "$CSV" > "$tmp"
awk -F, -v c="$CORTE" 'NR>1 && $1 >= c' "$CSV" >> "$tmp"
cat "$tmp" > "$CSV"
log "CSV reduzido a $(wc -l < "$CSV") linhas"
