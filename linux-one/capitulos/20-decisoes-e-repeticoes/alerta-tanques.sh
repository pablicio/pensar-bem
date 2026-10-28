#!/bin/bash
# Avisa se a última leitura de algum tanque passou do limite.

csv=/home/pi/monitor/leituras.csv
limite=8.0
problema=0

for t in {1..6}; do
  ultima=$(tail -n 60 "$csv" | grep ",$t," | tail -n 1)
  temp=$(echo "$ultima" | cut -d, -f4)
  if [[ -z $temp ]]; then
    echo "Tanque $t: sem leitura recente"
    problema=1
  elif awk -v x="$temp" -v l="$limite" \
       'BEGIN { exit !(x > l) }'; then
    echo "Tanque $t: ${temp} C (limite ${limite} C)"
    problema=1
  fi
done

exit $problema
