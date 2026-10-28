import pandas as pd

from rateio.leitura import ler_cadastro, ler_envio
from rateio.limpeza import cpf_normalizado

ged = pd.read_csv("dados/brutos/ged/compensacao/"
                  "compensacao_2027-02.csv", sep=";",
                  encoding="latin-1", decimal=",",
                  thousands=".", dtype={"CPF": "string"})

# 1. cadastro ativo x GED: um cooperado, uma linha
cad = ler_cadastro()
ativos = cad[cad["Situação"] == "Ativo"].copy()
ativos["cpf"] = cpf_normalizado(ativos["CPF"])
ged["cpf"] = cpf_normalizado(ged["CPF"])
confere = ativos.merge(ged[["cpf", "Valor (R$)"]], on="cpf",
                       how="outer", validate="one_to_one",
                       indicator=True)
print(confere["_merge"].value_counts().to_dict())

# 2. envio x GED pelos dígitos como foram enviados
envio = ler_envio("2027-02")
envio["chave"] = (envio["CPF"]
                  .str.replace(r"\D", "", regex=True))
ged["chave"] = ged["CPF"].str.replace(r"\D", "", regex=True)
lados = envio.merge(ged[["chave", "Nome", "Valor (R$)"]],
                    on="chave", how="outer", indicator=True,
                    validate="one_to_one",
                    suffixes=("", "_ged"))
so_envio = lados[lados["_merge"] == "left_only"]
so_ged = lados[lados["_merge"] == "right_only"]
print(len(so_envio), "CPFs do envio que a GED não achou:",
      f"R$ {so_envio['Valor'].sum():,.2f}")
print(len(so_ged), "linhas da GED sem par no envio:",
      f"R$ {so_ged['Valor (R$)'].sum():,.2f}")
print(so_ged.sort_values("Valor (R$)", ascending=False)
      [["chave", "Nome_ged", "Valor (R$)"]].head(3))
