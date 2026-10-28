import bisect

import pandas as pd

from cruza import por_dicionario
from rateio.limpeza import cpf_normalizado


def por_busca_binaria(cpfs, linhas):
    ordenadas = sorted(linhas, key=lambda linha: linha[0])
    chaves = [cpf for cpf, _ in ordenadas]
    totais = []
    for cpf in cpfs:
        inicio = bisect.bisect_left(chaves, cpf)
        fim = bisect.bisect_right(chaves, cpf)
        soma = 0.0
        for _, kwh in ordenadas[inicio:fim]:
            soma += kwh
        totais.append(soma)
    return totais


arquivo = "dados/brutos/ged/consumo/consumo_2027-02.csv"
fev = pd.read_csv(arquivo, dtype={"cpf": "string"})
fev["cpf"] = cpf_normalizado(fev["cpf"])
cpfs = list(fev["cpf"].unique())
linhas = list(zip(fev["cpf"], fev["kwh"]))
binaria = por_busca_binaria(cpfs, linhas)
dicionario = por_dicionario(cpfs, linhas)
print("mesmos totais:", binaria == dicionario)
