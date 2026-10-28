import pandas as pd

from rateio.leitura import ler_cadastro
from rateio.limpeza import cpf_normalizado

ged = pd.read_csv("dados/brutos/ged/compensacao/"
                  "compensacao_2027-02.csv", sep=";",
                  encoding="latin-1", decimal=",",
                  thousands=".", dtype={"CPF": "string"})
cad = ler_cadastro()
ativos = cad[cad["Situação"] == "Ativo"].copy()
ativos["cpf"] = cpf_normalizado(ativos["CPF"])
ged["cpf"] = cpf_normalizado(ged["CPF"])
assert ativos["cpf"].is_unique
junto = ativos.merge(ged[["cpf", "Valor (R$)"]], on="cpf",
                     how="outer", indicator=True)
assert len(junto) == len(ativos) + 1      # a sede
assert (junto["_merge"] != "left_only").all()
print("junção conferida:", len(junto), "linhas")
