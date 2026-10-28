import pandas as pd

from rateio.leitura import ler_envio
from rateio.limpeza import cpf_normalizado

ged = pd.read_csv("dados/brutos/ged/compensacao/"
                  "compensacao_2027-02.csv", sep=";",
                  encoding="latin-1", decimal=",",
                  thousands=".", dtype={"CPF": "string"})
envio = ler_envio("2027-02")
envio["chave"] = cpf_normalizado(envio["CPF"])
ged["chave"] = cpf_normalizado(ged["CPF"])
lados = envio.merge(ged[["chave", "Valor (R$)"]], on="chave",
                    how="outer", indicator=True,
                    validate="one_to_one")
print(lados["_merge"].value_counts().to_dict())
