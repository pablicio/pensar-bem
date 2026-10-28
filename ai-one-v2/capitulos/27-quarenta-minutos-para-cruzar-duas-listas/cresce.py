import time

import pandas as pd

from cruza import por_dicionario, por_lista
from rateio.limpeza import cpf_normalizado

arquivo = "dados/brutos/ged/consumo/consumo_2027-02.csv"
fev = pd.read_csv(arquivo, dtype={"cpf": "string"})
fev["cpf"] = cpf_normalizado(fev["cpf"])
todos = list(fev["cpf"].unique())


def cronometra(funcao, *argumentos):
    inicio = time.perf_counter()
    resultado = funcao(*argumentos)
    return resultado, time.perf_counter() - inicio


tamanhos, tempos = [], []
for n in [100, 200, 400, 800]:
    cpfs = todos[:n]
    parte = fev[fev["cpf"].isin(cpfs)]
    linhas = list(zip(parte["cpf"], parte["kwh"]))
    a, t_lista = cronometra(por_lista, cpfs, linhas)
    b, t_dict = cronometra(por_dicionario, cpfs, linhas)
    assert a == b
    tamanhos.append((n, len(linhas), n * len(linhas)))
    tempos.append((n, t_lista, t_dict))

print("cooperados  linhas  comparações")
for n, linhas, comparacoes in tamanhos:
    print(f"{n:>10}  {linhas:>6}  {comparacoes:>11,}")
print("cooperados  lista (s)  dicionário (s)")
for n, t_lista, t_dict in tempos:
    print(f"{n:>10}  {t_lista:>9.3f}  {t_dict:>14.4f}")
