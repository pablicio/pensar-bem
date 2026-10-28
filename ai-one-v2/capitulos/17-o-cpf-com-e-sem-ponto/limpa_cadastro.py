import pandas as pd

from rateio.cpf import verificadores

cad = pd.read_excel("dados/brutos/cadastro_cooperados.xlsx",
                    dtype={"CPF": "string"})
cad["cpf"] = (cad["CPF"].str.replace(r"\D", "", regex=True)
              .str.zfill(11))

repetidos = cad[cad["cpf"].duplicated(keep=False)]
print(len(repetidos), "linhas com CPF repetido")
print(repetidos["Situação"].value_counts().to_dict())
dirceu = repetidos[repetidos["cpf"] == "06041976598"]
print(dirceu[["Código", "CPF", "Situação"]])


def valido(cpf):
    return verificadores(cpf[:9]) == [int(c) for c in cpf[9:]]


print("CPFs inválidos:", (~cad["cpf"].map(valido)).sum())
ativos = cad[cad["Situação"] == "Ativo"]
mesmo_nome = ativos["Nome"].duplicated(keep=False).sum()
print("ativos com nome repetido:", mesmo_nome)
