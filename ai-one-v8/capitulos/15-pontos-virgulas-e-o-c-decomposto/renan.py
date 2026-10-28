import csv
import re
import unicodedata

from lupa.diario import BRUTOS, atos
from lupa.extrator import limpa

CNPJ = re.compile(r"Contratada: ([^,]+), CNPJ nº "
                  r"(\d\d\.\d{3}\.\d{3}/\d{4}-\d\d)")
with open(BRUTOS / "empresas.csv", encoding="utf-8") as f:
    empresas = {e["nome"] for e in csv.DictReader(f)}


def pdf(texto):
    return unicodedata.normalize("NFC", texto) != texto


def confere(textos, como):
    achados = conhecidas = 0
    for t in textos:
        for nome, cnpj in CNPJ.findall(como(t)):
            achados += 1
            conhecidas += nome in empresas
    return achados, conhecidas


contratos = [a["texto"] for a in atos()
             if "Contratada:" in a["texto"]]
for origem, textos in [
        ("editor", [t for t in contratos if not pdf(t)]),
        ("PDF", [t for t in contratos if pdf(t)])]:
    print(f"{origem}: {len(textos)} contratos")
    for nome, como in [("cru", lambda t: t),
                       ("limpo", limpa)]:
        achados, conhecidas = confere(textos, como)
        print(f"  {nome:6} CNPJs achados {achados:5}"
              f"  empresa na lista {conhecidas:5}")
