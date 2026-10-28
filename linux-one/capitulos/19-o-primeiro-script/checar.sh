#!/bin/bash
# Confere a saúde do Pi dos tanques. Rodar toda manhã.

echo "== Disco =="
df -h / | tail -n 1

echo "== Últimas leituras =="
tail -n 6 /home/pi/monitor/leituras.csv

echo "== Tamanho do CSV =="
du -h /home/pi/monitor/leituras.csv
