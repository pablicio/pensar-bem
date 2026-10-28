#!/bin/sh
# uso: ./build.sh NOMEPROG   (compila src/NOMEPROG.cbl em bin/)
set -e
mkdir -p bin
cobc -x -std=ibm -Wall -I copy -o "bin/$1" "src/$1.cbl"
echo "ok: bin/$1"
