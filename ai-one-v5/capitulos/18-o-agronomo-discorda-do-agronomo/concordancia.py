import csv

import numpy as np
from sklearn.metrics import cohen_kappa_score

from folha.conjunto import CLASSES, PASTA

with open(PASTA / "revisao.csv", encoding="utf-8") as f:
    revisao = list(csv.DictReader(f))


def matriz(a, b):
    """Pares de rótulos: linha = o de a, coluna = o de b."""
    m = np.zeros((6, 6), dtype=int)
    for linha in revisao:
        i, j = CLASSES.index(linha[a]), CLASSES.index(linha[b])
        m[i, j] += 1
    return m


def kappa(m):
    """O kappa de Cohen a partir da matriz de concordância."""
    n = m.sum()
    observada = np.trace(m) / n
    esperada = (m.sum(axis=1) @ m.sum(axis=0)) / n ** 2
    return observada, esperada, (observada - esperada) / (
        1 - esperada)


m = matriz("edson_2026", "edson_2027")
print("Dr. Edson 2026 (linhas) contra 2027 (colunas):")
print("          " + " ".join(f"{c[:5]:>5}" for c in CLASSES))
for c, linha in zip(CLASSES, m):
    print(f"{c[:9]:9} " + " ".join(f"{v:5}" for v in linha))
NOMES = {"edson_2026": "Edson 2026",
         "edson_2027": "Edson 2027", "bia": "Bia"}
PARES = [("edson_2026", "edson_2027"), ("edson_2027", "bia"),
         ("edson_2026", "bia")]
print()
print("par                        p_o    p_e  kappa  sklearn")
for a, b in PARES:
    po, pe, k = kappa(matriz(a, b))
    conferido = cohen_kappa_score([x[a] for x in revisao],
                                  [x[b] for x in revisao])
    par = f"{NOMES[a]} × {NOMES[b]}"
    print(f"{par:24} {po:6.3f} {pe:6.3f} {k:6.3f}"
          f" {conferido:8.3f}")
