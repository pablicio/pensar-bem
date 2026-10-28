#!/bin/bash
# Sai com 1 se o disco / passar de 90%.

uso=$(df --output=pcent / | tail -n 1 | tr -dc '0-9')
echo "Disco em ${uso}%"
[ "$uso" -le 90 ] || exit 1
