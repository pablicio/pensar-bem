import re

from lupa.diario import atos, gabarito
from lupa.extrator import limpa

corpus = {a["id"]: a for a in atos()}
# as regras do Renan, escritas olhando três extratos
PADROES = {
    "CONTRATADA": r"Contratada: (.+?), CNPJ",
    "OBJETO": r"Objeto(?: do contrato)?: (.+?)\. Valor",
    "VALOR": r"Valor(?: global)?: (R\$ [\d.]+,\d\d)",
    "PRAZO": r"Prazo(?: de vigência)?: (\d+ \(\w+\) \w+)",
}
certos = {e: 0 for e in PADROES}
total = 0
erros = {}
for ident, g in gabarito().items():
    ato = corpus.get(ident)
    if (not g["entidades"] or ato is None
            or ato["data"] < "2027"):
        continue
    total += 1
    texto = limpa(ato["texto"])
    for inicio, fim, nome in g["entidades"]:
        ouro = limpa(ato["texto"][inicio:fim])
        m = re.search(PADROES[nome], texto)
        if m and m.group(1) == ouro:
            certos[nome] += 1
        else:
            erros.setdefault(nome, ouro)
print(f"{total} extratos de 2027")
for nome, n in certos.items():
    print(f"  {nome:10}  {n:3} certos  ({n / total:.1%})")
for nome, ouro in erros.items():
    print(f"{nome} perdido: {ouro[:48]}")
