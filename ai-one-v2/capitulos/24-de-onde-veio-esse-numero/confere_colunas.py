from rateio.dicionario import FONTES
from rateio.leitura import (ler_abadiania, ler_cadastro,
                            ler_cocalzinho, ler_corumba)

lidas = {"corumba": ler_corumba("2027-03"),
         "cocalzinho": ler_cocalzinho(["2027-03-31"]),
         "abadiania": ler_abadiania("2027-03"),
         "cadastro": ler_cadastro()}
for fonte, tabela in lidas.items():
    esperado = FONTES[fonte]["colunas"]
    if list(tabela.columns) == esperado:
        print(f"{fonte:11} colunas como no dicionário")
    else:
        print(f"{fonte:11} MUDOU: {list(tabela.columns)}")
