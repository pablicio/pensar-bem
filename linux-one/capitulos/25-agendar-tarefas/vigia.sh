#!/bin/bash
set -uo pipefail
source /home/pi/monitor/monitor.env

msg=$(/home/pi/bin/alerta-tanques.sh) && exit 0

curl -s -o /dev/null \
  "https://api.telegram.org/bot$TOKEN_TELEGRAM/sendMessage" \
  -d chat_id=-100184732991 \
  --data-urlencode text="VIGIA: $msg"
