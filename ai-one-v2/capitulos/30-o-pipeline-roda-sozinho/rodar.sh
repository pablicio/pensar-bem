#!/bin/sh
# o rateio de um mês: os testes primeiro, depois o pipeline
set -e
python -m pytest -q
python -m rateio --mes "$1"
