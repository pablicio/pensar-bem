"""Gera os dados brutos da Coopersol Cerrado.

Rode uma vez, na pasta do projeto:
    python dados/gerar_coopersol.py
Grava tudo em dados/brutos/. Mesma semente, mesmos bytes.
"""
import numpy as np

from cadastro import gravar_cadastro, montar_cadastro
from ceu import gerar_energia
from ged import gravar_consumo, gravar_estacao, gravar_ged
from inversores import gravar_a, gravar_b, gravar_c
from mundo import BRUTOS, DIAS, PASSOS, USINAS
from planilha import gravar_planilha


def gerar():
    BRUTOS.mkdir(parents=True, exist_ok=True)
    energia = {u: gerar_energia(mw, n)
               for u, (_, mw, n) in USINAS.items()}
    gravar_a(energia["corumba"])
    gravar_b(energia["cocalzinho"])
    fora = gravar_c(energia["abadiania"])
    presente = np.ones((DIAS, PASSOS))
    for d, p in fora:
        presente[d, p] = 0
    pessoas, dirceu = montar_cadastro()
    for p in pessoas:
        base = {"residencial": 180, "comercio": 1400,
                "rural": 620}[p["tipo"]]
        p["consumo"] = int(base * p["peso"]
                           / {"residencial": 1, "comercio": 4,
                              "rural": 3}[p["tipo"]])
    gravar_cadastro(pessoas)
    gravar_ged(pessoas, energia, presente)
    gravar_consumo(pessoas)
    gravar_estacao()
    gravar_planilha(pessoas, energia, presente)


if __name__ == "__main__":
    gerar()
