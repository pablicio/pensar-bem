import pandas as pd

cad = pd.read_excel("dados/brutos/cadastro_cooperados.xlsx",
                    dtype={"CPF": "string"})
cad["cpf"] = (cad["CPF"].str.replace(r"\D", "", regex=True)
              .str.zfill(11))
repetidos = cad[cad["cpf"].duplicated(keep=False)]
inativas = repetidos[repetidos["Situação"] == "Inativo"]
ativas = repetidos[repetidos["Situação"] == "Ativo"]
codigo_ativa = ativas.set_index("cpf")["Código"]
pares = inativas[["cpf", "Nome", "Código"]].assign(
    ativa=inativas["cpf"].map(codigo_ativa))
primeiros = pares.sort_values("Código").head(3)
print(primeiros.to_string(index=False))
