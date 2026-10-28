#!/bin/bash
# Uso: tanque.sh NUMERO [DATA]
# Mostra as leituras de um tanque num dia (padrão: hoje).

tanque="$1"
dia="${2:-$(date +%F)}"

grep "^$dia," /home/pi/monitor/leituras.csv \
  | grep ",$tanque," \
  | tail -n 5
