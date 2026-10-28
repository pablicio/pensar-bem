import pandas as pd

from rio.serie import digitacao, ler

leitura = ler("cadernos")["leitura_cm"]
erro = digitacao(leitura)
print(erro.sum(), "leituras com um zero a mais:")
for hora in leitura.index[erro]:
    antes = leitura.loc[:hora].iloc[-2]
    depois = leitura.loc[hora:].iloc[1]
    print(f"  {hora:%d/%m/%Y %Hh}  {antes:4d}"
          f" {leitura[hora]:5d} {depois:4d} cm")
