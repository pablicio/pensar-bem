import csv
import re

from lupa.cnpj import valido
from lupa.diario import BRUTOS

with open(BRUTOS / "empresas.csv", encoding="utf-8") as f:
    lista = [re.sub(r"\D", "", e["cnpj"])
             for e in csv.DictReader(f)]

um = troca = um_pego = troca_pega = 0
for c in lista:
    for i in range(14):
        for d in "0123456789":
            if d != c[i]:                 # um dígito errado
                um += 1
                um_pego += not valido(c[:i] + d + c[i + 1:])
    for i in range(13):
        if c[i] != c[i + 1]:              # vizinhos trocados
            troca += 1
            t = c[:i] + c[i + 1] + c[i] + c[i + 2:]
            troca_pega += not valido(t)
print(f"um dígito errado: {um_pego} de {um}"
      f" ({100 * um_pego / um:.2f}%) pegos")
print(f"vizinhos trocados: {troca_pega} de {troca}"
      f" ({100 * troca_pega / troca:.2f}%) pegos")
